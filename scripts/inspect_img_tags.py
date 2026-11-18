with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
img_matches = re.findall(r'<img[^>]+>', c)
print(f"Total <img> tags: {len(img_matches)}")
unique_srcs = set(re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', c))
for s in sorted(unique_srcs):
    print("SRC:", s)
