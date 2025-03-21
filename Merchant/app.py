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

st.title("📊 Toll Plaza Operations")
tabs_font_css = """
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
  font-size: 24px;
}
</style>
"""
st.markdown(tabs_font_css, unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 Data Analysis", "📹 Video Playback", "⏳ Peak Hour Prediction"])

with tab1:
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

with tab2:
    st.subheader("🎥 Video Playback")

    youtube_link = "https://www.youtube.com/embed/VSKIHXwZbR8?si=UDchQkJM3yuMALrJ&rel=0"
    st.markdown(
    f'<iframe width="100%" height="400" src="{youtube_link}" '
    'frameborder="0" allow="accelerometer; autoplay; clipboard-write; '
    'encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
    unsafe_allow_html=True
    )

with tab3:
    st.subheader("⏳ Peak Hour Prediction")
    
    st.write("""
    Here we analyze historical traffic data to predict peak hours at various toll plazas. 
    Below are insights based on real-time trends and historical patterns. Using synthetic data.
    """)

    # Display three images with descriptions
    # col1, col2, col3 = st.columns(3)

    
    st.image("predicted_hour_test.png", caption="Peak Traffic Trend Over Test Data",use_container_width=True)
    st.write("This graph compares actual (green) and predicted (red) peak traffichours over time, highlighting forecast accuracy and variations. The shaded regionrepresents the confidence interval, helping visualize prediction reliability.")

    st.image("predicted_hour_weekly.png", caption="Hourly Traffic Distribution",use_container_width=True)
    st.write("This graph compares actual (blue) and predicted (red) peak traffichours from March 10-16, 2024. It highlights forecast accuracy and variations inpeak traffic trends over the week.")

    st.image("predicyed_hour_traffic.png", caption="Predicted Peak Hours",use_container_width=True)
    st.write("This graph compares actual (blue) and predicted (red) traffic peakhours on holidays throughout the year. It highlights forecast accuracy andseasonal traffic variations.")
