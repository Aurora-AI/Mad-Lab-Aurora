with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('nb-polaroid-hold')
if idx != -1:
    print(c[idx-1200:idx+400])
