import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Clovis Park Tour Events", layout="wide")

st.title("Mobile Recreation Park Tour")
st.markdown(
    "The Mobile Rec is a free community program designed to bring recreation directly to "
    "neighborhoods across our area. Mobile Rec will travel to different parks weekly, "
    "offering fun, engaging, and active play opportunities for kids of all ages. From games "
    "and sports to arts and crafts, each Mobile Rec visit turns your local park into a pop-up "
    "play space full of energy and excitement. No registration is needed, just drop in and join the fun!"
)

df = pd.read_csv("data_ai/park_events_geocoded.csv")

# Sidebar filters
st.sidebar.header("Filter Events")
months = ["All", "June", "July", "August"]
selected_month = st.sidebar.selectbox("Filter by Month", months)

if selected_month != "All":
    filtered = df[df["date"].str.contains(selected_month, case=False)]
else:
    filtered = df.copy()

st.sidebar.markdown("---")
st.sidebar.metric("Events Shown", len(filtered))
st.sidebar.metric("Total Events", len(df))

# Month color mapping
def get_color(date_str):
    if "June" in date_str:
        return "green"
    elif "July" in date_str:
        return "blue"
    elif "August" in date_str or "Augsut" in date_str:
        return "orange"
    return "gray"

# Build map centered on Clovis
center_lat = filtered["lat"].mean()
center_lon = filtered["lon"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="OpenStreetMap")

for _, row in filtered.iterrows():
    color = get_color(row["date"])
    popup_html = f"""
    <div style="font-family: sans-serif; min-width: 200px;">
        <h4 style="margin-bottom:4px; color:#1a1a1a;">{row['park']}</h4>
        <p style="margin:2px 0;"><b>Date:</b> {row['date']}</p>
        <p style="margin:2px 0;"><b>Time:</b> {row['time']}</p>
        <p style="margin:2px 0;"><b>Address:</b> {row['address']}</p>
    </div>
    """
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(popup_html, max_width=280),
        tooltip=row["park"],
        icon=folium.Icon(color=color, icon="tree-deciduous", prefix="glyphicon"),
    ).add_to(m)

# Legend
legend_html = """
<div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
     background: white; padding: 10px 16px; border-radius: 8px;
     border: 1px solid #ccc; font-family: sans-serif; font-size: 13px;">
  <b>Month</b><br>
  <span style="color: green;">&#9679;</span> June &nbsp;
  <span style="color: #4169E1;">&#9679;</span> July &nbsp;
  <span style="color: orange;">&#9679;</span> August
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Event Locations")
    st_folium(m, width="100%", height=520, returned_objects=[])

with col2:
    st.subheader("Event Schedule")
    display_df = filtered[["date", "time", "park", "address"]].copy()
    display_df.columns = ["Date", "Time", "Park", "Address"]
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=520)
