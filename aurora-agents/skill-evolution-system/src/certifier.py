def certify(scoring, validation):
    """
    Certifies a skill with a level ('certified', 'validated', or 'draft') 
    based on the rubric score and test validation results.
    """
    # Extract score from the scoring dictionary
    score = scoring.get("score", 0)
    pass_rate = validation.get("pass_rate", 0.0)

    if score >= 85 and pass_rate >= 0.85:
        return "certified"
    elif score >= 70 and pass_rate >= 0.70:
        return "validated"
    else:
        return "draft"
