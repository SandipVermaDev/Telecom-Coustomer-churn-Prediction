# 📊 Telecom Customer Churn Prediction

---

## 🚀 Overview

**Telecom Customer Churn Prediction** is an interactive web application that leverages machine learning to predict customer churn for telecom companies. The app provides both single and batch prediction modes, insightful visualizations, and actionable retention suggestions—all in a modern, animated UI.

- **Live Demo:** [Streamlit Cloud App](https://telecom-customer-churn-prediction-sandip.streamlit.app/)

---

## ✨ Features

- **Single & Batch Churn Prediction:**  
  Predict churn for individual customers or upload a CSV for batch processing.
- **Prediction Output:**  
  For each prediction, the app displays the predicted churn probability (%), risk level (Low/Moderate/High), and churn status (Churn/No Churn).
- **Interactive Visualizations:**  
  Explore customer demographics, service usage, billing etc.
- **Model Explainability:**  
  SHAP-based feature importance for every prediction.
- **Retention Suggestions:**  
  Get actionable, data-driven tips to reduce churn risk.
- **Prediction Logging:**  
  All predictions are logged for review and analysis.
- **Modern UI:**  
  Animated, theme-adaptive interface built with Streamlit.

---

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** (UI)
- **scikit-learn** (ML models)
- **XGBoost** (Boosting)
- **Pandas, NumPy** (Data wrangling)
- **Plotly** (Interactive charts)
- **SHAP** (Model interpretability)
- **Matplotlib, Seaborn** (Additional visualizations)
- **Joblib** (Model serialization)

---

## 📂 Project Structure

```
.
├── app.py                       # Main Streamlit app entry point
├── app_pages/                   # Modular Streamlit pages
│   ├── about.py
│   ├── batch_prediction.py
│   ├── bio.py
│   ├── churn_prediction.py
│   ├── how_model_works.py
│   ├── prediction_logs.py
├── assets/                      # Images and static assets
├── Datasets/                    # Sample and validation datasets
├── models_and_preprocessing/    # Trained models and encoders
├── utils/                       # Utility scripts (model loading, prediction, etc.)
├── Visualization/               # Pre-generated visualizations
├── prediction_logs.csv          # Prediction log file
├── requirements.txt             # Python dependencies
├── Telecom Customer Churn Prediction.ipynb  # Model development and analysis notebook
└── README.md                    # Project documentation
```

---

## 📈 How It Works

1. **Input Customer Data:**  
   Enter details manually or upload a CSV file.
2. **Prediction:**  
   The app preprocesses data, applies trained ML models, and predicts churn probability.
3. **Explanation:**  
   SHAP values highlight the top factors influencing each prediction.
4. **Retention Tips:**  
   Get tailored suggestions to reduce churn risk.
5. **Visualization:**  
   Explore customer and churn trends with interactive charts.

---

## 🎥 Demo

![App Demo](assets\demo.gif)

---

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SandipVermaDev/Telecom-Customer-Churn-Prediction.git
cd Telecom-Customer-Churn-Prediction
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

### 4. Open in Browser

Visit [http://localhost:8501](http://localhost:8501) to use the app.

---

## 📚 Datasets

- **WA_Fn-UseC_-Telco-Customer-Churn.csv**  
  (Source: [Kaggle - Telco Customer Churn](https://www.kaggle.com/blastchar/telco-customer-churn))

---

## 👨‍💻 Author

- **Sandip Verma**  
  MCA student | Data Science & Machine Learning Enthusiast  
  LinkedIn: [Sandip Verma](https://www.linkedin.com/in/sandip-verma-dev/)

---

## 🙏 Acknowledgements

- [Kaggle - Telco Customer Churn Dataset](https://www.kaggle.com/blastchar/telco-customer-churn)
- Streamlit, scikit-learn, XGBoost, SHAP, Plotly, and the open-source community.

---