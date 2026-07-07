import streamlit as st
import pandas as pd

st.title("Patient Engagement Translator")

df = pd.read_csv("sample_posts.csv")

# Split by disease
hae = df[df["disease"] == "HAE"]
ns = df[df["disease"] == "Netherton Syndrome"]

# Create two columns
left, right = st.columns(2)

# --------------------
# HAE
# --------------------
with left:

    st.subheader("HAE")

    st.metric("Posts", len(hae))

    st.markdown("### Top Insight")

    hae_text = " ".join(
        hae["text"].astype(str)
    ).lower()

    if "insurance" in hae_text:
        theme = "Insurance / Access"
        need = "Access Barriers"

        action = """
        - Improve reimbursement education
        - Develop access resources
        - Support navigation programs
        """

    elif "diagnosis" in hae_text:
        theme = "Diagnosis Journey"
        need = "Healthcare System Friction"

        action = """
        - Create diagnosis resources
        - Increase disease awareness
        - Support patient education
        """

    else:
        theme = "Treatment Experience"
        need = "Education Gap"

        action = """
        - Develop educational content
        - Share patient stories
        """

    st.info(f"""
Theme: {theme}

Unmet Need: {need}
""")

    st.markdown("**Recommended Actions**")

    st.markdown(action)

# --------------------
# NETHERTON
# --------------------
with right:

    st.subheader("Netherton Syndrome")

    st.metric("Posts", len(ns))

    st.markdown("### Top Insight")

    ns_text = " ".join(
        ns["text"].astype(str)
    ).lower()

    if "diagnosis" in ns_text:
        theme = "Diagnosis Journey"
        need = "Healthcare System Friction"

        action = """
        - Increase provider awareness
        - Improve diagnosis resources
        - Support educational materials
        """

    elif "caregiver" in ns_text:
        theme = "Caregiver Burden"
        need = "Emotional Burden"

        action = """
        - Expand caregiver resources
        - Develop peer support programs
        - Share lived experiences
        """

    else:
        theme = "Treatment Experience"
        need = "Treatment Limitations"

        action = """
        - Gather treatment feedback
        - Improve educational content
        """

    st.info(f"""
Theme: {theme}

Unmet Need: {need}
""")

    st.markdown("**Recommended Actions**")

    st.markdown(action)
