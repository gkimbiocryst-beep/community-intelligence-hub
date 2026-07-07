import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PE Translator",
    page_icon="🎯",
    layout="wide"
)

df = pd.read_csv("sample_posts.csv")

# ==========================================
# SAME CLASSIFICATION LOGIC AS DASHBOARD
# ==========================================

def classify_theme(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance","coverage",
        "approval","copay",
        "denied","refill"
    ]):
        return "Access & Reimbursement"

    elif any(word in text for word in [
        "diagnosis","diagnosed",
        "doctor","genetic testing"
    ]):
        return "Diagnosis Journey"

    elif any(word in text for word in [
        "nausea","side effect",
        "reaction","stomach"
    ]):
        return "Treatment Limitations"

    elif any(word in text for word in [
        "orladeyo","treatment",
        "medication","attacks"
    ]):
        return "Treatment Experience"

    elif any(word in text for word in [
        "daughter","caregiver",
        "family","parent"
    ]):
        return "Caregiver Burden"

    else:
        return "Other"


def classify_unmet_need(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance","coverage",
        "approval","copay"
    ]):
        return "Access Barriers"

    elif any(word in text for word in [
        "diagnosis","diagnosed",
        "doctor","genetic testing"
    ]):
        return "Healthcare System Friction"

    elif any(word in text for word in [
        "daughter","caregiver",
        "family","parent"
    ]):
        return "Emotional Burden"

    elif any(word in text for word in [
        "nausea","side effect",
        "stomach","reaction"
    ]):
        return "Treatment Limitations"

    else:
        return "Further Review Needed"


def get_opportunity(unmet_need):

    mapping = {
        "Access Barriers":
            "Access Support & Navigation",

        "Healthcare System Friction":
            "Diagnosis Awareness",

        "Emotional Burden":
            "Caregiver Support",

        "Treatment Limitations":
            "Treatment Education"
    }

    return mapping.get(
        unmet_need,
        "Further Review Needed"
    )


df["theme"] = df["text"].apply(classify_theme)
df["unmet_need"] = df["text"].apply(classify_unmet_need)

st.title("🎯 Patient Engagement Translator")

st.caption(
    "Transforms social listening insights into actionable patient engagement opportunities"
)

tabs = st.tabs([
    "HAE",
    "Netherton Syndrome"
])

for disease, tab in zip(
    ["HAE", "Netherton Syndrome"],
    tabs
):

    with tab:

        disease_df = df[
            df["disease"] == disease
        ]

        themes = (
            disease_df[
                ~disease_df["theme"].isin(["Other"])
            ]["theme"]
            .value_counts()
        )

        needs = (
            disease_df[
                ~disease_df["unmet_need"].isin([
                    "Further Review Needed"
                ])
            ]["unmet_need"]
            .value_counts()
        )

        top_theme = themes.idxmax()

        top_need = needs.idxmax()

        opportunity = get_opportunity(
            top_need
        )

        st.markdown(f"""
### **Top Theme**
**{top_theme}**

### **Top Unmet Need**
**{top_need}**

### **Patient Engagement Opportunity**
**{opportunity}**
""")

        st.info(
            f"""
Based on current social listening activity,
the most prominent discussion area is
'{top_theme}', which is associated with
the unmet need '{top_need}'.
            """
        )

        st.success("""
Recommended Actions

• Develop targeted educational resources

• Identify patient storytelling opportunities

• Explore future engagement programming

• Monitor discussion trends over time
        """)
