"""Patch only the new results block, preserving the latest page structure."""
from html.parser import HTMLParser
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


class DivRanges(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.stack = []
        self.ranges = []
        self.feed(source)

    def source_offset(self):
        line, col = self.getpos()
        return self.offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.stack.append((self.source_offset(), dict(attrs)))

    def handle_endtag(self, tag):
        if tag == 'div' and self.stack:
            start, attrs = self.stack.pop()
            self.ranges.append((start, self.source_offset() + len('</div>'), attrs))


path = ROOT / 'index.html'
source = path.read_text(encoding='utf-8')
matches = [(a, b) for a, b, attrs in DivRanges(source).ranges
           if 'score-comparison-wrapper' in attrs.get('class', '').split()]
assert len(matches) == 1, 'Expected one results block'
start, end = matches[0]
fragment = (ROOT / 'qa-pa/current-challenge-results.html').read_text(encoding='utf-8').strip()
source = source[:start] + fragment + source[end:]
path.write_text(source, encoding='utf-8', newline='\n')
shutil.copy2(path, ROOT / 'website/index.html')
print('Preserved latest Gemini page; replaced only the challenge results block.')
