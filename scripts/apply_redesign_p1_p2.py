# -*- coding: utf-8 -*-
import re

with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Substituir font-dudu no body por tipografia executiva sans-serif
# O body tem: class="flex min-h-full flex-col font-dudu relative bg-canvas text-ink transition-colors duration-300"
html = re.sub(r'class="([^"]*)font-dudu([^"]*)"', r'class="\1font-sans antialiased\2"', html)

# 2. Injetar import de fontes executivas no <head> se não estiver completo
# Plus Jakarta Sans, Outfit, JetBrains Mono
fonts_link = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style id="elysian-redesign-styles">
  :root {
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    --font-display: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    --font-mono: 'JetBrains Mono', monospace !important;
  }
  body {
    font-family: var(--font-sans) !important;
    letter-spacing: -0.011em;
  }
  h1, h2, h3, .elysian-headline {
    font-family: var(--font-display) !important;
    letter-spacing: -0.03em;
  }
  .tabular-nums {
    font-variant-numeric: tabular-nums;
    font-family: var(--font-mono);
  }
  /* Polimento Tátil de Interação */
  button, .btn-action, a[href^="#"], a[href^="http"] {
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }
  button:active, .btn-action:active {
    transform: scale(0.98) translateY(1px);
  }
  button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 2px !important;
  }
  /* Estilização limpa para substituição de imagens de fundo rasgadas */
  .clean-paper-surface {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.05), 0 0 1px rgba(0,0,0,0.1) !important;
    border-radius: 12px !important;
  }
  .dark .clean-paper-surface {
    background: rgba(24, 24, 27, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.3) !important;
  }
  /* Ajuste no Hero Logo da Elysian */
  .elysian-brand-mark {
    font-family: var(--font-display);
    font-weight: 800;
    letter-spacing: -0.04em;
    font-size: 1.5rem;
    color: currentColor;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .elysian-brand-badge {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(0,0,0,0.06);
  }
  .dark .elysian-brand-badge {
    background: rgba(255,255,255,0.1);
  }
</style>'''

if 'id="elysian-redesign-styles"' not in html:
    html = html.replace('</head>', f'{fonts_link}\n</head>')

# 3. Substituir Footer residual da Aori por Footer oficial da Elysian
novo_footer = '''<footer class="w-full border-t border-rule bg-canvas px-5 pt-16 pb-10 sm:px-[3vw] sm:pt-20">
  <div class="grid grid-cols-1 gap-x-[4vw] gap-y-12 sm:grid-cols-12 max-w-7xl mx-auto">
    <div class="sm:col-span-5">
      <div class="elysian-brand-mark">
        <span>ELYSIAN</span>
        <span class="elysian-brand-badge">ETRS v3.0</span>
      </div>
      <p class="mt-4 max-w-[36ch] text-[0.92rem] leading-relaxed text-ink-soft">
        Engenharia de sistemas de receita turnkey. Projetamos, implantamos e sustentamos infraestruturas que transformam sinais operacionais em receita líquida mensurável para B2C e B2G.
      </p>
      <div class="mt-6 flex flex-wrap items-center gap-4 text-xs font-mono text-ink-faint">
        <span class="inline-flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span> Sistema Ativo & Monitorado</span>
        <span>•</span>
        <span>Latência &lt; 250ms</span>
      </div>
    </div>
    <nav aria-label="Navegação Institucional" class="sm:col-span-3">
      <p class="text-[0.72rem] tracking-[0.28em] text-ink-faint uppercase font-mono">Arquitetura</p>
      <ul class="mt-5 space-y-3">
        <li><a class="text-[0.92rem] text-ink-soft transition-colors hover:text-ink font-medium" href="#capitulo-01">01. O Problema Invisível</a></li>
        <li><a class="text-[0.92rem] text-ink-soft transition-colors hover:text-ink font-medium" href="#capitulo-02">02. Da Fragmentação ao Sinal</a></li>
        <li><a class="text-[0.92rem] text-ink-soft transition-colors hover:text-ink font-medium" href="#capitulo-03">03. O Sistema ETRS</a></li>
        <li><a class="text-[0.92rem] text-ink-soft transition-colors hover:text-ink font-medium" href="#capitulo-05">04. Verticais B2C & B2G</a></li>
        <li><a class="text-[0.92rem] text-ink-soft transition-colors hover:text-ink font-medium" href="#diagnostico">05. Solicitar Diagnóstico</a></li>
      </ul>
    </nav>
    <div class="sm:col-span-4">
      <p class="text-[0.72rem] tracking-[0.28em] text-ink-faint uppercase font-mono">Contato Direto</p>
      <p class="mt-5 max-w-[32ch] text-[0.92rem] leading-relaxed text-ink-soft">
        Pronto para avaliar os vazamentos da sua esteira comercial? Inicie uma avaliação sem compromisso com nossa engenharia.
      </p>
      <div class="mt-6 flex flex-col gap-3">
        <a class="inline-flex items-center gap-2 text-[0.82rem] tracking-wider text-ink font-semibold uppercase underline decoration-accent decoration-2 underline-offset-4 hover:opacity-80 transition-opacity" href="mailto:contato@elysianconsult.com.br">
          contato@elysianconsult.com.br
        </a>
        <a class="inline-flex items-center gap-2 text-[0.78rem] tracking-wider text-ink-faint hover:text-ink transition-colors font-mono uppercase" href="#diagnostico">
          → Solicitar Diagnóstico ETRS
        </a>
      </div>
    </div>
  </div>
  <div class="mt-16 max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-x-6 gap-y-3 border-t border-rule pt-6 text-[0.72rem] tracking-[0.12em] text-ink-faint uppercase font-mono">
    <span>© 2026 Elysian Consultoria Empresarial Ltda. Todos os direitos reservados.</span>
    <div class="flex items-center gap-6">
      <a class="hover:text-ink transition-colors" href="/privacidade.md">Privacidade</a>
      <a class="hover:text-ink transition-colors" href="/termos.md">Termos</a>
      <a class="hover:text-ink transition-colors" href="/llms.txt">llms.txt</a>
    </div>
  </div>
</footer>'''

html = re.sub(r'<footer class="w-full border-t border-rule bg-canvas.*?</footer>', novo_footer, html, flags=re.DOTALL)

# 4. Substituir a imagem da logo quebrada da Aori no Header/Nav por texto/marca vetorial Elysian
# Procurar imagem com alt="aoricreative"
html = re.sub(
    r'<img[^>]*alt="aoricreative"[^>]*>',
    r'<span class="font-extrabold text-lg tracking-tight font-sans text-ink">ELYSIAN <span class="text-xs font-mono font-normal opacity-60">ETRS</span></span>',
    html
)

# 5. Salvar o arquivo
with open(r'c:\Projetos\MadLabAurora\Elysian Consult\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Também sincronizar com aori_transplanted_landing.html
with open(r'c:\Projetos\MadLabAurora\Elysian Consult\aori_transplanted_landing.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Redesign P1 e P2 aplicado com sucesso!")
