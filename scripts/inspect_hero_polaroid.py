with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
# Procurar "websites" ou a estrutura ao redor da polaroid
idx = c.find('websites')
if idx != -1:
    print("Trecho ao redor de 'websites':")
    print(c[idx-400:idx+400])
else:
    print("'websites' não encontrado.")
