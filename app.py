import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Social Media Listening Hub",
    page_icon="📊",
    layout="wide"
)

st.title("Social Media Listening Hub")

try:
    df = pd.read_csv("sample_posts.csv")

    st.success("✅ Data loaded successfully")

    st.write("Preview of your data:")

    st.dataframe(df.head())

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Posts", len(df))

    with col2:
        if "platform" in df.columns:
            st.metric(
                "Platforms",
                df["platform"].nunique()
            )

except Exception as e:

    st.error("Error loading data")
    st.code(str(e))
