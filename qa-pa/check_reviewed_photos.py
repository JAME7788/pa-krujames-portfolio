from pathlib import Path
import json
import re
from collections import Counter
from curate_current_web import Document

root = Path(__file__).resolve().parents[1]
albums = json.loads((root / 'albums_data.json').read_text(encoding='utf-8'))
html = (root / 'index.html').read_text(encoding='utf-8')
inline, _ = json.JSONDecoder().raw_decode(html.split('const ALBUMS_DATA = ', 1)[1])
assert inline == albums, 'Inline album data differs from JSON'
assert (root/'website/index.html').read_text(encoding='utf-8') == html, 'Mirror differs'
assert json.loads((root/'website/albums_data.json').read_text(encoding='utf-8')) == albums
doc = Document(html)
ids = [n.attrs['id'] for n in doc.nodes if 'id' in n.attrs]
assert len(ids) == len(set(ids)), 'Duplicate HTML IDs'
images = [i for a in albums for i in a['items']]
assert len({i['src'] for i in images}) == len(images)
for a in albums:
    assert not a.get('share_url'), 'Legacy unreviewed photo album link remains'
    for item in a['items']:
        assert (root/item['src']).is_file()
        assert '202509' not in item['src']
        if item.get('date_iso'):
            assert '2025-10-01' <= item['date_iso'] <= '2026-09-30'
    for link in a.get('links', []):
        if link['href'].startswith('#'):
            assert link['href'][1:] in ids
        elif not link['href'].startswith('https://'):
            assert (root/link['href']).is_file()
    if re.fullmatch('album-[1-3]-[1-8]', a['id']):
        card = doc.by_id(a['id'].replace('album-', 'ind-'))
        displayed = [n.attrs['src'] for n in doc.nodes if n.tag == 'img' and card.start < n.start < card.end]
        assert displayed == [i['src'] for i in a['items'][:2]], a['id']
donation = [a['id'] for a in albums for i in a['items'] if 'IMG_20251201_' in i['src']]
assert donation == ['album-2-2'], donation
assert not any('20260811' in i['src'] for a in albums if a['id']=='album-awards' for i in a['items'])
for n in doc.nodes:
    if n.tag=='img' and n.attrs.get('src') and not n.attrs['src'].startswith('https://'):
        assert (root/n.attrs['src']).exists(), n.attrs['src']
print(f'PASS: {len(albums)} albums, {len(images)} unique images; dates, placement, mirrors, links and local assets checked')
