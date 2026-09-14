from pathlib import Path
from urllib.parse import unquote
from lxml import html
import subprocess

root = Path(__file__).resolve().parents[1]
doc = html.fromstring((root/'index.html').read_text(encoding='utf-8'))
section = doc.get_element_by_id('downloads')
links = [a.get('href') for a in section.xpath('.//a') if a.get('href','').startswith('assets/docs/')]
assert len(links) == len(set(links)) == 10
assert all((root/unquote(path)).is_file() for path in links)
assert len(section.xpath('.//div[@class="document-group"]')) == 4
assert len(section.xpath('.//details/ul/li')) == 2
ids = doc.xpath('//@id')
assert len(ids) == len(set(ids))
assert (root/'index.html').read_bytes() == (root/'website/index.html').read_bytes()
node = 'C:/Users/KruJames/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
for script in doc.xpath('//script[not(@src)]'):
    subprocess.run([node,'-e','new (require("node:vm").Script)(require("node:fs").readFileSync(0,"utf8"));'],input=script.text or '',text=True,encoding='utf-8',capture_output=True,check=True)
print('Passed: 4 groups, 10 unique files, 2 archived entries, local links, IDs, JavaScript and mirror.')
