def extract_patterns(benchmark_analyses):
    """
    Extracts structural design patterns and quality baselines from a list of benchmark analyses.
    """
    if not benchmark_analyses:
        return {
            "required_frontmatter_keys": ["name", "version", "description", "domain"],
            "expected_headings": ["Referenciais Cognitivos", "Modos de Operação", "Referências"],
            "target_modes_count": 2,
            "min_content_length": 1000
        }

    # Find frontmatter keys that are present in most benchmarks
    all_keys = {}
    for analysis in benchmark_analyses:
        for key in analysis.get("frontmatter", {}).keys():
            all_keys[key] = all_keys.get(key, 0) + 1
            
    required_frontmatter_keys = [k for k, count in all_keys.items() if count >= len(benchmark_analyses) / 2]
    # Ensure baseline keys
    for k in ["name", "version", "description", "domain"]:
        if k not in required_frontmatter_keys:
            required_frontmatter_keys.append(k)

    # Find headings that commonly appear
    all_headings = {}
    for analysis in benchmark_analyses:
        for heading in analysis.get("headings", []):
            # Normalize heading to find common patterns
            norm = heading.lower().strip()
            # Group similar headings
            if "referencial" in norm or "cognitivo" in norm:
                key = "Referenciais Cognitivos"
            elif "modo" in norm or "operação" in norm:
                key = "Modos de Operação"
            elif "referência" in norm:
                key = "Referências"
            elif "tom de voz" in norm or "personalidade" in norm:
                key = "Tom de Voz"
            elif "saída" in norm or "output" in norm:
                key = "Formato de Saída"
            elif "âncora" in norm or "caso" in norm:
                key = "Caso Âncora"
            else:
                key = heading
            all_headings[key] = all_headings.get(key, 0) + 1

    # Keep headings appearing in at least one benchmark as a guideline, but prioritize common ones
    expected_headings = [h for h, count in all_headings.items() if count >= max(1, len(benchmark_analyses) / 3)]

    # Calculate average content length for baseline
    total_len = sum(a.get("content_length", 0) for a in benchmark_analyses)
    avg_len = total_len / len(benchmark_analyses) if benchmark_analyses else 2000

    return {
        "required_frontmatter_keys": required_frontmatter_keys,
        "expected_headings": expected_headings,
        "target_modes_count": 3,
        "min_content_length": int(avg_len * 0.6)  # at least 60% of average benchmark size
    }
