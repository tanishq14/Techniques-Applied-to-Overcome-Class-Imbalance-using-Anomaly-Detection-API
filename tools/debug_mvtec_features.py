import os
import sys
import numpy as np
from PIL import Image

# Ensure project root on path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modules.mvtec_pipeline import MVTecAnomalyDetector

# Prepare test image
os.makedirs('static/uploads', exist_ok=True)
img_path = 'static/uploads/debug_mvtec.png'
Image.new('L', (224, 224), color=128).save(img_path)
print('Saved test image:', img_path)

# Instantiate detector
print('\nInitializing MVTecAnomalyDetector...')
detector = MVTecAnomalyDetector()

print('\nDetector summary:')
print(' resnet loaded:', detector.resnet is not None)
print(' scaler loaded:', detector.scaler is not None)
print(' pca loaded:', detector.pca is not None)
print(' pca_models keys:', list(getattr(detector, 'pca_models', {}).keys()))
print(' isolation_pca attr:', hasattr(detector, 'isolation_pca'))
print(' pca_elliptic attr:', hasattr(detector, 'pca_elliptic'))

# Compute raw features via resnet (before scaler/pca)
print('\nComputing raw ResNet features...')
img = Image.open(img_path).convert('L')
img_tensor = detector.transform(img).unsqueeze(0).to(detector.device)
with __import__('torch').no_grad():
    raw = detector.resnet(img_tensor).cpu().numpy()
raw = raw.reshape(1, -1)
print(' raw feature shape:', raw.shape)

# Print fitted shapes on scaler/pca if available
scaler_in = getattr(detector.scaler, 'n_features_in_', None)
pca_in = getattr(detector.pca, 'n_features_in_', None)
pca_comp = getattr(detector.pca, 'n_components_', None)
print(' scaler.n_features_in_ =', scaler_in)
print(' pca.n_features_in_     =', pca_in)
print(' pca.n_components_      =', pca_comp)

# Per-model PCA info
for k, m in getattr(detector, 'pca_models', {}).items():
    ni = getattr(m, 'n_features_in_', None)
    nc = getattr(m, 'n_components_', None)
    print(f" pca_models[{k}].n_features_in_={ni}, n_components_={nc}")

# Try transformations step-by-step
print('\nAttempting transforms step-by-step:')
try:
    if detector.scaler is not None and scaler_in == raw.shape[1]:
        scaled = detector.scaler.transform(raw)
        print(' scaler.transform ->', scaled.shape)
    else:
        print(' scaler.transform skipped (shape mismatch)')
except Exception as e:
    print(' scaler.transform raised:', e)

try:
    if detector.pca is not None and pca_in == raw.shape[1]:
        pca_out = detector.pca.transform(raw)
        print(' pca.transform ->', pca_out.shape)
    else:
        print(' pca.transform skipped (shape mismatch)')
except Exception as e:
    print(' pca.transform raised:', e)

# Finally, call detector.extract_features() to see full pipeline behavior
print('\nCalling detector.extract_features() (this runs the pipeline logic):')
try:
    feat = detector.extract_features(img_path)
    print(' extract_features returned shape:', feat.shape)
except Exception as e:
    print(' extract_features raised:')
    import traceback
    traceback.print_exc()
