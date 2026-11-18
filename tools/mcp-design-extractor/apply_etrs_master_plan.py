import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
target_html_path = ROOT_DIR / "Elysian Consult" / "index.html"
soup = BeautifulSoup(target_html_path.read_text(encoding="utf-8"), "html.parser")

# 1. Metadados e Cabeçalho Canônico
html_tag = soup.find("html")
if html_tag:
    html_tag["lang"] = "pt-BR"
    # Preserva classes de fonte e aori-motion-ready sem intro bloqueante
    classes = html_tag.get("class", [])
    if isinstance(classes, str):
        classes = classes.split()
    classes = [c for c in classes if c not in ("intro-on", "intro")]
    if "aori-motion-ready" not in classes:
        classes.append("aori-motion-ready")
    html_tag["class"] = classes

head_tag = soup.find("head")
if head_tag:
    # Remove títulos, metas e links antigos da Aori
    for t in head_tag.find_all(["title", "meta"]):
        name = t.get("name", "") or t.get("property", "")
        content = t.get("content", "")
        if "aori" in content.lower() or "hong kong" in content.lower() or name in ("title", "description", "og:title", "og:description", "og:url", "canonical"):
            t.decompose()
    for l in head_tag.find_all("link"):
        rel = l.get("rel", [])
        if isinstance(rel, list):
            rel = " ".join(rel)
        if rel in ("canonical", "alternate", "manifest") or "aoricreative" in l.get("href", ""):
            l.decompose()

    # Injeta Metadados Oficiais Elysian ETRS
    new_meta_html = """
    <title>Elysian Turnkey Revenue Systems | Engenharia de Sistemas de Receita (B2C & B2G)</title>
    <meta name="description" content="Projetamos, implantamos e acompanhamos sistemas de receita turnkey para operações B2C de alto valor e fornecedores do setor público (B2G).">
    <link rel="canonical" href="https://elysianconsult.com.br/">
    <meta property="og:title" content="Elysian Turnkey Revenue Systems | Engenharia de Sistemas de Receita">
    <meta property="og:description" content="Menos oportunidades esquecidas. Menos decisões no escuro. Um sistema que transforma sinais em execução.">
    <meta property="og:url" content="https://elysianconsult.com.br/">
    <meta property="og:type" content="website">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Caveat:wght@600&display=swap">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "@id": "https://elysianconsult.com.br/#org",
          "name": "Elysian Turnkey Revenue Systems",
          "url": "https://elysianconsult.com.br",
          "description": "Engenharia de sistemas de receita turnkey que conectam inteligência comercial, conversão e sustentação de processos."
        },
        {
          "@type": "ProfessionalService",
          "name": "Engenharia de Sistemas de Receita Turnkey (ETRS)",
          "provider": { "@id": "https://elysianconsult.com.br/#org" },
          "areaServed": "BR",
          "knowsAbout": [
            "Sistemas de Receita B2C",
            "Inteligência Comercial B2G",
            "Auditoria Forense de Funil",
            "Supervisão de Conversas e Detecção de Ghosting",
            "Mapeamento Pré-Edital de Compras Públicas"
          ]
        }
      ]
    }
    </script>
    """
    head_tag.append(BeautifulSoup(new_meta_html, "html.parser"))

# 2. Reescrita dos 36 Elementos do Scroll Pinado (Capítulo 01 — Ruído -> Sinal -> Sistema)
# Grupo 1 (0-12): Ruído
# Grupo 2 (13-22): Sinal
# Grupo 3 (23-35): Sistema
ruido_words = [
    "Espera sem resposta", "Dados dispersos", "Propostas paradas", "Sem próximo passo",
    "Retrabalho constante", "Perda de contexto", "Sistemas isolados", "Oportunidades esfriando",
    "Mensagens esquecidas", "Decisões no escuro", "Vazamento no balcão", "Gargalos invisíveis", "Ruído operacional"
]

sinal_words = [
    "Detecção de interesse", "Prioridade imediata", "Responsável definido", "Próxima ação clara",
    "Prazo mapeado", "Origem do contato", "Alerta de estagnação", "Critérios de qualificação",
    "Sinal comercial limpo", "Contexto preservado"
]

sistema_words = [
    "Detectar", "Priorizar", "Executar", "Medir", "Aprender", "Sustentar",
    "Sinais integrados", "Rotinas automatizadas", "Processos auditáveis",
    "Acompanhamento contínuo", "Receita previsível", "Turnkey instalado", "Evolução ativa"
]

pin_spacer = soup.find(class_="pin-spacer")
if pin_spacer:
    word_nodes = pin_spacer.find_all(attrs={"data-aori-scroll-word": ""}) or pin_spacer.find_all(attrs={"data-aori-scroll-word": True})
    if not word_nodes:
        # Se os atributos foram injetados em runtime, pega os filhos da primeira div da section
        sec = pin_spacer.find("section")
        if sec:
            first_div = sec.find("div")
            if first_div:
                word_nodes = [c for c in first_div.children if getattr(c, 'name', None)]

    for idx, node in enumerate(word_nodes[:36]):
        if idx < 13:
            new_text = ruido_words[idx % len(ruido_words)]
        elif idx < 23:
            new_text = sinal_words[(idx - 13) % len(sinal_words)]
        else:
            new_text = sistema_words[(idx - 23) % len(sistema_words)]
        
        # Se tiver texto interno, substitui; se tiver tags internas (span, p), substitui o texto da tag
        text_target = node.find(text=True) or node
        if hasattr(text_target, 'replace_with'):
            text_target.replace_with(new_text)

