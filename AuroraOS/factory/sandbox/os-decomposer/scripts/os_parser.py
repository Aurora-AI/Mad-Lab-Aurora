import re
from pathlib import Path
from typing import List, Dict

class OSParser:
    """Parser para extrair passos de execução de arquivos OS em Markdown."""
    
    def __init__(self, content: str):
        self.content = content
    
    def extract_steps(self) -> List[Dict[str, str]]:
        """Extrai os passos da seção 'Passos de Execução'."""
        steps = []
        
        # Divide o documento em seções de nível 2 (##)
        sections = re.split(r"\n(?=## [^#])", "\n" + self.content)
        
        section_content = ""
        for section in sections:
            header_match = re.match(r"## (Passos de Execução|Plano de Reparo)", section.strip(), re.I)
            if header_match:
                section_content = section
                break
        
        if not section_content:
            # Tenta encontrar no documento inteiro como último recurso
            section_content = self.content
            
        # Regex para capturar passos (ex: ### Passo 1 — [Título])
        step_pattern = re.compile(r"### (Passo \d+ — .*?)\n(.*?)(?=### Passo \d+ — |$)", re.S)
        matches = step_pattern.findall(section_content)
        
        for title, body in matches:
            steps.append({
                "title": title.strip(),
                "content": body.strip()
            })
            
        # Fallback: Se não achar com cabeçalhos ###, tenta buscar listas numeradas ou itens de checklist
        if not steps:
            # Procura especificamente por checklists dentro da seção de execução se identificada
            list_pattern = re.compile(r"^- \[ \] (.*?)$", re.M)
            list_matches = list_pattern.findall(section_content)
            for i, match in enumerate(list_matches, 1):
                steps.append({
                    "title": f"Passo {i}",
                    "content": match.strip()
                })
                
        return steps

def parse_os_file(path: Path) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    parser = OSParser(content)
    return parser.extract_steps()
