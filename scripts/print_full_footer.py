with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
footer_match = re.search(r'<footer[^>]*>.*?</footer>', c, re.DOTALL)
if footer_match:
    print(footer_match.group(0))
