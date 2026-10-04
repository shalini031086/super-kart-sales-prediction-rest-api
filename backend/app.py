
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# ===============================================
# Initialize Flask App
# ===============================================

super_kart_predictor_api = Flask("SuperKart Sales Predictor")

# ===============================================
# Load Model
# ===============================================

MODEL_PATH = "super_kart_model_v2_0.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# ===============================================
# Required Columns
# ===============================================

REQUIRED_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_Type_Category",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years"
]

# ===============================================
# Home Endpoint
# ===============================================

@super_kart_predictor_api.route("/", methods=["GET"])
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

# ===============================================
# Health Check Endpoint
# ===============================================

@super_kart_predictor_api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

# ===============================================
# Single Prediction Endpoint
# ===============================================

@super_kart_predictor_api.route("/v1/superkart", methods=["POST"])
def predict_super_kart_sales():

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:

        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        missing_cols = [
            col for col in REQUIRED_COLUMNS
            if col not in data
        ]

        if missing_cols:
            return jsonify({
                "error": "Missing required fields",
                "missing_columns": missing_cols
            }), 400

        input_df = pd.DataFrame([data])

        prediction = model.predict(input_df)[0]

        return jsonify({
            "Predicted_Product_Store_Sales_Total":
            round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===============================================
# Batch Prediction Endpoint
# ===============================================

@super_kart_predictor_api.route("/v1/superkartbatch", methods=["POST"])
def predict_super_kart_batch():

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:

        if "file" not in request.files:
            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        input_data = pd.read_csv(file)

        missing_cols = [
            col for col in REQUIRED_COLUMNS
            if col not in input_data.columns
        ]

        if missing_cols:
            return jsonify({
                "error": "Missing columns in uploaded CSV",
                "missing_columns": missing_cols
            }), 400

        predictions = model.predict(input_data)

        predictions = [
            round(float(x), 2)
            for x in predictions
        ]

        return jsonify({
            "predictions": predictions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===============================================
# Run Flask App
# ===============================================

if __name__ == "__main__":
    super_kart_predictor_api.run(
        host="0.0.0.0",
        port=7860,
        debug=False
    )
