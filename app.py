import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SkyCast | AI Travel Analyst",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN STYLING (CSS) ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e2638, #2a3b5c);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #00d2ff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 0.9rem;
        color: #9ab4d0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    .metric-sub {
        font-size: 0.85rem;
        color: #00d2ff;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTION FOR IMAGES ---
def display_visual(image_path, title, caption):
    st.markdown(f"### {title}")
    if os.path.exists(image_path):
        st.image(image_path, caption=caption, use_container_width=True)
    else:
        st.info(f"📊 Visualization placeholder: `{image_path}` (Run notebook to render asset)")

# --- APP HEADER ---
st.title("✈️ SkyCast: Flight Pricing & Intelligence Dashboard")
st.caption("MIC AIML Track 3 — Exploratory Data Analysis & Pricing Dynamics Platform")

st.markdown("---")

# --- TOP KPI METRICS ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Optimal Booking Window</div>
            <div class="metric-value">> 50 Days</div>
            <div class="metric-sub">Save up to 45% on base fares</div>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Class Price Multiplier</div>
            <div class="metric-value">3.2x - 5.1x</div>
            <div class="metric-sub">Economy vs. Business/First</div>
        </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Surge Window</div>
            <div class="metric-value">&lt; 15 Days</div>
            <div class="metric-sub">Exponential pricing spike</div>
        </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Data Records Analyzed</div>
            <div class="metric-value">100,000+</div>
            <div class="metric-sub">Cleaned & validated entries</div>
        </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab_estimator, tab_visuals, tab_data = st.tabs([
    "🎛️ Live Price Indicator & Estimator",
    "📈 Market Visualizations & Insights", 
    "📂 Dataset Explorer"
])

# ==========================================
# TAB 1: INTERACTIVE PRICE INDICATOR
# ==========================================
with tab_estimator:
    st.subheader("Interactive Fare Estimator & Deal Indicator")
    st.write("Simulate market conditions to evaluate estimated ticket prices and surge risk.")
    
    col_input, col_output = st.columns([1.2, 1.8])
    
    with col_input:
        st.markdown("#### 🛠️ Travel Parameters")
        travel_class = st.selectbox("Cabin Class", ["Economy", "Premium Economy", "Business", "First"])
        airline = st.selectbox("Airline Carrier", ["IndiGo", "Air India", "Vistara", "SpiceJet", "AirAsia", "GoAir"])
        stops = st.radio("Number of Stops", [0, 1, 2], horizontal=True, format_func=lambda x: "Non-stop (0)" if x == 0 else f"{x} Stop(s)")
        days_left = st.slider("Days Before Departure", min_value=1, max_value=90, value=35)
        
    with col_output:
        st.markdown("#### 🏷️ Price Indicator Output")
        
        # Heuristic price estimation engine
        base_fares = {"Economy": 4500, "Premium Economy": 8500, "Business": 22000, "First": 38000}
        airline_multipliers = {"IndiGo": 1.0, "AirAsia": 0.92, "SpiceJet": 0.95, "GoAir": 0.93, "Air India": 1.15, "Vistara": 1.25}
        
        calculated_base = base_fares[travel_class] * airline_multipliers[airline]
        stop_surcharge = stops * 1200
        
        # Surge pricing curve based on days left
        if days_left < 7:
            urgency_multiplier = 2.1
            deal_status = "🔴 Extreme Surge Pricing (Last Minute)"
            badge_color = "#ff4b4b"
        elif days_left < 20:
            urgency_multiplier = 1.5
            deal_status = "🟡 Moderate Surge Alert"
            badge_color = "#ffa421"
        elif days_left < 50:
            urgency_multiplier = 1.15
            deal_status = "🔵 Standard Market Rate"
            badge_color = "#00d2ff"
        else:
            urgency_multiplier = 0.88
            deal_status = "🟢 Optimal Booking Window (Best Deal)"
            badge_color = "#21c354"
            
        final_estimate = int((calculated_base + stop_surcharge) * urgency_multiplier)
        lower_bound = int(final_estimate * 0.92)
        upper_bound = int(final_estimate * 1.08)
        
        st.markdown(f"""
            <div style="background-color: #1e2638; padding: 25px; border-radius: 12px; border: 1px solid #3d4f73;">
                <div style="color: #9ab4d0; font-size: 0.9rem;">ESTIMATED FARE RANGE</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 8px 0;">
                    ₹{lower_bound:,} – ₹{upper_bound:,}
                </div>
                <div style="display: inline-block; background-color: {badge_color}22; color: {badge_color}; border: 1px solid {badge_color}; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                    {deal_status}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("##### 📌 Dynamic Price Breakdown:")
        st.markdown(f"""
        * **Base Tier:** ₹{base_fares[travel_class]:,} ({travel_class})
        * **Carrier Adjustment:** {airline_multipliers[airline]}x multiplier ({airline})
        * **Route Factor:** +₹{stop_surcharge:,} for {stops} stop(s)
        * **Departure Pressure:** {urgency_multiplier}x demand factor ({days_left} days remaining)
        """)

# ==========================================
# TAB 2: VISUALIZATIONS & INSIGHTS
# ==========================================
with tab_visuals:
    st.subheader("Key Findings & Visual Analytics")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        display_visual(
            "outputs/visualizations/1_price_distribution.png",
            "1. Overall Price Distribution",
            "Right-skewed density curve showing concentration of low-cost flights with high-value premium outliers."
        )
        display_visual(
            "outputs/visualizations/3_class_vs_price.png",
            "3. Cabin Class Variance",
            "Discrete separation in median pricing between economy and premium tiers."
        )

    with col_v2:
        display_visual(
            "outputs/visualizations/2_airline_vs_price.png",
            "2. Carrier Pricing Distributions",
            "Full-service carriers exhibit wider price variances compared to low-cost alternatives."
        )
        display_visual(
            "outputs/visualizations/4_stops_vs_price.png",
            "4. Layover & Stop Impact",
            "Fares scale with added stops due to cumulative airport taxes and connection legs."
        )
        
    st.markdown("---")
    display_visual(
        "outputs/visualizations/5_days_vs_price.png",
        "5. Booking Horizon vs. Ticket Price",
        "Clear exponential surge pattern emerging as departure date approaches (< 20 days)."
    )

# ==========================================
# TAB 3: DATA EXPLORER
# ==========================================
with tab_data:
    st.subheader("Dataset Inspector")
    
    csv_candidates = ['data/flight_pricing_dataset.csv', 'flight_pricing_dataset.csv']
    loaded_df = None
    for path in csv_candidates:
        if os.path.exists(path):
            loaded_df = pd.read_csv(path)
            break
            
    if loaded_df is not None:
        st.dataframe(loaded_df.head(50), use_container_width=True)
        st.caption(f"Showing first 50 rows of {len(loaded_df):,} total records.")
    else:
        st.warning("⚠️ Cleaned CSV file not detected in standard directory paths. Place dataset in `./data/` folder.")