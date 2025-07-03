import streamlit as st
from PIL import Image

def show_bio():
    # st.set_page_config(page_title="Developer Bio", layout="wide")
    st.title("👨‍🎓 Sandip Verma")
    st.subheader("Aspiring Data Analyst | Machine Learning Enthusiast")

    st.markdown("---")
    col1, col2 = st.columns([1, 3])

    with col1:
        profile_image = Image.open("assets/my_image.jpg")  # Add your image to the assets folder
        st.image(profile_image, caption="Sandip Verma", width=200)

    with col2: 
        st.markdown("""
        ### 👋 Hi, I'm **Sandip Verma**
        Aspiring **Data Analyst** with a keen interest in **Data Science** and **Machine Learning**, currently pursuing MCA in Artificial Intelligence & Data Science at **D.Y. Patil International University, Pune**.

        I have a strong foundation in programming, statistics, and data-driven decision-making. With hands-on experience in data cleaning, exploratory data analysis, data visualization, and predictive modeling, I aim to solve real-world business problems using analytical and machine learning techniques.

        - 📍 **Location**: Pune, India  
        - 📧 **Email**: iamsandip2608@gmail.com  
        - 🔗 [LinkedIn](https://www.linkedin.com/in/sandip-verma-dev/)  
        - 💻 [GitHub](https://github.com/SandipVermaDev)
        """)

    st.markdown("---")

    st.markdown("## 🎓 Education")
    st.markdown("""
    - **MCA in AI & DS**, D.Y. Patil International University, Pune — *08/2024 – Present*  
      *SGPA (1st Sem): 8.37 / 10*

    - **BCA**, C B Patel Computer College - VNSGU, Surat — *08/2021 – 04/2024*  
      *CGPA: 8.54 / 10*

    - **12th (GSEB)** — 77.86%  
    - **10th (GSEB)** — 80%
    """)

    st.markdown("---")

    st.markdown("## 🛠️ Skills")
    st.markdown("""
    - **Languages**: Python, SQL  
    - **Libraries**: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn  
    - **Tools**: Power BI, Excel, MySQL, Jupyter Notebook
    """)

    st.markdown("---")

    st.markdown("## 📊 Projects")

    st.markdown("### 🚖 Ola Data Analysis [GitHub](https://github.com/SandipVermaDev/Ola-Data-Analysis)")
    st.markdown("""
    - Analyzed 100,000+ ride records to uncover trends, cancellations, and revenue patterns using SQL and Excel.
    - Found key operational issues with a 28.08% cancellation rate.
    - Developed interactive Power BI dashboards to present findings.
    """)

    st.markdown("### 🚗 Car Price Prediction [GitHub](https://github.com/SandipVermaDev/car-price-prediction)")
    st.markdown("""
    - Predicted resale prices using data from 56,000+ car listings.
    - Used feature engineering and trained XGBoost with R² score of **0.8883**.
    - Enabled smarter decision-making for buyers and dealers.
    """)

    st.markdown("---")

    st.markdown("## 📜 Certifications")
    st.markdown("""
    - **Data Science & Machine Learning Fundamentals** – Udemy *(2025)*  
    - **Business Intelligence Using Advanced Excel & Power BI** – ExcelR *(2025)*
    """)

    st.markdown("---")

    st.markdown("## 🙌 Final Note")
    st.info("""
    This entire project, including the model design, frontend, backend, and deployment, was developed by me as part of my academic journey to explore real-world applications of machine learning and analytics.

    Thank you for visiting!
    """)

    st.markdown("---")
    # Add a back button to reset view
    if st.button("⬅️ Back to About"):
        st.session_state["show_bio"] = False
        st.rerun()