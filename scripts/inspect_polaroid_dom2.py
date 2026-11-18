with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = re.findall(r'<figure[^>]*nb-polaroid[^>]*>.*?</figure>', c, re.DOTALL)
print("Figures encontradas:", len(matches))
for m in matches:
    print(m)
