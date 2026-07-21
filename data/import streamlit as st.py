import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Performance Analytics Dashboard")

# Load data
df = pd.read_excel("data/students.xlsx")

# Clean data
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
df = df.dropna(how="all")

# Calculate average score
df["Average"] = df[["MATHS", "ENGLISH", "SCIENCES"]].mean(axis=1)

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Students", len(df))

with col2:
    st.metric("Average Score", round(df["Average"].mean(), 1))

with col3:
    st.metric("Highest Score", round(df["Average"].max(), 1))

st.divider()

st.subheader("Student Records")
st.dataframe(df)