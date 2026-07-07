import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Platform Intelligence",
    page_icon="🌐",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("sample_posts.csv")

# =====================================================
# CLASSIFIERS
# =====================================================

def classify_theme(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance","copay","coverage",
        "approval","denied","refill"
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

    elif any(word in text for word in [
        "awareness",
        "education",
        "rare disease day"
    ]):
        return "Disease Education"

    else:
        return "Other"


def classify_unmet_need(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance",
        "coverage",
        "approval",
        "copay",
        "denied"
    ]):
        return "Access Barriers"

    elif any(word in text for word in [
        "diagnosis",
        "diagnosed",
        "doctor",
        "genetic testing"
    ]):
        return "Healthcare System Friction"

    elif any(word in text for word in [
        "daughter",
        "caregiver",
        "family",
        "parent"
    ]):
        return "Emotional Burden"

    elif any(word in text for word in [
        "nausea",
        "side effect",
        "reaction",
        "stomach"
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
# CREATE COLUMNS
# =====================================================

df["theme"] = df["text"].apply(classify_theme)
df["unmet_need"] = df["text"].apply(classify_unmet_need)

# =====================================================
# HEADER
# =====================================================

st.title("🌐 Platform Intelligence")

st.caption(
    "Understand how conversations differ across social media platforms"
)

# =====================================================
# CONVERSATION VOLUME
# =====================================================

st.subheader("Conversation Volume by Platform")

platform_counts = (
    df["platform"]
    .value_counts()
    .reset_index()
)

platform_counts.columns = [
    "Platform",
    "Posts"
]

fig = px.bar(
    platform_counts,
    x="Platform",
    y="Posts",
    text="Posts",
    color="Posts"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# PLATFORM INTELLIGENCE TABLE
# =====================================================

rows = []

for platform in sorted(df["platform"].unique()):

    platform_df = df[
        df["platform"] == platform
    ]

    themes = (
        platform_df[
            ~platform_df["theme"].isin([
                "Other"
            ])
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

    top_theme = (
        themes.idxmax()
        if len(themes) > 0
        else "N/A"
    )

    top_need = (
        needs.idxmax()
        if len(needs) > 0
        else "N/A"
    )

    opportunity = get_opportunity(
        top_need
    )

    rows.append({

        "Platform": platform,

        "Posts": len(platform_df),

        "Top Theme": top_theme,

        "Top Unmet Need": top_need,

        "PE Opportunity": opportunity

    })

platform_summary = pd.DataFrame(rows)

st.subheader("Platform Intelligence Summary")

st.dataframe(
    platform_summary,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# PLATFORM DEEP DIVE
# =====================================================

selected_platform = st.selectbox(
    "Select Platform for Deep Dive",
    sorted(df["platform"].unique())
)

platform_df = df[
    df["platform"] == selected_platform
]

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

top_theme = (
    themes.idxmax()
    if len(themes) > 0
    else "N/A"
)

top_need = (
    needs.idxmax()
    if len(needs) > 0
    else "N/A"
)

opportunity = get_opportunity(
    top_need
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Top Theme",
    top_theme
)

col2.metric(
    "Top Unmet Need",
    top_need
)

col3.metric(
    "PE Opportunity",
    opportunity
)

st.info(
    f"""
On **{selected_platform}**, the dominant discussion theme is
**{top_theme}**.

The leading unmet need identified is
**{top_need}**.

This suggests a patient engagement opportunity focused on
**{opportunity}**.
"""
)

# =====================================================
# DONUT CHART
# =====================================================

if len(themes) > 0:

    chart_df = themes.reset_index()

    chart_df.columns = [
        "Theme",
        "Count"
    ]

    fig = px.pie(
        chart_df,
        values="Count",
        names="Theme",
        hole=0.60,
        title=f"{selected_platform} Theme Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
