from pathlib import Path
from collections import Counter
from urllib.parse import unquote, urlsplit
from lxml import html
import json
import subprocess

root = Path(__file__).resolve().parents[1]
node = 'C:/Users/KruJames/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
source = (root / 'index.html').read_text(encoding='utf-8')
doc = html.fromstring(source)
baseline = html.fromstring(subprocess.check_output(['git', 'show', 'HEAD:index.html'], cwd=root).decode('utf-8'))
expected_sections = baseline.xpath('//section/@id')
if 'student-evidence' not in expected_sections and 'student-evidence' in doc.xpath('//section/@id'):
    expected_sections.insert(expected_sections.index('gallery'), 'student-evidence')
assert doc.xpath('//section/@id') == expected_sections, 'Latest section order changed'
assert not [key for key, count in Counter(doc.xpath('//@id')).items() if count > 1], 'Duplicate IDs'
blocks = doc.xpath('//div[@class="score-comparison-wrapper"]')
assert len(blocks) == 1
results = blocks[0]
assert not results.xpath('.//img'), 'Unverified before/after photo'
assert len(results.xpath('.//tbody/tr')) == 4
assert len(results.xpath('.//button[@aria-pressed]')) == 3
assert 'ผ่านเกณฑ์ดี' not in results.text_content()
assert '13.2' not in results.text_content()
assert not doc.xpath('//section[@id="slides"]'), 'Removed slide embed restored'
assert len(doc.xpath('//iframe[contains(@src,"tiktok")]')) == len(baseline.xpath('//iframe[contains(@src,"tiktok")]'))
missing = []
for element in doc.xpath('//img[@src] | //script[@src] | //link[@rel="stylesheet"]'):
    src = element.get('src') or element.get('href')
    if not src:
        continue
    parts = urlsplit(src)
    if not parts.scheme and not parts.netloc and not (root / unquote(parts.path).lstrip('/')).is_file():
        missing.append(src)
assert not missing, f'Missing local assets: {missing}'
for script in doc.xpath('//script[not(@src)]'):
    subprocess.run([node, '-e', 'new (require("node:vm").Script)(require("node:fs").readFileSync(0,"utf8"));'], input=script.text or '', text=True, encoding='utf-8', check=True, capture_output=True)
assert (root / 'index.html').read_bytes() == (root / 'website/index.html').read_bytes()
print(json.dumps({'sections_preserved':len(doc.xpath('//section')), 'lesson_rows':4, 'inline_scripts':'passed', 'local_assets':'passed', 'mirror':'matched'}, indent=2))
