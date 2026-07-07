import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Social Media Listening Hub",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
df = pd.read_csv("sample_posts.csv")

# SPLIT BY DISEASE
hae = df[df["disease"] == "HAE"]
ns = df[df["disease"] == "Netherton Syndrome"]

# HEADER
st.title("Social Media Listening & Community Intelligence Hub")
st.caption(
    "Transforming patient conversations into actionable patient engagement insights"
)

# EXECUTIVE SUMMARY
st.markdown("## Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Conversations", len(df))
col2.metric("HAE Conversations", len(hae))
col3.metric("Netherton Conversations", len(ns))
col4.metric("Platforms", df["platform"].nunique())

st.markdown("---")

# =====================
# HAE SECTION
# =====================

st.header("HAE Community Insights")

col1, col2 = st.columns([1, 2])

with col1:

    st.metric("Conversations", len(hae))

    st.info("""
    **Priority Area**

    Insurance & Access

    **Unmet Need**

    Access Barriers
    """)

with col2:

    platform_counts = hae["platform"].value_counts()

    st.subheader("Conversation Sources")

    st.bar_chart(platform_counts)

st.markdown("""
### Key Insight

HAE conversations frequently discuss insurance approvals,
prior authorizations, and treatment access challenges.

### Recommended Actions

- Improve reimbursement education resources
- Expand patient support information
- Develop access-focused engagement initiatives
""")

st.markdown("---")

# =====================
# NETHERTON SECTION
# =====================

st.header("Netherton Syndrome Community Insights")

col1, col2 = st.columns([1, 2])

with col1:

    st.metric("Conversations", len(ns))

    st.info("""
    **Priority Area**

    Diagnosis Journey

    **Unmet Need**

    Healthcare System Friction
    """)

with col2:

    platform_counts = ns["platform"].value_counts()

    st.subheader("Conversation Sources")

    st.bar_chart(platform_counts)

st.markdown("""
### Key Insight

Netherton Syndrome conversations often focus on delayed
diagnosis, limited disease awareness, and caregiver burden.

### Recommended Actions

- Support diagnosis awareness initiatives
- Develop educational materials
- Enhance caregiver support resources
""")

st.markdown("---")

# STRATEGIC OPPORTUNITIES

st.header("Patient Engagement Opportunities")

st.success("""
Key areas where patient engagement efforts may create value:

• Access and reimbursement support

• Disease education

• Diagnosis awareness

• Caregiver support initiatives

• Community storytelling and peer support
""")

