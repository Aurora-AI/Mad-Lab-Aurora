with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = re.findall(r'(https?://[^\s"\'<>]*aoricreative[^\s"\'<>]*)', c, re.IGNORECASE)
print('Ocorrências aoricreative:', set(matches))
wa = re.findall(r'(https?://wa\.me[^\s"\'<>]*)', c, re.IGNORECASE)
print('Ocorrências WhatsApp:', set(wa))
