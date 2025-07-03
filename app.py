import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Telecom Customer Churn Prediction", layout="wide")

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns([.3, 1, .2])
    with col2:
        st.image("assets/logo.png", width=165)
        st.markdown("<h3 style='color:#4682b4;'> Developed by Sandip. </h3>", unsafe_allow_html=True)
    
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