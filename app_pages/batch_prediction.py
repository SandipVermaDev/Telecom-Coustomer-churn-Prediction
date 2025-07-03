def show_batch_prediction():
    import streamlit as st
    import pandas as pd
    import numpy as np
    from utils.load_models import load_all
    from utils.predict_utils import preprocess_input, make_prediction, get_retention_suggestion
    import plotly.express as px


    # Load models and objects
    voting_clf, rfc, label_encoders, sc, feature_order = load_all()

    st.markdown("""
        <style>
        .batch-animated-header {
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
        .batch-animated-header .emoji {
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
        .card-container-batch {
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 4px 24px 0 rgba(80,80,120,0.08);
            padding: 1.5em 1.2em 1.2em 1.2em;
            margin-bottom: 2em;
        }
        .batch-btn button, .stButton>button {
            background: linear-gradient(90deg, #ff512f, #dd2476, #ff6a00, #ff512f, #b06ab3);
            background-size: 200% auto;
            color: #fff;
            font-weight: bold;
            border-radius: 8px;
            box-shadow: 0 2px 8px 0 rgba(80,80,120,0.10);
            transition: 0.3s;
            border: none;
            font-size: 1.1rem;
            padding: 0.7em 2.2em;
            animation: gradient-move 3s linear infinite;
        }
        .batch-btn button:hover, .stButton>button:hover {
            background-position: 100% 0;
            color: #fff;
            transform: scale(1.05);
            box-shadow: 0 4px 16px 0 rgba(80,80,120,0.18);
        }
        .stDataFrame, .stTable, .stDataFrame *, .stTable *, .stDataFrame table, .stDataFrame th, .stDataFrame td, .stTable table, .stTable th, .stTable td {
            color: #111 !important;
            -webkit-text-fill-color: #111 !important;
        }
        .stDataFrame tbody tr:hover {
            background-color: #f7f7fa !important;
        }
        .gradient-download-batch button {
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
        .gradient-download-batch button:hover {
            background-position: 100% 0;
            color: #fff;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <h1 class='batch-animated-header'>
            <span class='emoji'>📁</span> Batch Churn Prediction
        </h1>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:1.1rem; margin-bottom:1.5em;'>Upload a CSV file to predict churn for multiple customers.</div>", unsafe_allow_html=True)

    # Initialize session state to track uploaded file name
    if "uploaded_file_name" not in st.session_state:
        st.session_state.uploaded_file_name = None

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    # Clear results if a new file is uploaded
    if uploaded_file is not None:
        current_name = uploaded_file.name
        if st.session_state.uploaded_file_name != current_name:
            st.session_state.uploaded_file_name = current_name
            st.session_state.pop("batch_results", None)


    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        expected_cols = [col for col in feature_order if col != 'Churn'] 

        # Step 2: Check if all expected features are in the uploaded data
        if not all(col in df.columns for col in expected_cols):
            missing_cols = [col for col in expected_cols if col not in df.columns]
            st.error(f"🚫 Uploaded file is missing required columns: {missing_cols}")
            return
        
        original_df = df.copy()  # Preserve original for results

        # Clean DataFrame for unknown categories
        df_clean: pd.DataFrame = df.copy()
        if not isinstance(df_clean, pd.DataFrame):
            st.error("Input data is not a DataFrame after cleaning.")
            return
        try:
            for col in label_encoders.keys():
                if col in df_clean.columns:
                    le = label_encoders[col]
                    df_clean[col] = df_clean[col].apply(lambda x: x if x in le.classes_ else np.nan)
                    if df_clean[col].isnull().sum() > 0:
                        st.warning(f"⚠️ Column '{col}' has unseen categories. Rows with unknown values will be skipped.")
                    df_clean = df_clean.loc[df_clean[col].notnull()]
            if len(df_clean) == 0:
                st.warning("No valid rows remain after cleaning for unknown categories.")
                return
            preprocessed_rows = [preprocess_input(row, label_encoders, sc, expected_cols) for row in df_clean.to_dict(orient='records')]
        except Exception as e:
            st.error(f"Preprocessing error: {e}")
            return

        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.markdown('<div class="batch-btn">', unsafe_allow_html=True)
            predict_button = st.button("Predict", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        
        if predict_button:
            # Predictions
            try:
                probs = []
                preds = []
                for arr in preprocessed_rows:
                    pred, prob = make_prediction(voting_clf, arr)
                    preds.append(pred)
                    probs.append(prob)
            except Exception as e:
                st.error(f"Prediction failed: {e}")
                return

            # Add predictions to original DataFrame
            original_df = original_df.loc[df_clean.index].copy() # type: ignore
            original_df['Churn_Probability (%)'] = (np.array(probs) * 100).round(2)
            original_df['Churn_Risk_Level'] = original_df['Churn_Probability (%)'].apply(lambda x: 'High' if x >= 70 else 'Moderate' if x >= 40 else 'Low')
            original_df['Prediction'] = np.where(np.array(preds) == 1, 'Churn', 'No Churn')
            original_df['Timestamp'] = pd.Timestamp.now()

            # Save to session state
            st.session_state["batch_results"] = original_df


        # If results exist in session state
        if "batch_results" in st.session_state:
            original_df = st.session_state["batch_results"]

            # Display results in tabular format
            st.markdown("---")
            # st.subheader("📊 Prediction Results")
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader("📊 Prediction Results")

            with col2:
                st.markdown('<div class="batch-btn">', unsafe_allow_html=True)
                if st.button("❌ Clear Results", use_container_width=True):
                    st.session_state.pop("batch_results", None)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)


            # 🔍 Filter by Prediction Result and Churn Risk Level
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                prediction_filter = st.selectbox("Filter by Prediction Result", options=["All", "Churn", "No Churn"], key="batch_prediction_filter")
            with col_filter2:
                risk_filter = st.selectbox("Filter by Churn Risk Level", options=["All", "High", "Moderate", "Low"], key="batch_risk_filter")
            filtered_df = original_df.copy()
            if prediction_filter != "All":
                filtered_df = filtered_df[filtered_df["Prediction"] == prediction_filter]
            if risk_filter != "All":
                filtered_df = filtered_df[filtered_df["Churn_Risk_Level"] == risk_filter]

            if filtered_df.empty:
                st.warning("⚠️ No results match the selected filter.")
            else:
                # Highlight churn risk levels
                def highlight_risk_level(row):
                    if row['Churn_Risk_Level'] == 'High':
                        return ['background-color: #ffcccc' for _ in row]  # Red for High risk
                    elif row['Churn_Risk_Level'] == 'Moderate':
                        return ['background-color: #ffeb99' for _ in row]  # Orange for Moderate risk
                    elif row['Churn_Risk_Level'] == 'Low':
                        return ['background-color: #d5f5e3' for _ in row]  # Green for Low risk
                    else:
                        return ['' for _ in row]  # No highlight if risk level is unknown

                styled_filtered = filtered_df.style.apply(highlight_risk_level, axis=1).set_properties(**{'color': 'black'})
                st.dataframe(styled_filtered)

                # Download button for results
                st.markdown("---")
                csv = original_df.to_csv(index=False).encode('utf-8')
                st.markdown('<div class="gradient-download-batch">', unsafe_allow_html=True)
                st.download_button("📥 Download Results as CSV", csv, "churn_predictions.csv", "text/csv", key='download-csv')
                st.markdown('</div>', unsafe_allow_html=True)


                # 📈 Summary Statistics Section
                st.markdown("""
                    <div class='fade-in-section'>
                        <h3 class='batch-animated-header' style='font-size:1.3rem;margin-bottom:0.5em;'>
                            <span class='emoji'>📈</span> Summary Statistics
                        </h3>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("<div style='font-size:1.1rem;margin-bottom:0.5em;'><b><span class='emoji'>🔥</span> Churn Risk Level Distribution</b></div>", unsafe_allow_html=True)
                    risk_level_counts = original_df['Churn_Risk_Level'].value_counts().reset_index() # type: ignore
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
                        height=350
                    )
                    st.plotly_chart(fig_risk, use_container_width=True)

                with col2:
                    st.markdown("<div style='font-size:1.1rem;margin-bottom:0.5em;'><b><span class='emoji'>📊</span> Prediction Result Distribution</b></div>", unsafe_allow_html=True)
                    prediction_counts = original_df['Prediction'].value_counts().reset_index() # type: ignore   
                    prediction_counts.columns = ['Prediction', 'Count']

                    fig_pred = px.bar(
                        prediction_counts,  
                        x='Prediction',
                        y='Count',
                        color='Prediction',
                        color_discrete_map={
                            'Churn': 'crimson',
                            'No Churn': 'dodgerblue'
                        },
                        title="Churn vs No Churn",
                        height=350
                    )
                    st.plotly_chart(fig_pred, use_container_width=True)


                # Display individual details for each row on click
                for i, row in filtered_df.iterrows():
                    with st.expander(f"Customer {i}: {row['Prediction']} - {row['Churn_Risk_Level']} Risk"):

                     
                        # Show customer details in a horizontal row
                        st.markdown("#### 🧾 Customer Details")
                        # columns = st.columns(len(expected_cols))
                        # for col, feature in zip(columns, expected_cols):
                        #     with col:
                        #         st.markdown(f"**{feature}**")
                        #         st.write(row[feature])
                        details_dict = {feature: row[feature] for feature in expected_cols}
                        details_df = pd.DataFrame(details_dict.items(), columns=["Feature", "Value"]) # type: ignore
                        st.table(details_df)    


                        prob = row['Churn_Probability (%)']
                        st.markdown(f"<h4 style='color: purple;'>🔮 Churn Probability: <strong>{prob}%</strong></h4>", unsafe_allow_html=True)
                        st.progress(int(prob))

                        # Risk messages
                        if prob < 40:
                            st.markdown(f"<p style='color:#27ae60;'>✅ Low Risk: Unlikely to churn.</p>", unsafe_allow_html=True)
                        elif prob < 70:
                            st.markdown(f"<p style='color:#f39c12;'>⚠️ Moderate Risk: Might churn.</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p style='color:#e74c3c;'>🔥 High Risk: Likely to churn.</p>", unsafe_allow_html=True)

                        # Retention suggestions
                        st.markdown("### 💡 Retention Suggestions")
                        suggestions = get_retention_suggestion(prob)

                        # Context-based tips
                        if row['Contract'] == 'Month-to-month':
                            suggestions.append("Promote yearly plans with better value.")
                        if row['PaymentMethod'] == 'Electronic check':
                            suggestions.append("Suggest switching to auto-payment options.")
                        if row['OnlineSecurity'] == 'No' or row['TechSupport'] == 'No':
                            suggestions.append("Promote Online Security or Tech Support.")
                        if row['tenure'] <= 6:
                            suggestions.append("Offer onboarding support or welcome reward.")
                        if row['StreamingTV'] == 'Yes' or row['StreamingMovies'] == 'Yes':
                            suggestions.append("Recommend additional content packs or upgrades.")

                        st.markdown("<ul style='font-size:16px;'>" + "".join([f"<li>{s}</li>" for s in suggestions]) + "</ul>", unsafe_allow_html=True)

                st.success("✅ All customer predictions completed!")
            
