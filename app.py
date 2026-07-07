import streamlit as st
import pandas as pd

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="Social Media Listening Hub",
    page_icon="📊",
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

    if "insurance" in text or "copay" in text:
        return "Insurance & Access"

    elif "diagnosis" in text:
        return "Diagnosis Journey"

    elif "caregiver" in text or "daughter" in text:
        return "Caregiver Burden"

    elif "side effect" in text or "nausea" in text:
        return "Treatment Experience"

    else:
        return "General Discussion"


# =====================================================
# UNMET NEED CLASSIFIER
# =====================================================

def classify_unmet_need(text):

    text = str(text).lower()

    if "insurance" in text or "copay" in text:
        return "Access Barriers"

    elif "diagnosis" in text:
        return "Healthcare System Friction"

    elif "caregiver" in text or "daughter" in text:
        return "Emotional Burden"

    elif "side effect" in text or "nausea" in text:
        return "Treatment Limitations"

    else:
        return "Education Gap"


# CREATE NEW COLUMNS

df["theme"] = df["text"].apply(classify_theme)

df["unmet_need"] = df["text"].apply(classify_unmet_need)


hae = df[df["disease"] == "HAE"]
ns = df[df["disease"] == "Netherton Syndrome"]

# =====================================================
# MAKE SURE THESE COLUMNS EXIST
# =====================================================
# These should already be created by your classifier code

hae = df[df["disease"] == "HAE"]
ns = df[df["disease"] == "Netherton Syndrome"]

# =====================================================
# OPPORTUNITY MAPPING
# =====================================================

def get_opportunity(unmet_need):

    if unmet_need == "Access Barriers":
        return "Access Support & Navigation"

    elif unmet_need == "Healthcare System Friction":
        return "Diagnosis Awareness"

    elif unmet_need == "Emotional Burden":
        return "Caregiver Support"

    elif unmet_need == "Treatment Limitations":
        return "Treatment Education"

    else:
        return "Patient Education"

# =====================================================
# HEADER
# =====================================================

st.title("Social Media Listening & Community Intelligence Hub")

st.caption(
    "Transforming patient conversations into actionable patient engagement insights"
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.markdown("## Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Conversations", len(df))
col2.metric("HAE", len(hae))
col3.metric("Netherton Syndrome", len(ns))
col4.metric("Platforms", df["platform"].nunique())

st.markdown("---")

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs(["HAE", "Netherton Syndrome"])

# =====================================================
# HAE TAB
# =====================================================

with tab1:

    hae_top_theme = hae["theme"].value_counts().idxmax()

    hae_top_need = hae["unmet_need"].value_counts().idxmax()

    hae_opportunity = get_opportunity(hae_top_need)

    st.header("HAE Community Insights")

    left, right = st.columns([1, 2])

    with left:

        st.metric(
            "Conversations",
            len(hae)
        )

        st.info(f"""
Top Theme

{hae_top_theme}

Top Unmet Need

{hae_top_need}
""")

        st.success(f"""
Patient Engagement Opportunity

{hae_opportunity}
""")

    with right:

        st.subheader("Theme Distribution")

        st.bar_chart(
            hae["theme"].value_counts()
        )

    st.markdown("### Conversation Sources")

    st.bar_chart(
        hae["platform"].value_counts()
    )

# =====================================================
# NETHERTON TAB
# =====================================================

with tab2:

    ns_top_theme = ns["theme"].value_counts().idxmax()

    ns_top_need = ns["unmet_need"].value_counts().idxmax()

    ns_opportunity = get_opportunity(ns_top_need)

    st.header("Netherton Syndrome Community Insights")

    left, right = st.columns([1, 2])

    with left:

        st.metric(
            "Conversations",
            len(ns)
        )

        st.info(f"""
Top Theme

{ns_top_theme}

Top Unmet Need

{ns_top_need}
""")

        st.success(f"""
Patient Engagement Opportunity

{ns_opportunity}
""")

    with right:

        st.subheader("Theme Distribution")

        st.bar_chart(
            ns["theme"].value_counts()
        )

    st.markdown("### Conversation Sources")

    st.bar_chart(
        ns["platform"].value_counts()
    )
