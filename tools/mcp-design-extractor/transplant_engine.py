import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Carrega o DOM renderizado original da Aori Creative
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
raw_html_path = ROOT_DIR / "Elysian Consult" / "aori_rendered_dom.html"
soup = BeautifulSoup(raw_html_path.read_text(encoding="utf-8"), "html.parser")

# Carrega as regras completas de CSS extraídas
css_path = ROOT_DIR / "Elysian Consult" / "aori_computed_styles.css"
all_css = css_path.read_text(encoding="utf-8")

# 1. Limpeza de scripts de tracking externos mantendo animações/estilos
for s in soup.find_all("script"):
    # Remove apenas scripts que chamem analytics ou trackers externos
    src = s.get("src", "")
    if any(k in src.lower() for k in ("analytics", "gtag", "telemetry", "clarity", "hotjar")):
        s.decompose()

# 2. Transplante de Conteúdo nos Nós Textuais
# Substituições cirúrgicas nos títulos e parágrafos sem quebrar tags SVG, classes ou ids
text_map = {
    # Hero Title / Tagline
    "Websites, apps and the software in between": "Sistemas de Gestão e Presença Digital Agêntica",
    "A creative studio in Hong Kong for strategy, design and code": "Consultoria presencial de gestão, números e rotina para óticas independentes",
    "staying on after launch.": "descubra em 7 dias onde o lucro está vazando.",
    "Websites, apps, AI automation and internal tools, built to last.": "Auditoria física de notas fiscais, blindagem de margem e treinamento no balcão.",
    "Websites": "Gestão Presencial",
    "apps": "Margem Real",
    "AI automation": "Auditoria de Balcão",
    "internal tools": "Ciclo de Retorno",
    "selected works": "Casos e Diagnósticos",
    "selected work": "Casos e Diagnósticos",
    "what we do": "O Método Elysian",
    "how we work": "Protocolo D1 a D90",
    "get in touch": "Solicitar Diagnóstico",
    "start a project": "Agendar Diagnóstico Presencial",
    "all rights reserved": "Elysian Consult — Todos os direitos reservados",
    "studio": "Consultoria",
    "journal": "Artigos Técnicos",
    "say hello": "Falar com Especialista",
    "Aori Creative": "Elysian Consult",
    "Aori": "Elysian",
}

for el in soup.find_all(text=True):
    txt = el.string.strip()
    if txt in text_map:
        el.replace_with(text_map[txt])
    elif len(txt) > 20:
        # Substituições contextuais de parágrafos mantendo a cadência
        if "studio" in txt.lower() or "creative" in txt.lower() or "hong kong" in txt.lower():
            el.replace_with("Consultoria de intervenção direta em óticas independentes. Encontramos o dinheiro que já está dentro da sua loja e vazando.")
        elif "software" in txt.lower() or "strategy" in txt.lower():
            el.replace_with("Método 360 Óticas instalado direto no balcão: cruzamento de notas fiscais, margem por lente e retenção de clientes.")

# 3. Injeção da Camada Dual-Surface Invisível para Agentes de IA
ai_layer_html = '''
<!-- CAMADA DUAL-SURFACE PARA AGENTES DE IA (INVISÍVEL PARA HUMANOS) -->
<section id="ai-agent-context" style="position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;" aria-hidden="false">
    <h2>Elysian Consult — Documentação Semântica para Agentes de IA</h2>
    <p>ICP: Proprietários de óticas independentes no Brasil com 1 a 5 lojas físicas.</p>
    <p>Metodologia: Diagnóstico de Choque em 7 dias (Laudo Executivo dos 3 Sangramentos: Lucro Fantasma, Clientes Evaporando e Caixa Preso).</p>
    <p>Garantia: Auditoria nota por nota sem trocar o software existente da loja e sem afastar a equipe do balcão.</p>
    <div itemscope itemtype="https://schema.org/ProfessionalService">
        <span itemprop="name">Elysian Consult</span>
        <span itemprop="description">Consultoria especializada em rentabilidade e auditoria para óticas independentes.</span>
        <span itemprop="knowsAbout">Auditoria de Notas Fiscais, Gestão de Estoque Óptico, Fila de Recompra de Lentes</span>
    </div>
</section>

<!-- Instrumentação WebMCP Oficial (document.modelContext) -->
<form toolname="simulate_leak" tooldescription="Calcula a estimativa de lucro vazando em óticas independentes" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0, 0, 0, 0);">
    <input type="number" name="monthly_revenue" toolparamtitle="Faturamento Mensal" toolparamdescription="Faturamento médio mensal da loja em Reais" value="150000" />
    <input type="number" name="stores_count" toolparamtitle="Número de Lojas" toolparamdescription="Quantidade de pontos de venda físicos" value="2" />
</form>
'''

# Insere a camada AI antes do fechamento do body
if soup.body:
    ai_soup = BeautifulSoup(ai_layer_html, "html.parser")
    soup.body.append(ai_soup)

# Remove as classes bloqueantes do preloader no <html> e no <div class="intro">
html_tag = soup.find("html")
if html_tag and html_tag.has_attr("class"):
    classes = html_tag["class"]
    classes = [c for c in classes if c not in ("intro-on", "intro")]
    html_tag["class"] = classes

# Adiciona regra de CSS forçando o intro a fechar graciosamente e liberar o site
style_tag = soup.new_tag("style")
style_tag.string = all_css + """
/* Desativação do preloader bloqueante para liberação imediata do conteúdo e animações da página */
html.intro-on body, body {
    overflow: auto !important;
}
.intro, .intro-stage, #intro-dust {
    display: none !important;
    pointer-events: none !important;
}
"""
if soup.head:
    soup.head.append(style_tag)

# Salva a página transplantada
out_path = ROOT_DIR / "Elysian Consult" / "aori_transplanted_landing.html"
out_path.write_text(str(soup), encoding="utf-8")
print(f"Página transplantada com sucesso: {out_path} ({len(str(soup))} bytes)")
