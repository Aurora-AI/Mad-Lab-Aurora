with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
idx = c.find('85263844473')
if idx != -1:
    print('Trecho ao redor do WhatsApp:')
    print(c[idx-200:idx+300])

idx2 = c.find('aoricreative')
if idx2 != -1:
    print('\nTrecho ao redor de aoricreative:')
    print(c[idx2-200:idx2+300])
