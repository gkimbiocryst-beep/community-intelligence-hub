from textblob import TextBlob


# ======================
# THEME CLASSIFIER
# ======================

def classify_theme(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance",
        "copay",
        "coverage",
        "prior auth",
        "refill"
    ]):
        return "Insurance & Access"

    elif any(word in text for word in [
        "diagnosed",
        "diagnosis",
        "doctor",
        "genetic testing"
    ]):
        return "Diagnosis Journey"

    elif any(word in text for word in [
        "nausea",
        "side effect",
        "medication",
        "treatment"
    ]):
        return "Treatment Experience"

    elif any(word in text for word in [
        "daughter",
        "caregiver",
        "family"
    ]):
        return "Caregiver Burden"

    else:
        return "General Discussion"


# ======================
# SENTIMENT
# ======================

def get_sentiment(text):

    score = TextBlob(
        str(text)
    ).sentiment.polarity

    if score > 0.1:
        return "Positive"

    elif score < -0.1:
        return "Negative"

    else:
        return "Neutral"


# ======================
# UNMET NEEDS
# ======================

def classify_unmet_need(text):

