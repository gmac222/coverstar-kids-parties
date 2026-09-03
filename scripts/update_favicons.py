import glob
import re

files = glob.glob('**/*.html', recursive=True)
print(f'Updating favicon tags across {len(files)} HTML files...')

pattern = r'<link rel="icon"[^>]+>'

new_favicon_tags = """  <link rel="icon" type="image/png" href="/assets/images/favicon.png">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/assets/images/favicon.png">"""

count = 0
for f in files:
    content = open(f, encoding='utf-8').read()
    if 'rel="icon"' in content:
        new_content = re.sub(pattern, new_favicon_tags, content)
    else:
        # Insert before </head> if no icon link exists
        new_content = content.replace('</head>', f'{new_favicon_tags}\n</head>')
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as out:
            out.write(new_content)
        count += 1
        print(f'Updated favicon in {f}')

print(f'Done! Updated favicon across {count} HTML files.')
