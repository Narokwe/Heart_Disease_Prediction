# api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the trained model and scaler
try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    logging.info("Model and scaler loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model or scaler: {e}")
    raise RuntimeError(f"Error loading model or scaler: {e}")

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Heart Disease Prediction API is running!"})

@app.route("/version", methods=["GET"])
def version():
    return jsonify({"version": "1.0.0"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "features" not in data:
            return jsonify({
                "error": "Request must contain 'features' key with a list of numeric values."
            }), 400

        features = np.array(data["features"])

        if features.ndim != 1 or features.shape[0] != scaler.mean_.shape[0]:
            return jsonify({
                "error": f"Expected {scaler.mean_.shape[0]} features, got {features.shape[0]}."
            }), 400

        features = features.reshape(1, -1)
        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)

        return jsonify({
            "prediction": int(prediction[0]),
            "message": "Prediction successful"
        })

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)