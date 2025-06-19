import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="🌍 Global Smoking Dashboard", layout="wide")
st.title("🚬 Global Smoking Statistics Dashboard")
st.markdown("Explore global patterns of smoking by gender, age, and country using interactive visualizations.")

# ----------------------
# Load Dataset
# ----------------------
@st.cache_data
def load_data():
    return pd.read_csv("smoking.csv")

df = load_data()

prevalence_col = 'Data.Percentage.Total'

# ----------------------
# Sidebar Filters
# ----------------------
with st.sidebar:
    st.header("🔍 Filter Data")
    selected_years = st.multiselect("Select Year(s):", options=sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
    selected_countries = st.multiselect("Select Country/Countries:", options=sorted(df['Country'].unique()), default=sorted(df['Country'].unique()))

filtered_df = df[(df["Year"].isin(selected_years)) & (df["Country"].isin(selected_countries))]

# ----------------------
# KPIs Row
# ----------------------
st.subheader("📊 Summary Statistics")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Records", f"{filtered_df.shape[0]}")
kpi2.metric("Unique Countries", f"{filtered_df['Country'].nunique()}")
kpi3.metric("Avg. Smoking Rate (%)", f"{filtered_df[prevalence_col].mean():.2f}")

# ----------------------
# Row 1: Top Countries vs Gender
# ----------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("### 🌍 Top 10 Countries by Smoking Rate")
    top_countries = filtered_df.groupby("Country")[prevalence_col].mean().sort_values(ascending=False).head(10).reset_index()
    fig1 = px.bar(top_countries, x="Country", y=prevalence_col,
                  title="Top 10 Countries with Highest Smoking Prevalence",
                  labels={prevalence_col: "Smoking Prevalence (%)"})
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    st.markdown("### 🧑‍🤝‍🧑 Smoking by Gender")
    if 'Data.Percentage.Male' in df.columns and 'Data.Percentage.Female' in df.columns:
        gender_df = filtered_df.melt(id_vars=['Country', 'Year'],
                                     value_vars=['Data.Percentage.Male', 'Data.Percentage.Female'],
                                     var_name='Gender', value_name='Smoking Prevalence (%)')
        gender_df["Gender"] = gender_df["Gender"].str.extract(r"(\w+)$")
        fig2 = px.box(gender_df, x="Gender", y='Smoking Prevalence (%)', color="Gender",
                      points="all", title="Smoking Distribution by Gender")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Gender data not available in the dataset.")

# ----------------------
# Row 2: Age (if available) vs Map
# ----------------------
row2_col2 = st.columns(2)

with row2_col2:
    st.markdown("### 🗺️ Smoking Prevalence Map")
    try:
        country_avg = filtered_df.groupby("Country")[prevalence_col].mean().reset_index()
        fig4 = px.choropleth(country_avg, locations="Country", locationmode="country names",
                             color=prevalence_col, color_continuous_scale="Reds",
                             title="Average Smoking Prevalence by Country")
        st.plotly_chart(fig4, use_container_width=True)
    except Exception as e:
        st.warning(f"Map not displayed due to: {e}")

# ----------------------
# Optional: Expandable Raw Data Table
# ----------------------
with st.expander("📄 View Filtered Data Table"):
    st.dataframe(filtered_df.head(100))
