with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '85263844473' in line or 'aoricreative' in line:
        print(f"L{i+1}: {line.strip()[:160]}")
