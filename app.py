import streamlit as st
import pandas as pd

# Set up the page layout
st.set_page_config(page_title="Flight Price Analysis", layout="wide")

# Header
st.title("✈️ AI Travel Analyst - Flight Pricing Insights")
st.write("Explore the factors that drive flight prices based on 100,000 real-world records.")

# Show a peek at the dataset
st.subheader("1. The Dataset (Cleaned)")
# Note: Update the path below if your CSV has a slightly different name!
try:
    df = pd.read_csv('data/flight_pricing_dataset.csv')
    st.dataframe(df.head(10))
except FileNotFoundError:
    st.warning("Please ensure your dataset is in the 'data' folder to view it here.")

st.divider()

# Show the Visualizations side-by-side
st.subheader("2. Key Visualizations & Insights")
col1, col2 = st.columns(2)

with col1:
    st.image("outputs/visualizations/1_price_distribution.png", caption="Distribution of Flight Prices")
    st.write("**Insight:** Most flights are cheap, but extreme outliers exist.")
    
    st.image("outputs/visualizations/3_class_vs_price.png", caption="Prices by Travel Class")
    st.write("**Insight:** First Class is significantly more expensive, but Economy has rare, extreme price spikes.")

with col2:
    st.image("outputs/visualizations/2_airline_vs_price.png", caption="Prices by Airline")
    st.write("**Insight:** Premium airlines have much wider price ranges than budget airlines.")
    
    st.image("outputs/visualizations/4_stops_vs_price.png", caption="Prices by Number of Stops")
    st.write("**Insight:** More stops generally mean a slightly higher median price.")

st.divider()

# Final full-width graph
st.image("outputs/visualizations/5_days_vs_price.png", caption="Days Before Departure vs. Price", use_column_width=True)
st.write("**Insight:** Booking under 50 days before departure causes massive price spikes.")