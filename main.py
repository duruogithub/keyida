from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# App configuration
app.config["THRESHOLD"] = float(os.getenv("THRESHOLD", 0.136868298))
app.config["MODEL_PATH"] = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), "rf_model.pkl"))

# Validate model path
if not os.path.exists(app.config["MODEL_PATH"]):
    raise FileNotFoundError(f"Model file not found: {app.config['MODEL_PATH']}")

# Load model
try:
    logger.info(f"Loading model file: {app.config['MODEL_PATH']}")
    model = joblib.load(app.config["MODEL_PATH"])
    if not hasattr(model, "predict"):
        raise ValueError("Loaded model is invalid. Please verify the model file!")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise RuntimeError(f"Unable to load model: {e}")

@app.route("/")
def index():
    """Render home page"""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Template rendering error: {e}")
        return f"Template rendering error: {e}", 500

@app.route("/predict", methods=["POST"])
def predict():
    """Handle prediction request"""
    try:
        # Extract and validate input data
        input_data = validate_input(request.form)

        # Perform prediction
        prediction = make_prediction(input_data)

        # Render visualization page and pass prediction results
        return render_template("visualization.html", prediction=prediction)
    except ValueError as ve:
        logger.warning(f"Input validation failed: {ve}")
        return jsonify({"error": "Invalid input data", "details": str(ve)}), 400
    except Exception as e:
        logger.error(f"Prediction processing failed: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/visualization")
def visualization():
    """Render risk visualization page"""
    try:
        return render_template("visualization.html")
    except Exception as e:
        logger.error(f"Visualization page rendering error: {e}")
        return f"Visualization page rendering error: {e}", 500

def validate_input(form):
    """Validate and parse input data"""
    try:
        gender = int(form.get("gender", 0))
        age = int(form.get("age", 0))
        bmi = float(form.get("bmi", 0.0))
        residence = int(form.get("residence", 0))
        fx = int(form.get("fx", 0))
        bm = int(form.get("bm", 0))
        lwy = int(form.get("lwy", 0))
        smoke = int(form.get("smoke", 0))
        drink = int(form.get("drink", 0))
        fit = int(form.get("fit", 0))

        # Check if values are within expected range
        if not (0 <= gender <= 1):
            raise ValueError("Gender value must be 0 or 1")
        if not (0 <= age <= 3):
            raise ValueError("Age value must be between 0-3")
        if not (0.0 <= bmi <= 50.0):
            raise ValueError("BMI value must be between 0.0-50.0")
        if not (0 <= residence <= 1):
            raise ValueError("Residence value must be 0 or 1")
        if not all(0 <= v <= 1 for v in [fx, bm, lwy, smoke, drink, fit]):
            raise ValueError("Binary input values must be 0 or 1")

        return np.array([[gender, age, bmi, residence, fx, bm, lwy, smoke, drink, fit]])
    except ValueError as e:
        raise ValueError(f"Input data validation failed: {e}")

def make_prediction(input_data):
    """Make predictions using the model and generate results"""
    try:
        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_data)[0, 1]
            risk = probability * 100
            if probability > app.config["THRESHOLD"]:
                level, recommendation = "High Risk", "High risk! Immediate colonoscopy is recommended."
            else:
                level, recommendation = "Low Risk", "Low risk. Observation and regular follow-ups are recommended."
        else:
            prediction = model.predict(input_data)
            risk = prediction[0] * 100
            level, recommendation = "Unknown Risk", "The model does not support probability prediction. Please check the model type."

        return {
            "risk": round(risk, 2),
            "level": level,
            "recommendation": recommendation,
            "input_data": input_data.tolist(),
            "threshold": app.config["THRESHOLD"]
        }
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app_debug = os.getenv("APP_DEBUG", "false").lower() == "true"
    logger.info(f"App is running on port {port}, debug mode: {app_debug}")
    app.run(host="0.0.0.0", port=port, debug=app_debug, threaded=True)