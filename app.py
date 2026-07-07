import streamlit as st
import pandas as pd
import plotly.express as px

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
        "misdiagnosed"
    ]):
        return "Diagnosis Journey"

    # TREATMENT LIMITATIONS
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
        "father"
    ]):
        return "Caregiver Burden"

    # EDUCATION
    elif any(word in text for word in [
        "awareness",
        "explaining",
        "what is",
        "rare disease day",
        "education"
    ]):
        return "Disease Education"

    else:
        return "Other"

# =====================================================
# UNMET NEED CLASSIFIER
# =====================================================

def classify_unmet_need(text):

    text = str(text).lower()

    if any(word in text for word in [
        "insurance",
        "copay",
        "coverage",
        "prior auth",
        "approval",
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
        "stomach",
        "side effect",
        "reaction"
    ]):
        return "Treatment Limitations"

    else:
        return "Education Gap"

# =====================================================
# CREATE CLASSIFICATION COLUMNS
# =====================================================

df["theme"] = df["text"].apply(classify_theme)
df["unmet_need"] = df["text"].apply(classify_unmet_need)

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

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Conversations", len(df))
c2.metric("HAE", len(hae))
c3.metric("Netherton Syndrome", len(ns))
c4.metric("Platforms", df["platform"].nunique())

st.markdown("---")

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs(["HAE", "Netherton Syndrome"])

# =====================================================
# HAE
# =====================================================

with tab1:

    hae_themes = (
        hae[hae["theme"] != "Other"]
        ["theme"]
        .value_counts()
    )

    hae_top_theme = hae_themes.idxmax()

    hae_top_need = (
        hae["unmet_need"]
        .value_counts()
        .idxmax()
    )

    hae_opportunity = get_opportunity(
        hae_top_need
    )

    st.header("HAE Community Insights")

    left, right = st.columns([1, 2])

    with left:

        st.metric("Conversations", len(hae))

        st.markdown(f"""
### **Top Theme**
**{hae_top_theme}**

### **Top Unmet Need**
**{hae_top_need}**
""")

        st.success(f"""
### **Patient Engagement Opportunity**
**{hae_opportunity}**
""")

    with right:

        chart_df = hae_themes.reset_index()
        chart_df.columns = ["Theme", "Count"]

        fig = px.pie(
            chart_df,
            values="Count",
            names="Theme",
            hole=0.6,
            title="Theme Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Conversation Sources")

    st.bar_chart(
        hae["platform"].value_counts()
    )

# =====================================================
# NETHERTON
# =====================================================

with tab2:

    ns_themes = (
        ns[ns["theme"] != "Other"]
        ["theme"]
        .value_counts()
    )

    ns_top_theme = ns_themes.idxmax()

    ns_top_need = (
        ns["unmet_need"]
        .value_counts()
        .idxmax()
    )

    ns_opportunity = get_opportunity(
        ns_top_need
    )

    st.header("Netherton Syndrome Community Insights")

    left, right = st.columns([1, 2])

    with left:

        st.metric("Conversations", len(ns))

        st.markdown(f"""
### **Top Theme**
**{ns_top_theme}**

### **Top Unmet Need**
**{ns_top_need}**
""")

        st.success(f"""
### **Patient Engagement Opportunity**
**{ns_opportunity}**
""")

    with right:

        chart_df = ns_themes.reset_index()
        chart_df.columns = ["Theme", "Count"]

        fig = px.pie(
            chart_df,
            values="Count",
            names="Theme",
            hole=0.6,
            title="Theme Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Conversation Sources")

    st.bar_chart(
        ns["platform"].value_counts()
    )
