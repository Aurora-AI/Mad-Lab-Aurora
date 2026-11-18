# -*- coding: utf-8 -*-
with open(r'c:\Projetos\MadLabAurora\Elysian Consult\hero_seismograph_snippet.html', 'r', encoding='utf-8') as f:
    snippet = f.read()

with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Substituir o interior da figure da polaroid por esse componente sóbrio de sismografia e escuta determinística
target_figure = re.search(r'<figure class="nb-polaroid nb-hero-polaroid".*?</figure>', html, re.DOTALL)
if target_figure:
    old_figure = target_figure.group(0)
    
    new_figure = f'''<figure class="nb-polaroid nb-hero-polaroid" data-dolly-focus="true" style="--nb-sheen:1; width: var(--nb-pw); aspect-ratio: 950 / 1220; isolation: isolate; position: relative; rotate: 2.5deg; container-type: inline-size;">
  <div style="position: absolute; inset: 0; width: 100%; height: 100%; padding: 4%;">
    {snippet}
  </div>
  <figcaption class="nb-polaroid-caption" style="display: none;"></figcaption>
  <a href="#capitulo-01" aria-label="Conhecer o sistema de escuta e receita ETRS" class="nb-polaroid-hold" style="display: block; position: absolute; inset: 0; width: 100%; height: 100%; z-index: 10;"></a>
</figure>'''

    html = html.replace(old_figure, new_figure)
    
    with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    with open(r'c:\Projetos\MadLabAurora\Elysian Consult\aori_transplanted_landing.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Hero atualizado com a sismografia de escuta determinística!")
else:
    print("Figura não encontrada.")
