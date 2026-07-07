def classify_theme(text):

    text = str(text).lower()

    # Access
    if any(word in text for word in [
        "insurance","copay","coverage",
        "prior auth","approval","cost"
    ]):
        return "Access & Reimbursement"

    # Diagnosis
    elif any(word in text for word in [
        "diagnosis","diagnosed",
        "doctor","allergies",
        "genetic testing"
    ]):
        return "Diagnosis Journey"

    # Treatment
    elif any(word in text for word in [
        "orladeyo",
        "pill",
        "treatment",
        "medication",
        "prophylaxis"
    ]):
        return "Treatment Experience"

    # Side effects
    elif any(word in text for word in [
        "nausea",
        "side effect",
        "stomach issues",
        "reaction"
    ]):
        return "Treatment Limitations"

    # Caregiver
    elif any(word in text for word in [
        "daughter",
        "caregiver",
        "family",
        "parent"
    ]):
        return "Caregiver Burden"

    # Education
    elif any(word in text for word in [
        "awareness",
        "explaining",
        "what is",
        "learn"
    ]):
        return "Disease Education"

    else:
        return "Other"
``
