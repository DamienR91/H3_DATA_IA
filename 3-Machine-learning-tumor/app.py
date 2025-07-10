from flask import Flask, request, jsonify
from predict_tumor import predict_tumor

app = Flask(__name__)

@app.route('/')
def home():
    return "API Flask Tumor"

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.get_json()
    features = data.get("features")
    prediction = predict_tumor(features)
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
