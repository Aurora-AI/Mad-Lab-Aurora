import re
import yaml

def parse_frontmatter(content):
    """
    Parses frontmatter from markdown. Falls back to manual key-value parsing if yaml fails.
    """
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not frontmatter_match:
        return {}
    
    yaml_text = frontmatter_match.group(1)
    try:
        return yaml.safe_load(yaml_text) or {}
    except Exception:
        # Fallback manual parsing for basic key-value pairs
        metadata = {}
        for line in yaml_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip().strip("'\"")
                v = v.strip().strip("'\"")
                # Handle lists in fallback
                if v.startswith("[") and v.endswith("]"):
                    v = [item.strip().strip("'\"") for item in v[1:-1].split(",")]
                metadata[k] = v
        return metadata

def analyze(skill_content):
    """
    Analyzes a skill in markdown format, extracting structural and metadata features.
    """
    if not skill_content:
        return {
            "name": "unknown",
            "frontmatter": {},
            "headings": [],
            "references": [],
            "triggers": [],
            "has_anchor_cases": False,
            "has_templates": False
        }

    frontmatter = parse_frontmatter(skill_content)
    
    # Extract headings (e.g. ## Modos de Operação)
    headings = re.findall(r"^#+\s+(.+)$", skill_content, re.MULTILINE)
    headings = [h.strip() for h in headings]
    
    # Extract trigger keywords
    triggers = []
    # Search in frontmatter
    if "trigger" in frontmatter:
        triggers.append(str(frontmatter["trigger"]))
    # Search in headings or body
    trigger_section_match = re.search(r"##\s*(?:Gatilhos|Triggers).*?\n(.*?)(?=\n##|$)", skill_content, re.DOTALL | re.IGNORECASE)
    if trigger_section_match:
        trigger_text = trigger_section_match.group(1)
        # Extract bullet points
        bullets = re.findall(r"-\s*(.+)$", trigger_text, re.MULTILINE)
        triggers.extend(bullets)

    # Extract references to files/directories (e.g., references/ founder-dna.md or file://)
    references = []
    # Match markdown links to files: [label](file:///...) or [label](references/...)
    file_links = re.findall(r"\[.*?\]\(((?:file:///|references/|docs/).*?)\)", skill_content)
    references.extend(file_links)
    
    # Also look for references mentioned in text or comments
    ref_mentions = re.findall(r"(?:references|docs)/[a-zA-Z0-9_\-\./]+", skill_content)
    references.extend(ref_mentions)
    
    # Deduplicate and clean paths (remove anchors #L10 etc.)
    cleaned_refs = []
    for ref in references:
        # Clean file:// and remove fragment identifiers
        clean = ref.replace("file:///", "").split("#")[0].strip()
        if clean and clean not in cleaned_refs:
            cleaned_refs.append(clean)

    # Check for cases and templates
    has_anchor_cases = any(re.search(r"caso[\s\-]+âncora|anchor[\s\-]+case", h, re.IGNORECASE) for h in headings) or \
                       bool(re.search(r"caso[\s\-]+âncora|anchor[\s\-]+case", skill_content, re.IGNORECASE))
                       
    has_templates = any(re.search(r"template|modelo|formato", h, re.IGNORECASE) for h in headings) or \
                    bool(re.search(r"template\s+de|modelo\s+de|format:\s*\w+", skill_content, re.IGNORECASE))

    return {
        "name": frontmatter.get("name", "unknown"),
        "frontmatter": frontmatter,
        "headings": headings,
        "references": cleaned_refs,
        "triggers": triggers,
        "has_anchor_cases": has_anchor_cases,
        "has_templates": has_templates,
        "content_length": len(skill_content)
    }
