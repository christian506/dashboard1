import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------
# Page Config
# ---------------------
st.set_page_config(
    page_title="🚬 Smoking Dashboard",
    page_icon="🚬",
    layout="wide"
)

st.title("🚬 Global Smoking Statistics Dashboard")

# ---------------------
# Load Data
# ---------------------
@st.cache_data
def load_data():
    return pd.read_csv("smoking.csv")

df = load_data()

# ---------------------
# Sidebar Filters
# ---------------------
st.sidebar.header("🔍 Filter Options")
years = sorted(df["Year"].dropna().unique())
countries = sorted(df["Country"].dropna().unique())

selected_years = st.sidebar.multiselect("Select Year(s):", options=years, default=years)
selected_countries = st.sidebar.multiselect("Select Country(ies):", options=countries, default=["Lebanon", "France", "United States"])

filtered_df = df[df["Year"].isin(selected_years) & df["Country"].isin(selected_countries)]

# Add dynamic-like variation (optional)
df_sim = filtered_df.copy()
df_sim["Data.Percentage.Total.Live"] = df_sim["Data.Percentage.Total"] * np.random.uniform(0.95, 1.05)
df_sim["Data.Percentage.Male.Live"] = df_sim["Data.Percentage.Male"] * np.random.uniform(0.95, 1.05)
df_sim["Data.Percentage.Female.Live"] = df_sim["Data.Percentage.Female"] * np.random.uniform(0.95, 1.05)

# ---------------------
# KPIs
# ---------------------
st.subheader("📊 Key Smoking Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Smoking Rate (%)", f"{df_sim['Data.Percentage.Total.Live'].mean():.2f}")
col2.metric("Avg. Male Smoking Rate (%)", f"{df_sim['Data.Percentage.Male.Live'].mean():.2f}")
col3.metric("Avg. Female Smoking Rate (%)", f"{df_sim['Data.Percentage.Female.Live'].mean():.2f}")

# ---------------------
# Gender Comparison
# ---------------------
st.subheader("👫 Smoking Rate by Gender")
gender_df = df_sim[["Country", "Year", "Data.Percentage.Male.Live", "Data.Percentage.Female.Live"]].copy()
gender_df = gender_df.melt(id_vars=["Country", "Year"], var_name="Gender", value_name="Rate")
gender_df["Gender"] = gender_df["Gender"].str.extract(r"(\w+)$")

fig_gender = px.box(gender_df, x="Gender", y="Rate", color="Gender", title="Distribution by Gender")
st.plotly_chart(fig_gender, use_container_width=True)

# ---------------------
# Trend Over Time
# ---------------------
st.subheader("📈 Trend Over Years")
trend = df_sim.groupby("Year")["Data.Percentage.Total.Live"].mean().reset_index()
fig_trend = px.line(trend, x="Year", y="Data.Percentage.Total.Live", markers=True, title="Average Smoking Rate Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------
# Map View
# ---------------------
st.subheader("🗺️ Average Smoking Rate by Country")
map_df = df_sim.groupby("Country")["Data.Percentage.Total.Live"].mean().reset_index()
fig_map = px.choropleth(map_df, locations="Country", locationmode="country names",
                        color="Data.Percentage.Total.Live", color_continuous_scale="Reds",
                        title="World Map of Smoking Rates")
st.plotly_chart(fig_map, use_container_width=True)

# ---------------------
# Raw Data Table
# ---------------------
st.subheader("🔍 Filtered Data Snapshot")
st.dataframe(df_sim.head(50))
