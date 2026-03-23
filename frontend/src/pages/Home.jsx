import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <>
      <div className="welcome-section">
        <h2>Welcome to the Anomaly Detection Platform</h2>
        <p className="intro-text">
          This comprehensive API leverages state-of-the-art machine learning and deep learning 
          techniques to detect anomalies across three critical domains. Select a detection module below to get started.
        </p>
      </div>
      
      <div className="feature-cards">
        {/* Network Card */}
        <div className="feature-card network-card">
          <div className="card-icon">🌐</div>
          <h3>Network Intrusion Detection</h3>
        {/* Network Card */}
          <p className="card-description">
          Identify malicious network trafficand cyber attacks using the UNSW-NB15 dataset.
          Ensemble of 4 models with 95%+ accuracy.
          </p>
          <div className="card-details">
            <h4> Key Features:</h4>
            <ul>
              <li><strong>Dataset:</strong> UNSW-NB15 (2.5M Packets)</li>
              <li><strong>Models:</strong> Isolation Forest, OneClassSVM, Elliptic Envelope, LOF</li>
              <li><strong>Detection:</strong> 9 Attack types (DoS, Exploits, Reconnaissance, etc.)</li>
              <li><strong>Input:</strong> 44 network traffic features</li>
            </ul>
          </div>
          <Link to="/network" className="card-btn">🚀 Network Anomaly Detection</Link>
        </div>

        {/* MVTec Card */}
        <div className="feature-card mvtec-card">
            <div className="card-icon">🏭</div>
            <h3>Product Quality Inspection</h3>
            <p className="card-description">
              Detect manufacturing defects in industrial products using computer vision based detection techniques. 
              Trained on MVTec AD dataset.
            </p>
            <div className="card-details">
              <h4> Key Features:</h4>
              <ul>
                <li><strong>Dataset:</strong> MVTec AD (5,000+ images, 15 categories)</li>
                <li><strong>Models:</strong> ResNet34 + 4 anomaly detectors</li>
                <li><strong>Categories:</strong> Bottle, Cable, Circuit, Fabric, Metal parts, etc.</li>
                <li><strong>Detection:</strong> Cracks, scratches, contamination, defects</li>
              </ul>
            </div>
            <Link to="/mvtec" className="card-btn">🚀 Quality Inspection Detection</Link>
        </div>

        {/* X-ray Card */}
        <div className="feature-card xray-card">
            <div className="card-icon">🏥</div>
            <h3>Medical Chest X-ray Analysis</h3>
            <p className="card-description">
              AI-assisted diagnostic tool for detecting thoracic abnormalities. 
              Trained on NIH Chest X-ray14 dataset.
            </p>
            <div className="card-details">
            <h4>🔍 Key Features:</h4>
            <ul>
              <li><strong>Dataset:</strong> NIH Chest X-ray14 (112K+ images)</li>
              <li><strong>Conditions:</strong> 14 thoracic pathologies detectable</li>
              <li><strong>Unsupervised:</strong> Autoencoder, IsolationForest, OCSVM, LOF</li>
              <li><strong>Supervised:</strong> Decision Tree, KNN</li>
            </ul>
            <div className="medical-disclaimer-small mt-2" style={{fontSize: '0.85rem', color: '#856404'}}>
              <strong>⚠️ Disclaimer:</strong> Research tool only. Not for clinical diagnosis.
            </div>
          </div>
          <Link to="/xray" className="card-btn medical-btn">🚀 X-ray Analyzer</Link>
        </div>
      </div>

      <div className="tech-overview mt-4">
        <h2>🔧 Technical Architecture</h2>
        <div className="tech-grid">
          <div className="tech-item">
            <h4>🐍 Backend</h4>
            <p>Flask REST API</p>
            <p>Python 3.8+</p>
            <p>Modular pipeline design</p>
            <p>Docker</p>
          </div>
          <div className="tech-item"><h4>🧠 ML</h4><p>PyTorch, Scikit-learn & Ensemble Methods</p></div>
          <div className="tech-item"><h4>📊 Models</h4><p>11+ trained models</p></div>
          <div className="tech-item"><h4>🎨 Frontend</h4><p>React & Vite</p></div>
        </div>
      </div>
    </>
  );
}