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
def load_data():
    df = pd.read_csv("smoking.csv")
    return df

df = load_data()

# Use 'Data.Percentage.Total' as the prevalence column
prevalence_col = 'Data.Percentage.Total'

# ----------------------
# Filters
# ----------------------
with st.sidebar:
    st.header("🔍 Filter Data")
    selected_years = st.multiselect("Select Year(s):", options=df['Year'].unique(), default=df['Year'].unique())
    selected_countries = st.multiselect("Select Country/Countries:", options=df['Country'].unique(), default=df['Country'].unique())

filtered_df = df[(df["Year"].isin(selected_years)) & (df["Country"].isin(selected_countries))]

# ----------------------
# Key Metrics
# ----------------------
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", f"{filtered_df.shape[0]}")
col2.metric("Unique Countries", f"{filtered_df['Country'].nunique()}")
col3.metric("Average Smoking Rate (%)", f"{filtered_df[prevalence_col].mean():.2f}")

# ----------------------
# Top Smoking Countries
# ----------------------
st.subheader("🌍 Top 10 Countries by Smoking Rate")
top_countries = filtered_df.groupby("Country")[prevalence_col].mean().sort_values(ascending=False).head(10)
fig1 = px.bar(top_countries, orientation="v", title="Top 10 Countries with Highest Smoking Prevalence", labels={"value": "Smoking Prevalence (%)", "Country": "Country"})
st.plotly_chart(fig1, use_container_width=True)

# ----------------------
# Gender Analysis
# ----------------------
st.subheader("🧑‍🤝‍🧑 Smoking by Gender")
# Assuming 'Data.Percentage.Male' and 'Data.Percentage.Female' are the gender columns
if 'Data.Percentage.Male' in df.columns and 'Data.Percentage.Female' in df.columns:
    gender_df = filtered_df.melt(id_vars=['Country', 'Year'], value_vars=['Data.Percentage.Male', 'Data.Percentage.Female'], var_name='Gender', value_name='Smoking Prevalence (%)')
    fig2 = px.box(gender_df, x="Gender", y='Smoking Prevalence (%)', color="Gender", points="all", title="Smoking Distribution by Gender")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Gender data not available in the dataset.")


# ----------------------
# Age Group Analysis (if available)
# ----------------------
if "Age Group" in df.columns:
    st.subheader("👵 Smoking by Age Group")
    fig3 = px.violin(filtered_df, x="Age Group", y=prevalence_col, box=True, points="all", color="Age Group")
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------
# Map View (if geo available)
# ----------------------
if "Country" in df.columns:
    try:
        st.subheader("🗺️ Smoking Prevalence Map")
        country_avg = filtered_df.groupby("Country")[prevalence_col].mean().reset_index()
        fig4 = px.choropleth(country_avg, locations="Country", locationmode="country names",
                             color=prevalence_col,
                             color_continuous_scale="Reds", title="Average Smoking Prevalence by Country")
        st.plotly_chart(fig4, use_container_width=True)
    except Exception as e:
        st.warning(f"Map not displayed due to: {e}")
