import streamlit as st
import pandas as pd

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="PE Translator",
    page_icon="🎯",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("sample_posts.csv")

# =====================================================
# THEME CLASSIFIER
# =====================================================

def classify_theme(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance","coverage","approval",
        "copay","denied","refill"
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


# =====================================================
# UNMET NEED CLASSIFIER
# =====================================================

def classify_unmet_need(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance","coverage",
        "approval","copay","denied"
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


# =====================================================
# SENTIMENT CLASSIFIER
# =====================================================

def classify_sentiment(text):

    text = str(text).lower()

    negative_words = [
        "denied",
        "delay",
        "delayed",
        "frustrated",
        "difficult",
        "pain",
        "issue",
        "problem",
        "struggling",
        "rough",
        "fatigue",
        "burning",
        "itch",
        "nausea",
        "reaction",
        "misdiagnosed"
    ]

    positive_words = [
        "better",
        "improved",
        "effective",
        "great",
        "helpful",
        "successful",
        "supportive",
        "relieved",
        "controlled",
        "attack-free"
    ]

    if any(word in text for word in negative_words):
        return "Negative"

    elif any(word in text for word in positive_words):
        return "Positive"

    else:
        return "Neutral"


# =====================================================
# OPPORTUNITIES
# =====================================================

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


# =====================================================
# RECOMMENDATIONS
# =====================================================

def get_recommendations(unmet_need):

    recommendations = {

        "Access Barriers": [
            "Provide reimbursement education resources",
            "Create access-focused support materials",
            "Address common insurance questions"
        ],

        "Healthcare System Friction": [
            "Increase disease awareness initiatives",
            "Develop diagnosis journey resources",
            "Create provider education materials"
        ],

        "Emotional Burden": [
            "Expand caregiver support programming",
            "Create community storytelling opportunities",
            "Support peer-to-peer engagement"
        ],

        "Treatment Limitations": [
            "Gather patient treatment feedback",
            "Develop expectation-setting resources",
            "Address treatment burden concerns"
        ]
    }

    return recommendations.get(
        unmet_need,
        ["Further review needed"]
    )


# =====================================================
# CREATE COLUMNS
# =====================================================

df["theme"] = df["text"].apply(classify_theme)
df["unmet_need"] = df["text"].apply(classify_unmet_need)
df["sentiment"] = df["text"].apply(classify_sentiment)

# =====================================================
# PAGE HEADER
# =====================================================

st.title("🎯 Patient Engagement Translator")

st.caption(
    "Transforms social listening insights into actionable patient engagement opportunities"
)

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs(
    ["HAE", "Netherton Syndrome"]
)

for disease, tab in zip(
    ["HAE", "Netherton Syndrome"],
    [tab1, tab2]
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

        if len(themes) == 0:
            st.warning("No themes identified.")
            continue

        if len(needs) == 0:
            st.warning("No unmet needs identified.")
            continue

        top_theme = themes.idxmax()
        top_need = needs.idxmax()

        opportunity = get_opportunity(top_need)

        recommendations = get_recommendations(top_need)

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
The dominant conversation theme is **{top_theme}**.

The leading unmet need is **{top_need}**.

This suggests a patient engagement opportunity focused on **{opportunity}**.
"""
        )

        st.markdown("### **Recommended Actions**")

        for item in recommendations:
            st.write(f"• {item}")

        # =====================================================
        # PRIORITY RANKING
        # =====================================================

        st.markdown("---")
        st.markdown("## 🚨 Theme Priority Ranking")

        priority_rows = []

        for theme_name, count in themes.items():

            negative_posts = len(
                disease_df[
                    (disease_df["theme"] == theme_name)
                    &
                    (disease_df["sentiment"] == "Negative")
                ]
            )

            priority_score = count + (negative_posts * 2)

            if priority_score >= 12:
                priority = "🔴 High"
            elif priority_score >= 6:
                priority = "🟡 Medium"
            else:
                priority = "🟢 Opportunity"

            priority_rows.append({
                "Theme": theme_name,
                "Mentions": count,
                "Negative Posts": negative_posts,
                "Priority Score": priority_score,
                "Priority": priority
            })

        priority_df = pd.DataFrame(priority_rows)

        priority_df = priority_df.sort_values(
            by="Priority Score",
            ascending=False
        )

        priority_df.insert(
            0,
            "Rank",
            range(1, len(priority_df) + 1)
        )

        st.dataframe(
            priority_df,
            use_container_width=True,
            hide_index=True
        )
