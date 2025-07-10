from flask import Flask, jsonify, request
from predict import predict as predict_function

app = Flask(__name__)

@app.route('/')
def home():
    return "API Flask"

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.get_json()
    features = data.get("features")
    prediction = predict_function(features)
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)