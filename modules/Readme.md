# Anomaly Detection Pipeline Modules

Multi-domain anomaly detection system supporting Network Security, Manufacturing Quality Control, and Medical Diagnostics.

## 📦 Installation

pip install torch scikit-learn numpy pandas pillow

## 🚀 Quick Start

from modules import predict_network, predict_mvtec, predict_xray

### Network Intrusion Detection

result = predict_network({'preset': 'normal_web_browsing'})

### Product Quality Inspection

result = predict_mvtec('product_image.png')

### Chest X-Ray Analysis

result = predict_xray('chest_xray.png')


## 📚 Module Details

### 1. Network Module
- **Dataset**: UNSW-NB15
- **Models**: 4 unsupervised (IsolationForest, OCSVM, EllipticEnvelope, LOF)
- **Input**: Network traffic features (44 dimensions)
- **Output**: Normal/Attack classification

### 2. MVTec Module
- **Dataset**: MVTec Anomaly Detection
- **Models**: ResNet34 + 4 anomaly detectors
- **Input**: Product images
- **Output**: Normal/Anomaly classification

### 3. X-ray Module
- **Dataset**: NIH Chest X-ray14
- **Models**: 5 unsupervised + 2 supervised
- **Input**: Chest X-ray images
- **Output**: Normal/Anomaly + Disease classification

## 📖 API Reference

See individual module docstrings for detailed API documentation.

## 👨‍💻 Author

Tanishq Rahul Shelke

## 📄 License

MIT License
