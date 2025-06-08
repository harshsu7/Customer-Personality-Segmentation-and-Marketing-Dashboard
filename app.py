import streamlit as st
import pandas as pd
import plotly.express as px

# Load Preprocessed Data from EDA Script
@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\NewUser\\OneDrive\\Desktop\\harsh 22315A0070\\Third Year Project\\Datasets\\processed_data.csv")  # Ensure this file is generated from your EDA script
    return df

df = load_data()

# Page Title
st.title(" Customer Segmentation Dashboard")

# Cluster Overview
st.subheader("Cluster Summary")
cluster_summary = df.groupby("Clusters").agg({
    "Income": "mean",
    "Spent": "mean",
    "Customer Loyalty": "mean",
    "NumWebVisitsMonth": "mean"
}).reset_index()
st.dataframe(cluster_summary.style.format({"Income": "${:,.2f}", "Spent": "${:,.2f}"}))

# Cluster Distribution
st.subheader("Cluster Identifcation for Most sales in Upcoming Quarter")
fig_pie = px.pie(df, names="Clusters", title="Cluster Breakdown", color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig_pie)

# Filter Customers
st.sidebar.header("🔍 Filter Customers")
income_range = st.sidebar.slider("Income Range", int(df["Income"].min()), int(df["Income"].max()), (40000, 100000))
spending_range = st.sidebar.slider("Spending Range", int(df["Spent"].min()), int(df["Spent"].max()), (0, 4000))

filtered_df = df[(df["Income"] >= income_range[0]) & (df["Income"] <= income_range[1]) &
                 (df["Spent"] >= spending_range[0]) & (df["Spent"] <= spending_range[1])]

st.subheader("Filtered Customer Data")
st.dataframe(filtered_df)

# Cluster-wise Spending & Income
st.subheader("Spending vs Income by Cluster")
fig_scatter = px.scatter(df, x="Spent", y="Income", color="Clusters", title="Spending vs Income",
                         size_max=14, opacity=1.0, color_discrete_sequence=px.colors.qualitative.Set2_r)
st.plotly_chart(fig_scatter)

# Marketing Strategy Recommendations
st.subheader("📌 Marketing Strategy Recommendations for Each Cluster")
strategies = {
    0: "Focus on retention strategies such as loyalty programs. These customers have lower income & spending.",

    1: "Premium product promotions and high-end campaigns will work best. High-income and high-spending group.",

    2: "Discount offers and promotional campaigns should target these customers. Moderate income & spending.",

    3: "Encourage more engagement through personalized deals. These customers visit frequently but spend less."

}

for cluster, strategy in strategies.items():
    st.markdown(f"**Cluster {cluster}**: {strategy}")

st.write("---")
st.write("💡 *Use this dashboard to identify customer behavior and optimize marketing efforts!* ✨")
