def show_prediction_logs():
    import streamlit as st
    import pandas as pd
    import os
    import plotly.express as px

    # st.title("🗂️ Prediction Logs Viewer")
    
    st.markdown("""
        <style>
        .logs-animated-header {
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
        .logs-animated-header .emoji {
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
        .card-container-logs {
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 4px 24px 0 rgba(80,80,120,0.08);
            padding: 1.5em 1.2em 1.2em 1.2em;
            margin-bottom: 2em;
        }
        .stDataFrame, .stTable {
            border-radius: 12px !important;
            overflow: hidden !important;
        }
        .stDataFrame, .stTable, .stDataFrame *, .stTable *, .stDataFrame table, .stDataFrame th, .stDataFrame td, .stTable table, .stTable th, .stTable td {
            color: #111 !important;
            -webkit-text-fill-color: #111 !important;
        }
        .stDataFrame tbody tr:hover {
            background-color: #f7f7fa !important;
        }
        .gradient-download button {
            background: linear-gradient(90deg, #ff512f, #dd2476, #ff6a00, #ff512f, #b06ab3);
            background-size: 200% auto;
            color: #fff;
            font-weight: bold;
            border-radius: 8px;
            transition: 0.3s;
            border: none;
            font-size: 1.1rem;
            padding: 0.6em 1.5em;
            animation: gradient-move 3s linear infinite;
        }
        .gradient-download button:hover {
            background-position: 100% 0;
            color: #fff;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <h1 class='logs-animated-header'>
            <span class='emoji'>🗂️</span> Prediction Logs Viewer
        </h1>
    """, unsafe_allow_html=True)
    
    csv_path = "prediction_logs.csv"
    
    if os.path.exists(csv_path):
        df_logs = pd.read_csv(csv_path)

        # 🔍 Filter by Prediction Result
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            prediction_filter = st.selectbox("Filter by Prediction Result", options=["All", "Churn", "No Churn"], key="logs_prediction_filter")
        with col_filter2:
            risk_filter = st.selectbox("Filter by Churn Risk Level", options=["All", "High", "Moderate", "Low"], key="logs_risk_filter")
        if prediction_filter != "All":
            df_logs = df_logs[df_logs["Prediction"] == prediction_filter].copy()
        if risk_filter != "All":
            df_logs = df_logs[df_logs["Churn_Risk_Level"] == risk_filter].copy()
        # Ensure df_logs is a DataFrame (not ndarray)
        if not isinstance(df_logs, pd.DataFrame):
            df_logs = pd.DataFrame(df_logs)

        # ✨ Highlight Churn Risk Level
        def highlight_risk_level(row):
            if row['Churn_Risk_Level'] == 'High':
                return ['background-color: #ffcccc' for _ in row]  # Red for High risk
            elif row['Churn_Risk_Level'] == 'Moderate':
                return ['background-color: #ffeb99' for _ in row]  # Orange for Moderate risk
            elif row['Churn_Risk_Level'] == 'Low':
                return ['background-color: #d5f5e3' for _ in row]  # Green for Low risk
            else:
                return ['' for _ in row]  # No highlight if risk level is unknown


        # 📋 Display Filtered Logs
        # st.markdown("<div class='fade-in-section'><h3 class='logs-animated-header' style='font-size:1.3rem;margin-bottom:0.5em;'>📄 Filtered Logs</h3></div>", unsafe_allow_html=True)
        styled_logs = df_logs.style.apply(highlight_risk_level, axis=1).set_properties(**{'color': 'black'})
        st.dataframe(styled_logs, use_container_width=True)


        # 📊 Show Summary Stats
        st.markdown("""
            <div class='fade-in-section'>
                <h3 class='logs-animated-header' style='font-size:1.3rem;margin-bottom:0.5em;'>
                    <span class='emoji'>📈</span> Summary Statistics
                </h3>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div style='font-size:1.1rem;margin-bottom:0.5em;'><b><span class='emoji'>🔥</span> Churn Risk Level Distribution</b></div>", unsafe_allow_html=True)
            risk_level_counts = df_logs['Churn_Risk_Level'].value_counts().reset_index() # type: ignore
            risk_level_counts.columns = ['Risk Level', 'Count']
            fig_risk = px.bar(
                risk_level_counts,
                x='Risk Level',
                y='Count',
                color='Risk Level',
                color_discrete_map={
                    'High': 'red',
                    'Moderate': 'orange',
                    'Low': 'green'
                },
                title="Churn Risk Levels",
                height=400
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        with col2:
            st.markdown("<div style='font-size:1.1rem;margin-bottom:0.5em;'><b><span class='emoji'>📊</span> Prediction Result Distribution</b></div>", unsafe_allow_html=True)
            churn_counts = df_logs["Prediction"].value_counts().reset_index() # type: ignore
            churn_counts.columns = ['Prediction', 'Count']
            fig_pred = px.bar(
                churn_counts,
                x='Prediction',
                y='Count',
                color='Prediction',
                color_discrete_map={
                    'Churn': 'crimson',
                    'No Churn': 'dodgerblue'
                },
                title="Churn vs No Churn",
                height=400
            )
            st.plotly_chart(fig_pred, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # st.subheader("📈 Churn Risk Level Distribution")
        # risk_level_counts = df_logs['Churn_Risk_Level'].value_counts()
        # st.bar_chart(risk_level_counts)

        # # 📊 Show Overall Prediction Stats
        # st.subheader("📈 Prediction Stats")
        # churn_counts = df_logs["Prediction"].value_counts()
        # st.write("**Prediction Counts:**")
        # st.bar_chart(churn_counts)

        # 📥 Download Option
        with st.expander("📥 Download Logs as CSV"):
            st.markdown('<div class="gradient-download">', unsafe_allow_html=True)
            st.download_button(
                label="Download CSV",
                data=df_logs.to_csv(index=False),
                file_name="prediction_logs.csv",
                mime="text/csv"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No prediction logs found yet.")
        st.markdown("Make a prediction to generate logs.")