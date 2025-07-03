import pandas as pd

categorical_columns = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

numerical_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']

def preprocess_input(input_dict, label_encoders, scaler, feature_order):
    df = pd.DataFrame([input_dict])
    df = df[feature_order]
    
    for col in categorical_columns:
        df[col] = label_encoders[col].transform(df[col])

    df[numerical_columns] = scaler.transform(df[numerical_columns])
    return df

def make_prediction(model, input_df):
    proba = model.predict_proba(input_df)[0]
    pred = model.predict(input_df)[0]
    return pred, proba[1]

def get_retention_suggestion(churn_prob):
    if churn_prob < 40:
        return [
            "Offer loyalty rewards or thank-you discount.",
            "Encourage the customer to leave a review or referral."
        ]
    elif churn_prob < 70:
        return [
            "Send personalized offers or service upgrades.",
            "Reach out for feedback and experience improvement."
        ]
    else:
        return [
            "Assign a retention specialist to the account.",
            "Offer strong incentives or extended contract discounts.",
            "Evaluate any service complaints urgently."
        ]
