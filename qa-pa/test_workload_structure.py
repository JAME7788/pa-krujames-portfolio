from html.parser import HTMLParser
from pathlib import Path


class WorkloadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.active = False
        self.panes = []
        self.cards = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section' and attrs.get('id') == 'workload':
            self.active = True
        if not self.active or tag != 'div':
            return
        classes = attrs.get('class', '').split()
        if 'tab-pane' in classes:
            assert len(self.stack) == 1, ('Tab outside container', attrs)
            self.panes.append(attrs['id'])
        if 'subject-card' in classes:
            assert any('tab-pane' in a.get('class', '').split() for a in self.stack)
            self.cards += 1
        self.stack.append(attrs)

    def handle_endtag(self, tag):
        if not self.active:
            return
        if tag == 'div':
            assert self.stack, 'Extra closing div in workload'
            self.stack.pop()
        if tag == 'section':
            assert not self.stack, 'Unclosed div in workload'
            self.active = False


root = Path(__file__).resolve().parents[1]
parser = WorkloadParser()
parser.feed((root / 'index.html').read_text(encoding='utf-8'))
assert len(parser.panes) == len(set(parser.panes)) == 5
assert (root / 'index.html').read_bytes() == (root / 'website/index.html').read_bytes()
print(f'PASS: 5 tabs and {parser.cards} cards remain inside the workload container')
