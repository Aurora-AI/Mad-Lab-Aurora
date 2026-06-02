try:
    from src.analyzer import analyze
    from src.extractor import extract_patterns
    from src.compiler import compile_skill
    from src.validator import validate
    from src.scorer import score
    from src.certifier import certify
except ImportError:
    from analyzer import analyze
    from extractor import extract_patterns
    from compiler import compile_skill
    from validator import validate
    from scorer import score
    from certifier import certify

def run_pipeline(skill, benchmarks, test_cases):
    analysis_A = analyze(skill)
    analysis_B = [analyze(b) for b in benchmarks]

    patterns = extract_patterns(analysis_B)

    evolved = compile_skill(skill, patterns)

    validation = validate(evolved, test_cases)

    scoring = score(evolved)

    certification = certify(scoring, validation)

    return {
        "original_analysis": analysis_A,
        "patterns": patterns,
        "evolved_skill": evolved,
        "validation": validation,
        "score": scoring,
        "certification": certification
    }
