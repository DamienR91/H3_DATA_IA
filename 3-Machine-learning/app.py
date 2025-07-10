from flask import Flask, jsonify
from predict import predict as predict_function

app = Flask(__name__)

@app.route('/')
def home():
    return "API Flask"

@app.route('/predict')
def predict_route():
    prediction = predict_function()
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)