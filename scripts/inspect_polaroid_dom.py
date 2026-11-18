with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
idx = c.find('nb-polaroid-hold')
idx_figure = c.rfind('<figure', 0, idx)
idx_figure_end = c.find('</figure>', idx)
print(c[idx_figure:idx_figure_end+9])
