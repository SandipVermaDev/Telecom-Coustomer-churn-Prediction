import streamlit as st

def show_how_model_works():
    st.markdown("""
        <style>
        .how-works-animated-header {
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
        .how-works-animated-header .emoji {
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
        <h1 class='how-works-animated-header'>
            <span class='emoji'>🧠</span> How the Churn Prediction Model Works
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class='fade-in-section'>
    """, unsafe_allow_html=True)
    st.markdown("""
    This page provides an overview of the **churn prediction model** used in this application, including the data preprocessing steps, model architecture, and interpretability techniques.

    ---

    ## 🔍 1. Problem Definition
    The goal of the model is to **predict whether a customer is likely to churn** (i.e., discontinue their service) based on their profile, usage behavior, and service details.

    ---

    ## 🧼 2. Data Preprocessing

    Before training, the raw data is cleaned and transformed using the following steps:

    - **Handling missing values**: Rows with invalid or missing data (e.g., empty `TotalCharges`) are cleaned.
    - **Encoding categorical variables**: Categorical fields like `Contract`, `InternetService`, etc., are encoded using `Label Encoding`.
    - **Feature scaling**: Numerical features such as `tenure`, `MonthlyCharges`, and `TotalCharges` are scaled using `StandardScaler`.

    ---

    ## 🧩 3. Feature Selection

    A curated set of features is used, based on business relevance and model importance:

    - Customer tenure
    - Monthly and total charges
    - Contract type
    - Internet and support services
    - Payment method
    - And more...

    ---

    ## 🤖 4. Model Architecture

    The prediction engine uses an **Ensemble Voting Classifier** — a powerful method that combines multiple machine learning models to improve overall performance and reduce overfitting.

    Specifically, the ensemble includes:

    - **Random Forest Classifier (RF)**: Captures non-linear relationships using decision trees and is robust to overfitting.
    - **XGBoost Classifier (XGB)**: A high-performance gradient boosting technique known for speed and accuracy.
    - **Support Vector Machine (SVM)**: Effective in high-dimensional spaces and good at finding optimal decision boundaries.
    - **Logistic Regression (LR)**: A simple yet effective baseline model that offers interpretability.

    These models are combined using **Soft Voting**, which means the final prediction is based on the **weighted average of predicted probabilities** from all models rather than a majority vote.

    This ensemble approach ensures that the model benefits from the **strengths of each individual classifier**, resulting in more stable and accurate predictions.

    ---
    
    ## 🔧 Hyperparameter Tuning

    To enhance model performance, **hyperparameter tuning** is applied to each individual model in the ensemble using techniques such as grid search or random search.

    - **Random Forest (RF)**: Optimized by tuning `n_estimators`, `max_depth`, and `min_samples_leaf`.
    - **XGBoost (XGB)**: Hyperparameters such as learning rate (eta), max depth, and `n_estimators` were fine-tuned.
    - **SVM**: Tuning of kernel types, `C` (regularization), and `gamma` to improve decision boundaries.
    - **Logistic Regression (LR)**: Optimized `C` (regularization) and solver.

    ---            


    ## 📈 5. Model Evaluation

    The model is evaluated using industry-standard metrics such as:

    - **Accuracy**: Measures the overall correctness of the model by calculating the proportion of total correct predictions.
    - **Precision**: Indicates how many of the predicted churns were actually correct (focuses on false positives).
    - **Recall**: Measures how many actual churns were correctly identified by the model (focuses on false negatives).
    - **F1 Score**: A harmonic mean of precision and recall, providing a balanced metric especially useful for imbalanced datasets.

    These metrics ensure that the model effectively balances false positives and false negatives.

    ---

    ## 🧠 6. Interpretability with SHAP

    To improve transparency, the model can be interpreted using **SHAP (SHapley Additive exPlanations)**, which highlights:

    - The most influential features for each individual prediction.
    - Global importance of features across the dataset.

    This helps in understanding **why** the model predicts churn for a specific customer.

    ---

    ## 🎯 7. Prediction Output

    Once predictions are made, the application provides:

    - **Churn probability** (as a percentage)
    - **Churn risk level** (Low, Moderate, High)
    - **Actionable suggestions** to retain high-risk customers

    ---

    ## 🧾 Summary

    This churn prediction model is designed to be:

    - **Accurate**
    - **Transparent**
    - **Business-ready**

    It empowers organizations to take **proactive retention actions** and improve customer satisfaction.

    """)
    st.markdown("</div>", unsafe_allow_html=True)

