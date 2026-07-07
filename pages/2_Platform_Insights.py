import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="Platform Insights",
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

st.title("🌐 Platform Insights")

st.caption(
    "Understand how conversations differ across platforms and therapeutic areas"
)

# =====================================================
# PLATFORM VOLUME CHART
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
# TABS
# =====================================================

tab1, tab2 = st.tabs([
    "HAE",
    "Netherton Syndrome"
])

# =====================================================
# HAE TAB
# =====================================================

with tab1:

    st.header("HAE Platform Insights")

    rows = []

    hae_df = df[
        df["disease"] == "HAE"
    ]

    for platform in sorted(
        hae_df["platform"].unique()
    ):

        platform_df = hae_df[
            hae_df["platform"] == platform
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

        rows.append({
            "Platform": platform,
            "Posts": len(platform_df),
            "Top Theme": top_theme,
            "Top Unmet Need": top_need,
            "PE Opportunity":
                get_opportunity(top_need)
        })

    summary_df = pd.DataFrame(rows)

    st.dataframe(
        summary_df,
        use_container_width=True
    )

# =====================================================
# NETHERTON TAB
# =====================================================

with tab2:

    st.header(
        "Netherton Syndrome Platform Insights"
    )

    rows = []

    ns_df = df[
        df["disease"] == "Netherton Syndrome"
    ]

    for platform in sorted(
        ns_df["platform"].unique()
    ):

        platform_df = ns_df[
            ns_df["platform"] == platform
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

        rows.append({
            "Platform": platform,
            "Posts": len(platform_df),
            "Top Theme": top_theme,
            "Top Unmet Need": top_need,
            "PE Opportunity":
                get_opportunity(top_need)
        })

    summary_df = pd.DataFrame(rows)

    st.dataframe(
        summary_df,
        use_container_width=True
    )
