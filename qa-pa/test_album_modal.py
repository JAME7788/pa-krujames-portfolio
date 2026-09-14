from pathlib import Path
from lxml import html
import json

root=Path(__file__).resolve().parents[1]
source=(root/'index.html').read_text(encoding='utf-8')
tree=html.fromstring(source)
ids=['firebase-modal','lightbox','profile-modal','album-modal']
for name in ids:
    nodes=tree.xpath(f'//*[@id="{name}"]')
    assert len(nodes)==1 and nodes[0].getparent().tag=='body',name
controller=source.split('    function openAlbumModal(',1)[1].split('    // Interactive Before/After',1)[0]
lightbox=source.split('    function openLightbox(',1)[1].split('    // Mobile Navigation Toggle',1)[0]
data=json.JSONDecoder().raw_decode(source.split('const ALBUMS_DATA = ',1)[1])[0]
assert any(a['id']=='album-2-2' for a in data)
styles='\n'.join(tree.xpath('//style/text()'))
modals='\n'.join(html.tostring(tree.xpath(f'//*[@id="{name}"]')[0],encoding='unicode') for name in ['lightbox','album-modal'])
# A component fixture only; the production access gate is untouched.
fixture=f'''<!doctype html><html lang="th"><head><meta charset="utf-8">
<base href="{root.as_uri()}/"><style>{styles}</style></head>
<body><button onclick="openAlbumModal('album-2-2')">Test album 2.2</button>
{modals}<script>const ALBUMS_DATA={json.dumps(data,ensure_ascii=False)};
function openLightbox({lightbox}
function openAlbumModal({controller}</script></body></html>'''
path=root/'tmp/album-component-test.html'
path.write_text(fixture,encoding='utf-8')
print('PASS modal roots; fixture:',path)
