#!/usr/bin/env python3
"""Validate the public skill package without requiring external dependencies."""
from pathlib import Path
import re, sys
root = Path(__file__).resolve().parents[1]
errors=[]
for name in ('qiuhan-read-paper','yuanjie-write-paper'):
    skill=root/'.agents'/'skills'/name
    if not (skill/'SKILL.md').is_file(): errors.append(f'{name}: missing SKILL.md')
    if not (skill/'agents'/'openai.yaml').is_file(): errors.append(f'{name}: missing agents/openai.yaml')
    for f in skill.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', f.read_text()):
            if '://' in link or link.startswith('#'): continue
            target=link.split('#',1)[0].strip('<>')
            if not (f.parent/target).exists(): errors.append(f'{f.relative_to(root)}: broken link {link}')
    if any('sources' in p.relative_to(skill).parts for p in skill.rglob('*') if p.is_file()):
        errors.append(f'{name}: private sources directory unexpectedly present')
    if any(p.suffix.lower() in {'.pdf','.pptx','.docx','.zip','.mp3','.wav','.png','.jpg','.jpeg'} for p in skill.rglob('*') if p.is_file()):
        errors.append(f'{name}: private media unexpectedly present')
for required in ('README.md','LICENSE','NOTICE.md','scripts/install.py'):
    if not (root/required).is_file(): errors.append(f'missing {required}')
print({'status':'PASS' if not errors else 'FAIL','errors':errors})
sys.exit(bool(errors))
