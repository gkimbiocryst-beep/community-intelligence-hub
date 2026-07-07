import streamlit as st
import pandas as pd

# PAGE SETUP
st.set_page_config(
    page_title="Social Media Listening Hub",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
df = pd.read_csv("sample_posts.csv")

hae = df[df["disease"] == "HAE"]
ns = df[df["disease"] == "Netherton Syndrome"]

# HEADER
st.title("Social Media Listening & Community Intelligence Hub")

st.caption(
    "Transforming patient conversations into actionable patient engagement insights"
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.markdown("## Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Conversations",
    len(df)
)

col2.metric(
    "HAE",
    len(hae)
)

col3.metric(
    "Netherton Syndrome",
    len(ns)
)

col4.metric(
    "Platforms",
    df["platform"].nunique()
)

st.markdown("---")

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs(
    ["HAE", "Netherton Syndrome"]
)

# =====================================================
# HAE TAB
# =====================================================

with tab1:

    st.header("HAE Community Insights")

    left, right = st.columns([1, 2])

    with left:

        st.metric(
            "Conversations",
            len(hae)
        )

        st.info("""
Primary Theme

Insurance & Access

Unmet Need

Access Barriers
""")

    with right:

        st.subheader("Conversation Sources")

        st.bar_chart(
            hae["platform"].value_counts()
        )

    st.markdown("### Key Insight")

    st.write(
        """
HAE conversations frequently discuss insurance approvals,
prior authorization challenges, and treatment access barriers.
"""
    )

    st.markdown("### Recommended Actions")

    st.markdown("""
- Improve reimbursement education resources
- Expand patient support information
- Develop access-focused engagement initiatives
""")

# =====================================================
# NETHERTON TAB
# =====================================================

with tab2:

    st.header("Netherton Syndrome Community Insights")

    left, right = st.columns([1, 2])

    with left:

        st.metric(
            "Conversations",
            len(ns)
        )

        st.info("""
Primary Theme

Diagnosis Journey

Unmet Need

Healthcare System Friction
""")

    with right:

        st.subheader("Conversation Sources")

        st.bar_chart(
            ns["platform"].value_counts()
        )

    st.markdown("### Key Insight")

    st.write(
        """
Netherton Syndrome conversations frequently discuss delayed
diagnosis, difficulties finding knowledgeable providers,
and caregiver burden.
"""
    )

    st.markdown("### Recommended Actions")

    st.markdown("""
- Support diagnosis awareness initiatives
- Develop educational materials
- Expand caregiver support resources
""")

# =====================================================
# OVERALL OPPORTUNITIES
# =====================================================

st.markdown("---")

st.header("Patient Engagement Opportunities")

st.success("""
Key areas where patient engagement initiatives may create value:

• Access and reimbursement support

• Disease education

• Diagnosis awareness

• Caregiver support

• Community storytelling and peer support
""")

