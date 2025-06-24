import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Streamlit page settings
st.set_page_config(page_title="MindPulse Dashboard", layout="wide")

# Optional styling
st.markdown("""
    <style>
        .main {background-color: #f8f9fa;}
        h1 {color: #004080;}
        h2 {color: #2c3e50;}
    </style>
""", unsafe_allow_html=True)

st.title("MindPulse – Mental Health in Tech Dashboard")

# Upload section
uploaded_file = st.file_uploader("📁 Upload cleaned survey CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Sidebar filters
    with st.sidebar:
        st.header("Filter Options")
        selected_country = st.multiselect("Select Country", sorted(df['Country'].unique()))
        selected_gender = st.multiselect("Select Gender", ['Male', 'Female', 'Other'])

    # Apply filters
    if selected_country:
        df = df[df['Country'].isin(selected_country)]
    if selected_gender:
        df = df[df['Gender'].isin(selected_gender)]

    # KPIs
    st.markdown("### 🧮 Key Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Respondents", len(df))
    col2.metric("Seeking Treatment", df[df['treatment'] == 'Yes'].shape[0])
    col3.metric("Countries Covered", df['Country'].nunique())

    # Gender Distribution Pie Chart
    st.markdown("### ⚧️ Gender Distribution")
    gender_count = df['Gender'].value_counts().reset_index()
    gender_count.columns = ['Gender', 'Count']
    fig_gender = px.pie(gender_count, names='Gender', values='Count',
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        title="Gender Breakdown")
    st.plotly_chart(fig_gender, use_container_width=True)

    # Treatment by Gender Bar Chart
    st.markdown("### 💬 Treatment by Gender")
    treat_gender = pd.crosstab(df['Gender'], df['treatment']).reset_index()
    fig_treat_gender = px.bar(treat_gender, x='Gender', y=['Yes', 'No'],
                              barmode='group',
                              color_discrete_sequence=px.colors.qualitative.Pastel,
                              labels={'value': 'Count', 'variable': 'Treatment'})
    st.plotly_chart(fig_treat_gender, use_container_width=True)

    # Top 10 Countries by Respondents
    st.markdown("### 🌍 Top 10 Countries")
    top_countries = df['Country'].value_counts().head(10).reset_index()
    top_countries.columns = ['Country', 'Respondents']
    fig_country = px.bar(top_countries, x='Respondents', y='Country', orientation='h',
                         color='Country',
                         color_discrete_sequence=px.colors.qualitative.Vivid,
                         title="Top Responding Countries")
    st.plotly_chart(fig_country, use_container_width=True)

    # Work Interference by Treatment
    st.markdown("### 🧠 Work Interference vs Treatment")
    fig_work = px.histogram(df, x='work_interfere', color='treatment',
                            barmode='group',
                            color_discrete_sequence=px.colors.qualitative.Set2,
                            category_orders={'work_interfere': ['Never', 'Rarely', 'Sometimes', 'Often', 'Not applicable']})
    st.plotly_chart(fig_work, use_container_width=True)

    # Family History Pie Chart
    st.markdown("### 👨‍👩‍👧‍👦 Family History of Mental Illness")
    fam_count = df['family_history'].value_counts().reset_index()
    fam_count.columns = ['Family History', 'Count']
    fig_fam = px.pie(fam_count, names='Family History', values='Count',
                     color_discrete_sequence=px.colors.sequential.Sunset)
    st.plotly_chart(fig_fam, use_container_width=True)

    # Raw Data Viewer
    st.subheader("📋 Raw Data")
    with st.expander("Click to expand full dataset"):
        st.dataframe(df)

else:
    st.info("📌 Please upload the cleaned `survey_cleaned.csv` file to begin.")
