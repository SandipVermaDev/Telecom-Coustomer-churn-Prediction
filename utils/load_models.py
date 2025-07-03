import joblib

def load_all():
    voting_clf = joblib.load('models_and_preprocessing/voting_classifier_model.joblib')
    rfc = joblib.load('models_and_preprocessing/random_forest_model.joblib')
    label_encoders = joblib.load('models_and_preprocessing/label_encoders_dict.joblib')
    sc = joblib.load('models_and_preprocessing/standard_scaler.joblib')
    feature_order = joblib.load('models_and_preprocessing/feature_order.joblib')

    return voting_clf, rfc, label_encoders, sc, feature_order