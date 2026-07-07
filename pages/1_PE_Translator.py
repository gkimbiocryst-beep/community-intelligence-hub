import streamlit as st
import pandas as pd

st.title("Patient Engagement Translator")

df = pd.read_csv("sample_posts.csv")

st.write(
    "Translating patient conversations into engagement opportunities."
)

theme_counts = (
    df["disease"]
    .value_counts()
)

st.subheader("Conversation Summary")

for disease, count in theme_counts.items():

    st.write(
        f"• {disease}: {count} posts"
    )

st.markdown("---")

st.subheader("Example Insight")

st.info(
    """
    Theme: Insurance / Access

    Unmet Need: Access Barriers

    Recommendation:
    Improve patient access resources and reimbursement education.
    """
)
