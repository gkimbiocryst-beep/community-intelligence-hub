import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Platform Insights",
    page_icon="🌐",
    layout="wide"
)

df = pd.read_csv("sample_posts.csv")

# =====================================================
# SAME CLASSIFIER AS DASHBOARD
# =====================================================

def classify_theme(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance","copay","coverage",
        "approval","refill","denied"
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
        "reaction","stomach"
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

# =====================================================
# CLASSIFY DATA
# =====================================================

df["theme"] = df["text"].apply(classify_theme)
df["unmet_need"] = df["text"].apply(classify_unmet_need)

# =====================================================
# PAGE
# =====================================================

st.title("🌐 Platform Intelligence")

st.caption(
    "Understand how conversations differ across social media platforms"
)

# =====================================================
# VOLUME CHART
# =====================================================

st.subheader("Conversation Volume by Platform")

platform_counts = (
    df["platform"]
    .value_counts()
)

st.bar_chart(platform_counts)

# =====================================================
# SELECT PLATFORM
# =====================================================

platform = st.selectbox(
    "Select Platform",
    sorted(df["platform"].unique())
)

platform_df = df[
    df["platform"] == platform
]

# =====================================================
# CALCULATE INSIGHTS
# =====================================================

themes = (
    platform_df[
        ~platform_df["theme"].isin(["Other"])
    ]["theme"]
    .value_counts()
)

needs = (
    platform_df[
        ~platform_df["unmet_need"].isin([
            "Further Review Needed"
        ])
    ]["unmet_need"]
    .value_counts()
)

if len(themes) > 0:
    top_theme = themes.idxmax()
else:
    top_theme = "No Theme Identified"

if len(needs) > 0:
    top_need = needs.idxmax()
else:
    top_need = "No Unmet Need Identified"

opportunity = get_opportunity(top_need)

# =====================================================
# INSIGHT CARDS
# =====================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Top Theme",
    top_theme
)

c2.metric(
    "Top Unmet Need",
    top_need
)

c3.metric(
    "PE Opportunity",
    opportunity
)

# =====================================================
# DONUT CHART
# =====================================================

st.subheader("Theme Distribution")

if len(themes) > 0:

    chart_df = themes.reset_index()

    chart_df.columns = [
        "Theme",
        "Count"
    ]

    fig = px.pie(
        chart_df,
        names="Theme",
        values="Count",
        hole=.60
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# DISEASE BREAKDOWN
# =====================================================

st.subheader("Disease Breakdown")

st.bar_chart(
    platform_df["disease"].value_counts()
)

# =====================================================
# SAMPLE POSTS
# =====================================================

st.subheader("Example Conversations")

st.dataframe(
    platform_df[
        ["disease","text"]
    ].head(5)
)
