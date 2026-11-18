with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
print("Has font-dudu:", 'font-dudu' in c)
print("Has aoricreative:", 'aoricreative' in c)
print("Has 85263844473:", '85263844473' in c)
print("Occurrences of /_next/image:", c.count('/_next/image'))
print("Occurrences of /images/intro/:", c.count('/images/intro/'))
