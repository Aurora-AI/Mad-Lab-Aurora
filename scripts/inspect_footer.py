with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# 1. Encontrar o trecho do footer com os links sociais
footer_match = re.search(r'<footer[^>]*>.*?</footer>', c, re.DOTALL)
if footer_match:
    print("FOOTER ENCONTRADO:")
    print(footer_match.group(0)[:800])
else:
    # procurar onde está 85263844473
    idx = c.find('85263844473')
    print("Trecho ao redor do telefone:", c[idx-300:idx+400])
