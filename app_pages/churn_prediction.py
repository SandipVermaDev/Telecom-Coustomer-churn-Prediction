def show_churn_prediction():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from utils.load_models import load_all
    import shap

    # Load models and preprocessors
    voting_clf, rfc, label_encoders, sc, feature_order = load_all()


    # Set page title and layout
    st.markdown("<h1 style='color:#ff7f50;'>📊 Telecom Customer Churn Prediction</h1>", unsafe_allow_html=True)
    st.markdown("Predict whether a customer will churn based on their profile. Let's make data-driven decisions! 💡")



    # Define input features
    categorical_columns = [
        'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
        'PaperlessBilling', 'PaymentMethod'
    ]

    numerical_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']


    # Input form
    with st.form("churn_form"):
        st.subheader("🧾 Enter Customer Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox("Gender", ['Select Gender', 'Female', 'Male'])
            SeniorCitizen_display = st.selectbox("Senior Citizen", ['Select Senior Citizen', 'No', 'Yes']) 
            Partner = st.selectbox("Partner", ['Select Partner', 'Yes', 'No'])
            Dependents = st.selectbox("Dependents", ['Select Dependents', 'Yes', 'No'])
            PhoneService = st.selectbox("Phone Service", ['Select Phone Service', 'Yes', 'No'])

        with col2:
            MultipleLines = st.selectbox("Multiple Lines", ['Select Multiple Lines', 'No phone service', 'No', 'Yes'])
            InternetService = st.selectbox("Internet Service", ['Select Internet Service', 'DSL', 'Fiber optic', 'No'])
            OnlineSecurity = st.selectbox("Online Security", ['Select Online Security', 'No', 'Yes', 'No internet service'])
            OnlineBackup = st.selectbox("Online Backup", ['Select Online Backup', 'Yes', 'No', 'No internet service'])
            DeviceProtection = st.selectbox("Device Protection", ['Select Device Protection', 'No', 'Yes', 'No internet service'])

        with col3:
            TechSupport = st.selectbox("Tech Support", ['Select Tech Support', 'No', 'Yes', 'No internet service'])
            StreamingTV = st.selectbox("Streaming TV", ['Select Streaming TV', 'No', 'Yes', 'No internet service'])
            StreamingMovies = st.selectbox("Streaming Movies", ['Select Streaming Movies', 'No', 'Yes', 'No internet service'])
            Contract = st.selectbox("Contract", ['Select Contract', 'Month-to-month', 'One year', 'Two year'])
            PaperlessBilling = st.selectbox("Paperless Billing", ['Select Paperless Billing', 'Yes', 'No'])
            PaymentMethod = st.selectbox("Payment Method", ['Select Payment Method', 
                'Electronic check', 'Mailed check',
                'Bank transfer (automatic)', 'Credit card (automatic)'
            ])

        st.markdown("---")

        col4, col5, col6 = st.columns(3)

        with col4:
            tenure = st.number_input("Tenure (in months)", min_value=1, max_value=100, value=12)

        with col5:
            MonthlyCharges = st.number_input("Monthly Charges", min_value=18.0, max_value=200.0, value=70.0)

        with col6:
            TotalCharges = st.number_input("Total Charges", min_value=18.0, max_value=10000.0, value=1000.0)


        # Real-time validation of conditions
        valid_input = True

        if InternetService == 'No':
            if OnlineSecurity != 'No internet service' or OnlineBackup != 'No internet service' or \
            DeviceProtection != 'No internet service' or TechSupport != 'No internet service' or \
            StreamingTV != 'No internet service' or StreamingMovies != 'No internet service':
                st.error("When Internet Service is 'No', all related services must be set to 'No internet service'.")
                valid_input = False
        
        if PhoneService == 'No' and MultipleLines != 'No phone service':
            st.error("When Phone Service is 'No', Multiple Lines must be 'No phone service'.")
            valid_input = False

        # 🔁 Reverse validation (vise-versa)

        # If PhoneService is 'Yes', MultipleLines must not be 'No phone service'
        if PhoneService == 'Yes' and MultipleLines == 'No phone service':
            st.error("When Phone Service is 'Yes', Multiple Lines cannot be 'No phone service'.")
            valid_input = False

        # If InternetService is NOT 'No', none of the related services can be 'No internet service'
        if InternetService != 'No':
            if OnlineSecurity == 'No internet service' or OnlineBackup == 'No internet service' or \
            DeviceProtection == 'No internet service' or TechSupport == 'No internet service' or \
            StreamingTV == 'No internet service' or StreamingMovies == 'No internet service':
                st.error("When Internet Service is active, related services cannot be set to 'No internet service'.")
                valid_input = False
        

        # PaperlessBilling and PaymentMethod validation
        if PaperlessBilling == 'Yes' and PaymentMethod == 'Mailed Check':
            st.error("When Paperless Billing is 'Yes', Payment Method cannot be 'Mailed Check'.")
            valid_input = False

        if PaperlessBilling == 'No' and (PaymentMethod == 'Electronic check' or PaymentMethod == 'Bank transfer'):
            st.error("When Paperless Billing is 'No', Payment Method cannot be 'Electronic check' or 'Bank transfer'.")
            valid_input = False


        if TotalCharges < MonthlyCharges:
            st.error("Total Charges cannot be less than Monthly Charges. Please correct the input.")
            valid_input = False
        elif TotalCharges < (tenure*.8) * MonthlyCharges:
            st.warning("⚠️ Total charges seem unusually low based on tenure and monthly charges.")



        # submit = st.form_submit_button("Predict Churn", type="primary")

        col_submit1, col_submit2, col_submit3 = st.columns([2, 1, 1.5])
        with col_submit2:
            submit = st.form_submit_button("🚀 Predict Churn", type="primary")




    if submit and valid_input:
        if gender == 'Select Gender' or SeniorCitizen_display == 'Select Senior Citizen' or \
           Partner == 'Select Partner' or Dependents == 'Select Dependents' or PhoneService == 'Select Phone Service' or \
           MultipleLines == 'Select Multiple Lines' or InternetService == 'Select Internet Service' or \
           OnlineSecurity == 'Select Online Security' or OnlineBackup == 'Select Online Backup' or \
           DeviceProtection == 'Select Device Protection' or TechSupport == 'Select Tech Support' or \
           StreamingTV == 'Select Streaming TV' or StreamingMovies == 'Select Streaming Movies' or \
           Contract == 'Select Contract' or PaperlessBilling == 'Select Paperless Billing' or \
           PaymentMethod == 'Select Payment Method':
            st.error("Please select valid values for all fields.")
        
        else:

            # Step 1: Convert readable input to correct format
            SeniorCitizen = 1 if SeniorCitizen_display == 'Yes' else 0

            input_data = {
                'gender': gender,
                'SeniorCitizen': SeniorCitizen,
                'Partner': Partner,
                'Dependents': Dependents,
                'PhoneService': PhoneService,
                'MultipleLines': MultipleLines,
                'InternetService': InternetService,
                'OnlineSecurity': OnlineSecurity,
                'OnlineBackup': OnlineBackup,
                'DeviceProtection': DeviceProtection,
                'TechSupport': TechSupport,
                'StreamingTV': StreamingTV,
                'StreamingMovies': StreamingMovies,
                'Contract': Contract,
                'PaperlessBilling': PaperlessBilling,
                'PaymentMethod': PaymentMethod,
                'tenure': tenure,
                'MonthlyCharges': MonthlyCharges,
                'TotalCharges': TotalCharges
            }

            input_df = pd.DataFrame([input_data])

            # Reorder input_df columns
            input_df = input_df[feature_order]

            # Step 2: Encode categorical columns using the same LabelEncoder
            for col in categorical_columns:
                le_col = label_encoders[col]
                input_df[col] = le_col.transform(input_df[col])

            # Step 3: Standardize numerical columns using saved scaler
            input_df[numerical_columns] = sc.transform(input_df[numerical_columns])

            # Step 4: Make prediction
            pred_proba = voting_clf.predict_proba(input_df)[0]
            pred_class = voting_clf.predict(input_df)[0]



            # Initialize SHAP TreeExplainer with Random Forest
            explainer = shap.TreeExplainer(rfc)

            # Calculate SHAP values for the input data
            shap_values = explainer.shap_values(input_df)
            if isinstance(shap_values, list):
                shap_vals_for_churn = shap_values[1][0]  # [1] for class 1, [0] for the sample
            else:
                shap_vals_for_churn = shap_values[0]  



            st.markdown("---")
            st.subheader("🔍 Prediction Result")

            
            # Convert to percentage 
            churn_prob = round(pred_proba[1]*100, 2)


            # Categorize churn risk
            if churn_prob < 40:
                churn_risk = "Low"
                st.markdown(f"<h4 style='color: green; font-weight: bold;'>✅ Low Risk: The customer is unlikely to churn</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#27ae60; font-size:16px;'>Great! There's only a <strong>{churn_prob}%</strong> chance this customer might churn. They appear quite loyal.</p>", unsafe_allow_html=True)

            elif churn_prob < 70:
                churn_risk = "Moderate"
                st.markdown(f"<h4 style='color: orange; font-weight: bold;'>⚠️ Moderate Risk: The customer may churn</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#f39c12; font-size:16px;'>Heads up! There's a <strong>{churn_prob}%</strong> chance this customer could churn. Consider proactive engagement.</p>", unsafe_allow_html=True)

            else:
                churn_risk = "High"
                st.markdown(f"<h4 style='color: red; font-weight: bold;'>🔥 High Risk: The customer is likely to churn</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:#e74c3c; font-size:16px;'>Alert! There's a <strong>{churn_prob}%</strong> chance this customer will churn. Immediate action is recommended!</p>", unsafe_allow_html=True)


            # Display the probability bar
            st.markdown(f"<div style='font-size:16px;color: purple'>📊 Churn Risk Meter:</div>", unsafe_allow_html=True)
            st.progress(int(churn_prob))


            st.markdown("---")
            # 🎯 Tailored Suggestions
            st.markdown("### 💡 Retention Suggestions")

            if churn_prob < 40:
                st.markdown("""
                <ul style='color: #27ae60; font-size:16px;'>
                    <li>Consider offering a loyalty reward or a thank-you discount.</li>
                    <li>Encourage the customer to leave a positive review.</li>
                    <li>Promote value-added services like premium streaming or device protection.</li>
                </ul>
                """, unsafe_allow_html=True)

            elif churn_prob < 70:
                st.markdown("""
                <ul style='color: #f39c12; font-size:16px;'>
                    <li>Send a personalized check-in email offering support or a special offer.</li>
                    <li>Recommend upgrading to a longer-term contract for cost savings.</li>
                    <li>Suggest enabling features like Online Backup or Tech Support.</li>
                </ul>
                """, unsafe_allow_html=True)

            else:
                st.markdown("""
                <ul style='color: #e74c3c; font-size:16px;'>
                    <li>Flag this customer for a priority retention call or outreach.</li>
                    <li>Offer a customized retention offer (e.g., 1-month free service, discount).</li>
                    <li>Invite them to participate in a feedback survey to identify pain points.</li>
                    <li>Consider enrolling them in a customer success or onboarding program.</li>
                </ul>
                """, unsafe_allow_html=True)


            st.markdown("---")
            
            if input_data['Contract'] == 'Month-to-month':
                st.markdown("<p style='color:#d35400;'>📅 This customer is on a month-to-month plan, which is linked to higher churn. Consider promoting a yearly plan with better value.</p>", unsafe_allow_html=True)

            if input_data['PaymentMethod'] == 'Electronic check':
                st.markdown("<p style='color:#c0392b;'>💳 Customers using electronic checks have higher churn rates. Suggest switching to a secure auto-payment option like bank or credit card transfer.</p>", unsafe_allow_html=True)

            if input_data['OnlineSecurity'] == 'No' or input_data['TechSupport'] == 'No':
                st.markdown("<p style='color:#2980b9;'>🔐 This customer isn’t using Online Security or Tech Support. Promote these services to increase engagement and perceived value.</p>", unsafe_allow_html=True)

            if input_data['tenure'] <= 6:
                st.markdown("<p style='color:#16a085;'>🆕 This customer is fairly new. First impressions matter! Offer onboarding support or a welcome reward to build loyalty early.</p>", unsafe_allow_html=True)

            if input_data['StreamingTV'] == 'Yes' or input_data['StreamingMovies'] == 'Yes':
                st.markdown("<p style='color:#2c3e50;'>🎥 Streaming users are engaged—keep them hooked! Recommend other add-ons or personalized content packs.</p>", unsafe_allow_html=True)



            # Saving the prediction log
            st.markdown("---")
            # Create a copy of the original, human-readable input (before encoding/scaling)
            original_log_data = pd.DataFrame([input_data])
            original_log_data['SeniorCitizen'] = SeniorCitizen_display  # Replace numeric with readable value

            # Add prediction results
            original_log_data['Churn_Probability (%)'] = churn_prob
            original_log_data['Churn_Risk_Level'] = churn_risk
            original_log_data['Prediction'] = 'Churn' if pred_class == 1 else 'No Churn'
            original_log_data['Timestamp'] = pd.Timestamp.now()

            # Save to CSV with header only if file doesn't exist
            import os
            csv_path = "prediction_logs.csv"
            write_header = not os.path.exists(csv_path)

            original_log_data.to_csv(csv_path, mode='a', header=write_header, index=False)


            st.markdown(f"<p style='color:#8e44ad;'>📝 Prediction logged successfully!</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#8e44ad;'>📂 View all predictions in the Prediction Logs section.</p>", unsafe_allow_html=True)



            st.markdown("---")

            # If shape is (19, 2), take only churn column
            if shap_vals_for_churn.ndim == 2 and shap_vals_for_churn.shape[1] == 2:
                shap_vals_for_churn = shap_vals_for_churn[:, 1]

            # shap_vals_for_churn = shap_vals_for_churn.flatten()
            # Display SHAP explanation for the current prediction
            st.subheader("📌 Top Factors Influencing This Prediction")
            shap_df = pd.DataFrame({
                'Feature': input_df.columns,
                'SHAP Value': shap_vals_for_churn
            }).sort_values(by='SHAP Value', key=abs, ascending=False)

            fig_shap = px.bar(
                shap_df.head(10),
                x='SHAP Value',
                y='Feature',
                orientation='h',
                color='SHAP Value',
                color_continuous_scale='RdBu',
                # title="Top 10 SHAP Feature Contributions"
            )    

            fig_shap.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_shap, use_container_width=True)





            # st.subheader("📊 Model Insights")
            # Visual pie chart of probabilities
            # fig, ax = plt.subplots()
            # ax.pie([pred_proba[0], pred_proba[1]], labels=['No Churn', 'Churn'], autopct='%1.1f%%', colors=['#6fa8dc', '#e06666'])
            # st.pyplot(fig)

            # Feature importance from Random Forest
            # st.subheader("🔎 Feature Importance")
            # importances = rfc.feature_importances_
            # feature_names = input_df.columns
            # feat_imp_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)

            # # st.bar_chart(feat_imp_df.set_index('Feature'))
            # fig_feat = px.bar(
            #     feat_imp_df,
            #     x='Importance',
            #     y='Feature',
            #     orientation='h',
            #     color='Importance',
            #     color_continuous_scale='Bluered',  # 'Tealgrn', 'Viridis', 'Bluered', 'Plasma', etc.
            #     title="Random Forest Feature Importance"
            # )   

            # fig_feat.update_layout(yaxis=dict(autorange="reversed"))
            # st.plotly_chart(fig_feat, use_container_width=True)