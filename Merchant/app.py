import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Ensure script runs in the correct directory
os.chdir(os.path.dirname(__file__))

csv_files = [
    'Bannerghatta Road (P2) Plaza', 'Kadathanamale Toll Plaza', 'Kanakapura Road (P3) Plaza', 
    'ELECTRONIC CITY Phase 1', 'Tumkur Road (P7) Toll', 'Magadi Road (P6) Plaza', 
    'Kulumapalya toll plaza', 'Hosur Road (P1) Toll', 'Laxamannath Plaza', 
    'Banglaore-Nelamangala Plaza', 'Mysore Road (P5) Plaza', 'Link Road (L1) Toll', 
    'ATTIBELLE', 'Nelamangala Toll Plaza', 'Devanahalli Toll Plaza', 
    'Hoskote Toll Plaza', 'Kaniminike Toll Plaza'
]

st.markdown(
    """
    <style>
    div.stButton > button {
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Vehicle Count Analysis")
st.subheader("Select a Toll Plaza")

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

cols = st.columns(3)
for i, file in enumerate(csv_files):
    if cols[i % 3].button(file):
        st.session_state.selected_file = file  

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"❌ File '{file_path}' not found. Please ensure it is present in the deployment environment.")
        return None
    try:
        df = pd.read_csv(file_path)
        df['initiated_time'] = pd.to_datetime(df['initiated_time'].str[-5:], format='%H:%M', errors='coerce')
        df = df.dropna(subset=['initiated_time'])
        df['time_group'] = df['initiated_time'].dt.floor('30min')
        grouped_data = df.groupby('time_group').size().reset_index(name='vehicle_count')
        grouped_data['time_group'] = grouped_data['time_group'].dt.strftime('%H:%M')
        return grouped_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def plot_graph(grouped_data, title):
    fig = px.line(grouped_data, 
                  x='time_group', 
                  y='vehicle_count', 
                  markers=True,  
                  title=title)
    fig.update_xaxes(title_text="Time Intervals (HH:MM)", tickangle=45)
    fig.update_yaxes(title_text="Number of Vehicles")
    fig.update_layout(plot_bgcolor="#808080")
    st.plotly_chart(fig, use_container_width=True, key=title)
    return fig

if st.session_state.selected_file:
    file_path = f"{st.session_state.selected_file}.csv"
    grouped_data = load_data(file_path)
    if grouped_data is not None:
        plot_graph(grouped_data, f"Vehicle Count Per 30-Minute Interval\n  *{st.session_state.selected_file}*")

st.markdown("""---""")

if st.button("🚦 Overall Bangalore Insights", use_container_width=True):
    st.markdown("""<style>
    button {font-size: 50px !important; font-weight: bold;}
    </style>""", unsafe_allow_html=True)
    overall_file = "Bangalore_1Day_NETC.csv"
    overall_data = load_data(overall_file)
    if overall_data is not None:
        plot_graph(overall_data, "Overall Vehicle Count Per 30-Minute Interval in Bangalore")

if st.button("For Tabular Insights", use_container_width=True):
    df = pd.read_csv("Bangalore_1Day_NETC.csv")
    toll_data = df['merchant_name'].value_counts().reset_index()
    toll_data.columns = ["Name of Toll Plaza", "Total vehicles passed in last 24 hrs"]
    toll_data.index = toll_data.index + 1  # Set index to start from 1
    st.title("Toll Plaza Traffic Summary (Last 24 Hours)")
    st.table(toll_data)