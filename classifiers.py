def classify_theme(text):

    text = str(text).lower()

    # ACCESS
    if any(word in text for word in [
        "insurance",
        "copay",
        "coverage",
        "prior auth",
        "approval",
        "refill",
        "access"
    ]):
        return "Access & Reimbursement"

    # DIAGNOSIS
    elif any(word in text for word in [
        "diagnosis",
        "diagnosed",
        "genetic testing",
        "doctor",
        "allergies",
        "misdiagnosed"
    ]):
        return "Diagnosis Journey"

    # SIDE EFFECTS
    elif any(word in text for word in [
        "nausea",
        "stomach",
        "side effect",
        "reaction"
    ]):
        return "Treatment Limitations"

    # TREATMENT EXPERIENCE
    elif any(word in text for word in [
        "orladeyo",
        "pill",
        "treatment",
        "medication",
        "prophylaxis",
        "attacks"
    ]):
        return "Treatment Experience"

    # CAREGIVER
    elif any(word in text for word in [
        "daughter",
        "caregiver",
        "family",
        "parent"
    ]):
        return "Caregiver Burden"

    # EDUCATION
    elif any(word in text for word in [
        "awareness",
        "explaining",
        "what is",
        "rare disease day"
    ]):
        return "Disease Education"

    else:
        return "Other"
