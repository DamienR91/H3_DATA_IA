import joblib
import numpy as np

model = joblib.load("regression.joblib")

def predict(features):
    X = np.array([features])
    prediction = model.predict(X)
    return prediction.tolist()