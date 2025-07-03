def show_prediction_logs():
    import streamlit as st
    import pandas as pd
    import os
    import plotly.express as px

    st.title("🗂️ Prediction Logs Viewer")
    
    csv_path = "prediction_logs.csv"
    
    if os.path.exists(csv_path):
        df_logs = pd.read_csv(csv_path)

        # 🔍 Filter by Prediction Result
        prediction_filter = st.selectbox("Filter by Prediction Result", options=["All", "Churn", "No Churn"], key="logs_prediction_filter")
        if prediction_filter != "All":
            df_logs = df_logs[df_logs["Prediction"] == prediction_filter]


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
        st.subheader("📄 Filtered Logs") 
        st.dataframe(df_logs.style.apply(highlight_risk_level, axis=1), use_container_width=True)


        # 📊 Show Summary Stats
        st.subheader("📈 Summary Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔥 Churn Risk Level Distribution")
            risk_level_counts = df_logs['Churn_Risk_Level'].value_counts().reset_index()
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
            st.markdown("### 📊 Prediction Result Distribution")
            churn_counts = df_logs["Prediction"].value_counts().reset_index()
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
            st.download_button(
                label="Download CSV",
                data=df_logs.to_csv(index=False),
                file_name="prediction_logs.csv",
                mime="text/csv"
            )
    else:
        st.warning("No prediction logs found yet.")
        st.markdown("Make a prediction to generate logs.")