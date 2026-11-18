import re

with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('Tamanho do HTML:', len(c))

urls = set(re.findall(r'https?://[^\s"\'<>]+', c))
print('Total URLs externas:', len(urls))
for u in sorted(urls):
    if 'schema.org' not in u and 'w3.org' not in u and 'elysianconsult' not in u:
        print('  EXT:', u)

imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', c)
print('Total de <img>:', len(imgs))
for img in imgs[:10]:
    print('  IMG src:', img)

videos = re.findall(r'<video[^>]+src=["\']([^"\']+)["\']', c)
print('Total de <video>:', len(videos))
for v in videos[:10]:
    print('  VIDEO src:', v)

fonts = set(re.findall(r'font-family:\s*([^;\}]+)', c))
print('Font-families declaradas:', len(fonts))
for ft in list(fonts)[:10]:
    print('  FONT:', ft.strip())
