import glob
import re

files = glob.glob('**/*.html', recursive=True)
print(f'Removing client preview switcher bar across {len(files)} HTML files...')

pattern = r'<!-- Version Switcher Preview Bar -->\s*<div style="background-color: #03113B;[\s\S]*?</div>'

count = 0
for f in files:
    content = open(f, encoding='utf-8').read()
    new_content = re.sub(pattern, '', content)
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as out:
            out.write(new_content)
        count += 1
        print(f'Removed preview bar from {f}')

print(f'Done! Removed preview bar from {count} files.')
