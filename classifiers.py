def classify_theme(text):

    text = str(text).lower()

    # ACCESS & REIMBURSEMENT
    if any(word in text for word in [
        "insurance",
        "copay",
        "coverage",
        "prior auth",
        "prior authorization",
        "approval",
        "refill",
        "access",
        "cost",
        "denied"
    ]):
        return "Access & Reimbursement"

    # DIAGNOSIS JOURNEY
    elif any(word in text for word in [
        "diagnosis",
        "diagnosed",
        "genetic testing",
        "doctor",
        "doctors",
        "allergies",
        "misdiagnosed",
        "years before diagnosis"
    ]):
        return "Diagnosis Journey"

    # TREATMENT LIMITATIONS / SIDE EFFECTS
    elif any(word in text for word in [
        "nausea",
        "stomach",
        "side effect",
        "side effects",
        "reaction",
        "rough",
        "pain",
        "fatigue",
        "itch",
        "burning"
    ]):
        return "Treatment Limitations"

    # TREATMENT EXPERIENCE
    elif any(word in text for word in [
        "orladeyo",
        "pill",
        "daily pill",
        "treatment",
        "medication",
        "prophylaxis",
        "attacks",
        "swelling",
        "attack-free",
        "emergency kit"
    ]):
        return "Treatment Experience"

    # CAREGIVER BURDEN
    elif any(word in text for word in [
        "daughter",
        "son",
        "caregiver",
        "family",
        "parent",
        "mother",
        "father",
        "future"
    ]):
        return "Caregiver Burden"

    # DISEASE EDUCATION
    elif any(word in text for word in [
        "awareness",
        "explaining",
        "what is",
        "rare disease day",
        "education",
        "condition"
    ]):
        return "Disease Education"

    else:
        return "Other"

def get_recommendations(unmet_need):

    recommendations = {

        "Access Barriers": [
            "Provide reimbursement education resources",
            "Include navigation content in patient events",
            "Develop access-focused patient support materials"
        ],

        "Healthcare System Friction": [
            "Develop diagnosis journey resources",
            "Support disease awareness initiatives",
            "Create healthcare provider education materials"
        ],

        "Emotional Burden": [
            "Expand caregiver support programming",
            "Facilitate peer-to-peer storytelling",
            "Create emotional wellness resources"
        ],

        "Treatment Limitations": [
            "Gather patient treatment experience feedback",
            "Develop expectation-setting content",
            "Explore unmet treatment burden themes"
        ]
    }

    return recommendations.get(
        unmet_need,
        ["Further review needed"]
    )
