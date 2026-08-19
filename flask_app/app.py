from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the AI model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'network_anomaly_model.joblib')
try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Kubernetes liveness/readiness probes"""
    if model is not None:
        return jsonify({"status": "healthy", "model_loaded": True}), 200
    return jsonify({"status": "unhealthy", "model_loaded": False}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint for network traffic anomaly detection"""
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        data = request.get_json()
        
        # Extract features expected by the model
        # ['packets_per_sec', 'bytes_per_sec', 'flow_duration_sec', 'dst_port_entropy']
        features = [
            data.get('packets_per_sec', 0),
            data.get('bytes_per_sec', 0),
            data.get('flow_duration_sec', 0),
            data.get('dst_port_entropy', 0)
        ]
        
        # Convert to numpy array and reshape for a single prediction
        features_array = np.array(features).reshape(1, -1)
        
        # Perform inference
        # Isolation Forest returns 1 for normal, -1 for anomaly
        prediction = model.predict(features_array)[0]
        
        # Get anomaly score (lower score = more anomalous)
        score = model.decision_function(features_array)[0]
        
        is_anomaly = prediction == -1
        
        return jsonify({
            "status": "anomaly" if is_anomaly else "normal",
            "is_anomaly": bool(is_anomaly),
            "anomaly_score": float(score),
            "received_features": features
        }), 200

    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
