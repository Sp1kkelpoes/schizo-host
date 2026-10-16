#!/usr/bin/env python3
"""Append buttons for every ELF in payloads/ while retaining upstream tiles."""
from pathlib import Path
import json,re
p=Path('payloads.js')
if not p.exists(): raise SystemExit('Missing upstream payloads.js. Run setup.ps1 first.')
s=p.read_text(encoding='utf-8')
start='/* SCHIZO AUTO START */'; end='/* SCHIZO AUTO END */'
s=re.sub(re.escape(start)+r'.*?'+re.escape(end), '', s, flags=re.S)
entries=[]
for path in sorted(Path('payloads').glob('*.elf')):
    filename=path.name
    # existing upstream names are preserved, avoiding duplicate buttons
    if json.dumps(filename) in s or ('"name": "'+filename+'"') in s: continue
    entries.append(dict(title=path.stem,description='Custom ELF payload',name=filename,info=filename,key='custom-'+re.sub('[^a-z0-9-]','-',path.stem.lower())))
if entries:
    s+='\n'+start+'\nwindow.PAYLOAD_TILES = (window.PAYLOAD_TILES || []).concat('+json.dumps(entries,ensure_ascii=False)+');\n'+end+'\n'
p.write_text(s,encoding='utf-8')
print('Custom buttons:',', '.join(x['title'] for x in entries) or '(none new)')