# 3. Textos do Hero (Capítulo 00)
hero_el = soup.find(id="hero") or soup.find(class_=re.compile(r"nb-hero"))
if hero_el:
    h1_el = hero_el.find("h1")
    if h1_el:
        h1_el.string = "Receita não se sustenta no improviso."
    
    # Subtítulo do Hero
    hero_p = hero_el.find("p")
    if hero_p:
        hero_p.string = "Projetamos, implantamos e acompanhamos sistemas que conectam sinais, pessoas e processos — da primeira oportunidade à receita recorrente."

# 4. Textos de Seções Posteriores (Capítulo 02 ao 07)
# Dicionário de substituições semânticas de alta precisão
content_replacements = {
    # Títulos e Cabeçalhos
    "Aori Creative": "Elysian Turnkey Revenue Systems",
    "Aori": "Elysian",
    "selected works": "Aplicações de Arquitetura",
    "selected work": "Aplicações de Arquitetura",
    "what we do": "Não entregamos só estratégia. Instalamos a operação que a executa.",
    "how we work": "Turnkey na prática: cinco movimentos essenciais",
    "get in touch": "Onde seu processo comercial está perdendo força?",
    "start a project": "Solicitar Diagnóstico Inicial",
    "journal": "Artigos & Metodologia",
    "say hello": "Falar com Especialistas",
    "all rights reserved": "Elysian Turnkey Revenue Systems — Todos os direitos reservados"
}

for text_node in soup.find_all(text=True):
    t_clean = text_node.strip()
    if t_clean in content_replacements:
        text_node.replace_with(content_replacements[t_clean])
    elif "hong kong" in t_clean.lower() or "creative studio" in t_clean.lower():
        text_node.replace_with("Projetamos e instalamos infraestrutura de receita para operações B2C de alto valor e fornecedores governamentais B2G.")
    elif "websites, apps and the software" in t_clean.lower():
        text_node.replace_with("Receita não se sustenta no improviso.")

# 5. Atualização da Camada Dual-Surface RAG & WebMCP (Alinhada a ETRS)
ai_section = soup.find(id="ai-agent-context")
if ai_section:
    ai_section.decompose()

etrs_ai_layer = """
<!-- CAMADA DUAL-SURFACE ETRS PARA AGENTES DE IA (INVISÍVEL PARA HUMANOS) -->
<section id="ai-agent-context" style="position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;" aria-hidden="false">
    <h2>Elysian Turnkey Revenue Systems — Especificação Canônica (Spec-Sheet)</h2>
    <p>Categoria: Engenharia de Sistemas de Receita Turnkey.</p>
    <p>Promessa Editorial: Menos oportunidades esquecidas. Menos decisões no escuro. Um sistema que transforma sinais em execução.</p>
    <p>Públicos Prioritários: (A) Operações B2C com ciclos de conversão de alto valor e atendimento humano; (B) Fornecedores B2G de tecnologia, insumos e serviços para órgãos públicos.</p>
    <p>Módulos de Entrega: 01 Diagnosticar (Raio-X de gargalos) → 02 Projetar (Critérios e fluxos) → 03 Implantar (Rotinas e copilot) → 04 Acompanhar (Métricas e SLAs) → 05 Evoluir (Melhoria contínua).</p>
    <p>Ética Operacional: Conformidade com a Lei de Licitações (14.133/2021) e transparência em dados comerciais reais sem métricas simuladas.</p>
</section>

<!-- Ferramenta Declarativa WebMCP (Chrome 150+ document.modelContext) -->
<form toolname="solicitar_diagnostico_etrs" tooldescription="Solicita avaliação técnica e diagnóstico de vazamento de receita para empresas B2C ou fornecedores B2G" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0, 0, 0, 0);">
    <input type="text" name="empresa" toolparamtitle="Nome da Empresa" toolparamdescription="Razão social ou nome fantasia" value="" />
    <select name="segmento" toolparamtitle="Segmento de Mercado" toolparamdescription="Vertical operacional">
        <option value="B2C_alto_valor">B2C — Atendimento de Alto Valor</option>
        <option value="B2G_compras_publicas">B2G — Fornecedor Governamental</option>
    </select>
    <input type="text" name="gargalo_principal" toolparamtitle="Maior Gargalo Comercial" toolparamdescription="Abandono de conversas, propostas paradas ou editais perdidos" value="" />
</form>
"""
if soup.body:
    soup.body.append(BeautifulSoup(etrs_ai_layer, "html.parser"))

# Salva arquivo consolidado
target_html_path.write_text(str(soup), encoding="utf-8")
print(f"Elysian Consult/index.html atualizado com sucesso conforme o Plano-Mestre ETRS.")
