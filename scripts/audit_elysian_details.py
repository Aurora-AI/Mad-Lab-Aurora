with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['aoricreative', 'wa.me', 'facebook', 'instagram', '85263844473', 'chicle', 'faracohand']):
        print(f"L{i+1}: {line.strip()[:120]}")
