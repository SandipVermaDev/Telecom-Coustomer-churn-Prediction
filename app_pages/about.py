import streamlit as st

def show_about():

    # Set session state for showing bio
    if "show_bio" not in st.session_state:
        st.session_state["show_bio"] = False

    # If the user has not clicked "Know Sandip", display the button
    if not st.session_state["show_bio"]:
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("🎓 Know Sandip"):
                st.session_state["show_bio"] = True
                st.rerun() 

    if st.session_state["show_bio"]:
        from app_pages.bio import show_bio
        show_bio()
        return  



    st.markdown("""
        <style>
        .about-animated-header {
            text-align: center;
            font-size: 2.1rem;
            font-weight: bold;
            background: linear-gradient(90deg, #ff512f, #dd2476, #ff6a00, #ff512f, #b06ab3);
            background-size: 200% auto;
            color: #222;
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-move 3s linear infinite, fadeInDown 1.2s;
            margin-top: 0;
            margin-bottom: 0.5em;
            padding-top: 0;
        }
        .about-animated-header .emoji {
            background: none !important;
            -webkit-background-clip: initial !important;
            -webkit-text-fill-color: initial !important;
            color: inherit !important;
            animation: none !important;
        }
        @keyframes gradient-move {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        @keyframes fadeInDown {
            0% { opacity: 0; transform: translateY(-40px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .fade-in-section {
            animation: fadeInSection 1.2s;
        }
        @keyframes fadeInSection {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <h1 class='about-animated-header'>
            <span class='emoji'>💡</span> About This Application
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class='fade-in-section'>
    """, unsafe_allow_html=True)
    st.markdown("""
    Welcome to the **Telecom Customer Churn Prediction** application! This tool is designed to help businesses predict customer churn (i.e., the likelihood of customers discontinuing their service) based on historical data. By understanding churn, businesses can proactively address customer retention and improve service offerings.

    ---

    ## 🎯 Objectives

    The primary objectives of this application are:

    - **Predict Customer Churn**: Using machine learning algorithms to predict whether a customer is likely to churn based on their behavior and profile.
    - **Provide Actionable Insights**: Displaying churn risk levels for each customer and providing suggestions for retention strategies.
    - **Enhance Customer Retention**: Empower businesses to take proactive actions to retain high-risk customers, thereby reducing churn and improving customer lifetime value.

    ---

    ## 🛠 Technologies Used

    The application is built using the following technologies:

    - **Python**: Core programming language for developing machine learning models and the web application.
    - **Streamlit**: A framework for quickly building interactive web applications.
    - **scikit-learn**: For building machine learning models.
    - **XGBoost**: For boosting model accuracy.
    - **Pandas**: For data manipulation and cleaning.
    - **Plotly**: For interactive data visualizations.
    - **SHAP**: For model interpretability and feature importance explanations.
    - **Matplotlib**: For static data visualizations.
    - **Seaborn**: For statistical data visualizations.

    ---

    ## 👨‍💻 Developer Information

    This application was developed by:

    - **Sandip Verma** –  MCA student with a passion for **Data Science**, **Machine Learning**, and **Predictive Analytics**.

    ---

    ## 💡 Summary

    The **Customer Churn Prediction** application is designed to assist businesses in retaining their customers by identifying those at high risk of leaving. It uses various machine learning models to predict churn and offers actionable insights to help reduce attrition. 

    Thank you for exploring this tool! Stay tuned for further updates and improvements.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
