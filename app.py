import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_excel("data/students.xlsx")

# Remove empty columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Remove empty rows
df = df.dropna(how="all")

# Calculate Average Score
df["Average"] = df[["MATHS", "ENGLISH", "SCIENCES"]].mean(axis=1)

# ----------------------------
# DASHBOARD TITLE
# ----------------------------
st.title("🎓 Student Performance Analytics Dashboard")
st.markdown("Analyze student academic performance using interactive charts and KPIs.")

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Dashboard Filters")

selected_class = st.sidebar.selectbox(
    "Select Class",
    ["All"] + sorted(df["CLASS"].unique())
)

selected_gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(df["GENDER"].unique())
)

# Apply filters
filtered_df = df.copy()

if selected_class != "All":
    filtered_df = filtered_df[filtered_df["CLASS"] == selected_class]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["GENDER"] == selected_gender]

# ----------------------------
# KPI CARDS
# ----------------------------
total_students = len(filtered_df)
average_score = filtered_df["Average"].mean()
highest_score = filtered_df["Average"].max()
top_student = filtered_df.loc[
    filtered_df["Average"].idxmax(), "NAME"
]

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Students", total_students)
col2.metric("📊 Average Score", f"{average_score:.1f}")
col3.metric("🏆 Highest Score", f"{highest_score:.1f}")
col4.metric("⭐ Top Student", top_student)

st.divider()

# ----------------------------
# BAR CHART
# ----------------------------
subject_average = pd.DataFrame({
    "Subject": ["Maths", "English", "Sciences"],
    "Average Score": [
        filtered_df["MATHS"].mean(),
        filtered_df["ENGLISH"].mean(),
        filtered_df["SCIENCES"].mean()
    ]
})

fig = px.bar(
    subject_average,
    x="Subject",
    y="Average Score",
    title="Average Score by Subject",
    text_auto=".1f"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# PIE CHART
# ----------------------------
gender_count = filtered_df["GENDER"].value_counts().reset_index()
gender_count.columns = ["Gender", "Students"]

pie = px.pie(
    gender_count,
    names="Gender",
    values="Students",
    title="Gender Distribution"
)

st.plotly_chart(pie, use_container_width=True)

# ----------------------------
# DATA TABLE
# ----------------------------
st.subheader("Student Records")

st.dataframe(filtered_df, use_container_width=True)