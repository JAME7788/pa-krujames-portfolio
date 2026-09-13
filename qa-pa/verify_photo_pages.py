from pathlib import Path
from datetime import date
from lxml import html
import json
import subprocess
from curate_current_web import PHOTOS, ROOT

node = Path('C:/Users/KruJames/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
approved = {p['src'] for p in PHOTOS}
for photo in PHOTOS:
    assert date(2025,10,1) <= date.fromisoformat(photo['date']) <= date(2026,9,13)
    assert (ROOT / photo['src']).is_file()
results = []
for relative in ('index.html','embeds/canva-slides-krujames.html'):
    path = ROOT / relative
    source = path.read_text(encoding='utf-8')
    doc = html.fromstring(source)
    ids = doc.xpath('//@id')
    assert len(ids) == len(set(ids)), 'Duplicate IDs'
    for img in doc.xpath('//img[@src]'):
        src = img.get('src')
        if not src:
            continue
        assert (path.parent / src).is_file(), f'Missing {src}'
        if not src.removeprefix('../').startswith('assets/images/') and '/mascots/' not in src:
            assert src.removeprefix('../') in approved, f'Unreviewed activity image {src}'
    for script in doc.xpath('//script[not(@src)]'):
        subprocess.run([str(node), '-e', 'new (require("node:vm").Script)(require("node:fs").readFileSync(0,"utf8"));'], input=script.text or '', text=True, check=True, capture_output=True, encoding='utf-8')
    assert 'function hydrateCustomGallery' not in source
    assert 'onerror="this.src=' not in source
    assert 'รอตรวจสอบคะแนนต้นฉบับ' in source
    assert 'ระดับ ๓ (ดี)</span>' not in source
    assert (ROOT / 'website' / relative).read_bytes() == path.read_bytes()
    results.append({'file':relative,'images':len(doc.xpath('//img[@src]')),'verified_placements':len(doc.xpath('//*[@data-evidence-id]')),'scripts':'syntax passed'})
assert len(html.fromstring((ROOT/'index.html').read_text(encoding='utf-8')).xpath('//*[@id="gallery-container"]/*[@data-evidence-id]')) == 5
subprocess.run([str(node),'--check',str(ROOT/'assets/evidence-report.js')],check=True)
(ROOT/'qa-pa/photo-verification-20260913.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
