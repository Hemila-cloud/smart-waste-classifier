import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

from simulate_bins import generate_bin_data
from waste_classifier import classify_waste_image
from route_optimizer import get_optimized_route

# Page setup
st.set_page_config(
    page_title="Smart Waste Dashboard",
    layout="wide",
    page_icon="♻️"
)

# Sidebar
st.sidebar.title("♻️ Smart Waste System")
st.sidebar.markdown("Built by **Team Alpha** 👨‍💻")
st.sidebar.divider()
st.sidebar.markdown("### 📌 Navigation")
st.sidebar.markdown("- 🗑 Real-Time Bin Monitor\n- 📷 Waste Classification\n- 🚛 Route Optimization")
st.sidebar.divider()
st.sidebar.caption("🔬 Powered by Streamlit, Folium, and AI")

# Cached bin data
@st.cache_data
def get_cached_bins():
    return generate_bin_data()

bins_df = get_cached_bins()

# Tabs
tab1, tab2, tab3 = st.tabs([
    "🗑 Real-Time Bin Monitor",
    "📷 Waste Classification",
    "🚛 Route Optimization"
])
# ==================== 🗑 TAB 1: Bin Monitor (Improved) ====================
with tab1:
    st.header("🗑 Real-Time Bin Monitoring")

    # User filter for bin status
    status_filter = st.selectbox("🔍 Filter by Fill Level", ["All", "Low (<50%)", "Medium (50-80%)", "High (>80%)"])

    # Assign color-coded status column
    def get_status(level):
        if level < 50:
            return "🟢 Low"
        elif level < 80:
            return "🟠 Medium"
        else:
            return "🔴 High"

    bins_df["Status"] = bins_df["fill_level"].apply(get_status)

    # Apply filter
    if status_filter == "Low (<50%)":
        filtered_df = bins_df[bins_df["fill_level"] < 50]
    elif status_filter == "Medium (50-80%)":
        filtered_df = bins_df[(bins_df["fill_level"] >= 50) & (bins_df["fill_level"] < 80)]
    elif status_filter == "High (>80%)":
        filtered_df = bins_df[bins_df["fill_level"] >= 80]
    else:
        filtered_df = bins_df

    # Layout: Map and Chart/Table side by side
    col1, col2 = st.columns([1.5, 1])

    # Map View
    with col1:
        st.subheader("🗺️ Bin Map (Status Colored)")
        m = folium.Map(location=[filtered_df['lat'].mean(), filtered_df['lon'].mean()], zoom_start=14)
        for _, row in filtered_df.iterrows():
            color = "green" if row['fill_level'] < 50 else "orange" if row['fill_level'] < 80 else "red"
            folium.Marker(
                [row['lat'], row['lon']],
                popup=f"{row['bin_id']} - {row['fill_level']}% ({row['Status']})",
                icon=folium.Icon(color=color)
            ).add_to(m)
        st_folium(m, width=700, height=450)

    # Fill Chart and Table
    with col2:
        st.subheader("📊 Bin Fill Levels")
        fig = px.bar(
            filtered_df,
            x="bin_id",
            y="fill_level",
            color="fill_level",
            color_continuous_scale="RdYlGn",
            labels={'fill_level': 'Fill %'},
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Bin Fill Table")
        st.dataframe(
            filtered_df[["bin_id", "fill_level", "Status"]].sort_values(by="fill_level", ascending=False),
            use_container_width=True,
            hide_index=True
        )
# ==================== 📷 TAB 2: Waste Classification ====================
with tab2:
    st.header("📷 Classify Uploaded Waste Image")

    uploaded = st.file_uploader("📤 Upload a waste image", type=["jpg", "jpeg", "png"])

    if uploaded:
        st.image(uploaded, width=350, caption="🖼️ Uploaded Image")
        label, confidence = classify_waste_image(uploaded)

        st.success(f"""
        🧠 **Prediction:** `{label}`  
        📊 **Confidence:** `{confidence:.2f}%`
        """)
    else:
        st.info("📎 Please upload a waste image to classify.")
# ==================== 🚛 TAB 3: Route Optimization ====================
with tab3:
    st.header("🚛 Optimized Truck Route")

    route = get_optimized_route(bins_df)

    if not route:
        st.info("✅ All bins are under control. No high-fill bins (>80%) detected.")
    else:
        st.success("📍 Optimized Route (bins > 80% full):")
        st.markdown(" → ".join([f"🟦 `{bin_id}`" for bin_id in route]))

        # Optional: Route map
        st.subheader("🗺️ Optimized Route Map")
        route_map = folium.Map(location=[bins_df['lat'].mean(), bins_df['lon'].mean()], zoom_start=14)

        for bin_id in route:
            row = bins_df[bins_df['bin_id'] == bin_id].iloc[0]
            folium.Marker(
                [row['lat'], row['lon']],
                popup=f"{bin_id} - {row['fill_level']}%",
                icon=folium.Icon(color='blue', icon='truck', prefix='fa')
            ).add_to(route_map)

        st_folium(route_map, width=700, height=500)
