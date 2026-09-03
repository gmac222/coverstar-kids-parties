import glob
import re

files = glob.glob('**/*.html', recursive=True)
print(f'Replacing remote logo URLs in {len(files)} files...')

pattern = r'https://www\.coverstarexperiences\.co\.uk/wp-content/uploads/2016/08/[^\"]+\.jpg'

for f in files:
    content = open(f, encoding='utf-8').read()
    new_content = re.sub(pattern, '/assets/images/coverstar-logo.jpg', content)
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as out:
            out.write(new_content)
        print(f'Updated logo path in {f}')

print('All logo image paths updated to local /assets/images/coverstar-logo.jpg!')
