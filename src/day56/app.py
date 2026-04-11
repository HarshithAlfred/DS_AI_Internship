from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    value = data['input']

    prediction = model.predict([[value]])

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)