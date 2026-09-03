import glob
import re

files = glob.glob('**/*.html', recursive=True)
print(f'Updating mobile sticky CTA bar in {len(files)} HTML files...')

old_pattern = r'<!-- Mobile Sticky Bar -->\s*<div class="mobile-sticky-bar">[\s\S]*?</div>\s*</div>'

new_sticky = """  <!-- Mobile Sticky Bar -->
  <div class="mobile-sticky-bar">
    <div class="mobile-sticky-inner">
      <a href="/contact/#enquire" class="btn btn-pink">Enquire For Dates 🎉</a>
      <a href="/#packages" class="btn btn-white-navy">See Packages 📀</a>
    </div>
  </div>"""

count = 0
for f in files:
    content = open(f, encoding='utf-8').read()
    new_content = re.sub(old_pattern, new_sticky, content)
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as out:
            out.write(new_content)
        count += 1
        print(f'Updated sticky CTA buttons in {f}')

print(f'Done! Updated sticky bar in {count} files.')
