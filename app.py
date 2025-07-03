import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Telecom Customer Churn Prediction", layout="wide")

# Custom CSS for animated buttons only (no sidebar background override)
st.markdown("""
    <style>
    .stButton>button {
        background: linear-gradient(90deg, #232526 0%, #414345 100%);
        color: #fff;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #43e97b, #38f9d7 100%);
        color: #232526;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Function to load Lottie animation
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Sidebar
with st.sidebar:
    # Lottie animation (large, centered, transparent background)
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_4kx2q32n.json"  # This Lottie has a transparent background
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json is not None:
        st_lottie(lottie_json, speed=1, width=220, height=220, key="sidebar-lottie")
    st.markdown("""
        <h3 class='sandip-animated'>Developed by Sandip</h3>
        <style>
        .sandip-animated {
            text-align: center;
            margin-top: -30px;
            background: linear-gradient(90deg, #43e97b, #38f9d7, #4B8BBE, #43e97b);
            background-size: 200% auto;
            color: #fff;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-move 3s linear infinite, fadeInLeft 1.2s;
        }
        @keyframes gradient-move {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        @keyframes fadeInLeft {
            0% { opacity: 0; transform: translateX(-40px); }
            100% { opacity: 1; transform: translateX(0); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            button[aria-selected="true"] {
                background: linear-gradient(270deg, #ff512f, #dd2476, #ff6a00, #ff512f, #b06ab3);
                color: white !important;
                font-weight: bold !important;
                background-size: 400% 400%;
                animation: sidebar-gradient-move 4s ease infinite;
                border: 0 !important;
                transition: background 0.3s;
            }
            @keyframes sidebar-gradient-move {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
        </style>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title="Main Menu",
        options=[
            "Churn Prediction",
            "Prediction Logs", 
            "Batch Prediction",
            "How the Model Works",
            "About"
            ],
        icons=[
            "bar-chart", 
            "file-earmark-text", 
            "cloud-upload",
            "gear",
            "info-circle"
            ],
        menu_icon="cast",
        default_index=0,
    )

# Page Navigation
if selected == "Churn Prediction":
    from app_pages.churn_prediction import show_churn_prediction
    show_churn_prediction()

elif selected == "Prediction Logs":
    from app_pages.prediction_logs import show_prediction_logs
    show_prediction_logs()

elif selected == "Batch Prediction": 
    from app_pages.batch_prediction import show_batch_prediction
    show_batch_prediction()

elif selected == "How the Model Works":
    from app_pages.how_model_works import show_how_model_works
    show_how_model_works()

elif selected == "About":
    from app_pages.about import show_about
    show_about()

st.markdown("""
    <style>
    /* Set the sidebar width and prevent text wrapping */
    [data-testid="stSidebar"] {
        min-width: 290px;
        width: 310px;
        max-width: 400px;
    }
    </style>
""", unsafe_allow_html=True)