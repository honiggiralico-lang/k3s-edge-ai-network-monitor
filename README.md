# K3s Edge AI Network Anomaly Detector

This project integrates DevOps, Networking (Telecommunications), and Artificial Intelligence. 
The goal is to build a real-time network anomaly detection system (e.g., DDoS attacks) running on a lightweight Kubernetes (K3s) cluster on Proxmox bare-metal.

## Architecture
- **Infrastructure:** Proxmox VE (1 Fedora Master, 2 Debian Workers)
- **Orchestration:** K3s (Lightweight Kubernetes)
- **Application:** Flask API running in Docker containers
- **AI/ML:** scikit-learn Isolation Forest model for anomaly detection, trained offline.

## Project Workflow
1. **AI Training:** A scikit-learn model is trained offline using synthetic network traffic data.
2. **Flask API:** The trained model is embedded into a Flask application, which exposes an endpoint for real-time inference.
3. **Edge Deployment:** The Flask app is containerized and deployed on the K3s cluster.
4. **Network Monitoring:** Agents (DaemonSets) on the Debian worker nodes collect real-time network metrics and send them to the Flask API for anomaly detection.

## Directory Structure
- `ai_training/`: Python scripts for data generation, model training, and evaluation.
- `flask_app/`: The Flask API application and Dockerfile.
- `k3s_manifests/`: Kubernetes YAML manifests for deploying the application and agents on K3s.
