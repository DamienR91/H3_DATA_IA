import joblib
import numpy as np

model = joblib.load("tumor_model.joblib")
scaler = joblib.load("tumor_scaler.joblib")

def predict_tumor(features):
    X = np.array([features])
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    return int(prediction[0])
