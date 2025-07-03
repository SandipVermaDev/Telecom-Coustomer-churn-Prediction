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



    st.title("💡 About This Application")

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
