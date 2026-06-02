try:
    from src.analyzer import analyze
except ImportError:
    from analyzer import analyze

def validate(skill_content, test_cases):
    """
    Validates the evolved skill markdown against a set of checklist items and test cases.
    """
    if not skill_content:
        return {"valid": False, "pass_rate": 0.0, "details": ["Conteúdo vazio"]}

    analysis = analyze(skill_content)
    passed = 0
    details = []

    # 1. Structural checklist validation
    if len(analysis.get("headings", [])) >= 3:
        passed += 1
        details.append("Checklist: Possui 3 ou mais seções/cabeçalhos (Pass)")
    else:
        details.append("Checklist: Faltam seções mínimas no documento (Fail)")

    if analysis.get("has_templates", False):
        passed += 1
        details.append("Checklist: Possui templates/modelos de output definidos (Pass)")
    else:
        details.append("Checklist: Faltam templates/modelos de output (Fail)")

    # 2. Test cases validation
    for i, case in enumerate(test_cases):
        expected_props = case.get("expected_properties", [])
        case_passed = True
        
        for prop in expected_props:
            # Check if property is satisfied
            if prop == "determinism" and len(analysis.get("triggers", [])) == 0:
                case_passed = False
            elif prop == "structure" and not analysis.get("has_templates", False):
                case_passed = False
            elif prop == "references" and len(analysis.get("references", [])) == 0:
                case_passed = False
            elif prop == "modes" and len(analysis.get("headings", [])) < 3:
                case_passed = False

        if case_passed:
            passed += 1
            details.append(f"Caso de Teste {i+1}: Satisfez propriedades {expected_props} (Pass)")
        else:
            details.append(f"Caso de Teste {i+1}: Falhou nas propriedades {expected_props} (Fail)")

    total_checks = 2 + len(test_cases)
    pass_rate = passed / total_checks if total_checks else 0.0

    return {
        "valid": pass_rate >= 0.80,
        "pass_rate": pass_rate,
        "details": details
    }
