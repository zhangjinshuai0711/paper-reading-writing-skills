#!/usr/bin/env python3
"""Install the two bundled skills without overwriting existing folders."""
import argparse
from pathlib import Path
import shutil
import sys

NAMES = ('qiuhan-read-paper', 'yuanjie-write-paper')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project', type=Path, help='Existing project folder')
    group.add_argument('--user', action='store_true', help='Install in ~/.agents/skills')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.project is not None:
        project = args.project.expanduser().resolve()
        if not project.is_dir():
            parser.error('Project folder does not exist: ' + str(project))
        destination = project / '.agents' / 'skills'
    else:
        destination = Path.home() / '.agents' / 'skills'
    sources = [root / '.agents' / 'skills' / name for name in NAMES]
    if any(not (source / 'SKILL.md').is_file() for source in sources):
        parser.error('Skill files are missing; extract the complete repository or release package.')
    conflicts = [destination / name for name in NAMES if (destination / name).exists() or (destination / name).is_symlink()]
    if conflicts:
        print('Stopped without copying. Existing targets:', file=sys.stderr)
        for target in conflicts:
            print(target, file=sys.stderr)
        return 1
    destination.mkdir(parents=True, exist_ok=True)
    for name, source in zip(NAMES, sources):
        shutil.copytree(source, destination / name)
        print('Installed ' + str(destination / name))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
