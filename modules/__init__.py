"""
============================================================================
ANOMALY DETECTION PIPELINE MODULES
============================================================================

Multi-Techniques to overcome class imbalance in Anomaly Detection
Author: Tanishq Rahul Shelke
Version: 1.0

This package contains pipeline modules for three domains:
1. Network Intrusion Detection (UNSW-NB15 Dataset)
2. Industrial Product Quality Inspection (MVTec AD Dataset)
3. Medical Chest X-ray Analysis (NIH Chest X-ray14 Dataset)

============================================================================
QUICK START
============================================================================

Basic Usage:
    from modules import network_pipeline, mvtec_pipeline, xray_pipeline
    
    # Network intrusion detection
    network_data = {
        'dur': 0.5, 'proto': 'tcp', 'service': 'http',
        'state': 'FIN', 'spkts': 12, 'dpkts': 10
    }
    result = network_pipeline.predict_network(network_data)
    
    # Product quality inspection
    result = mvtec_pipeline.predict_mvtec('product_image.png')
    
    # Chest X-ray analysis
    result = xray_pipeline.predict_xray('chest_xray.png')

Advanced Usage (Direct Detector Access):
    from modules import NetworkAnomalyDetector
    
    detector = NetworkAnomalyDetector()
    result = detector.predict_all(network_data)

============================================================================
ARCHITECTURE
============================================================================

Each module follows the same pattern:
    - Detector Class: Loads models, handles preprocessing
    - predict_* function: Main API for predictions
    - Ensemble method: Combines multiple models
    
Models Used:
    Network:  4 unsupervised models (IsolationForest, OCSVM, etc.)
    MVTec:    ResNet34 + 4 anomaly detectors
    X-ray:    5 unsupervised + 2 supervised classifiers

============================================================================
"""

__version__ = '1.0.0'
__author__ = 'Tanishq Rahul Shelke'
__email__ = 'tanishq63@gmail.com'
__status__ = 'Production'

# Package metadata
__title__ = 'Anomaly Detection Pipelines'
__description__ = 'Techniques to overcome class imbalance in Anomaly/Defect Detection across multiple domains.'
__license__ = 'MIT'

import sys
import logging
from pathlib import Path

# Setup module logger
logger = logging.getLogger(__name__)

# ============================================================================
# IMPORT PIPELINE MODULES WITH ERROR HANDLING
# ============================================================================

try:
    from .network_pipeline import (
        predict_network,
        NetworkAnomalyDetector,
        TRAFFIC_PRESETS,
        DATASET_CONFIG as NETWORK_CONFIG
    )
    _network_available = True
    logger.info("✓ Network pipeline loaded successfully")
except ImportError as e:
    logger.error(f"✗ Failed to load network_pipeline: {e}")
    _network_available = False
    predict_network = None
    NetworkAnomalyDetector = None
    TRAFFIC_PRESETS = {}
    NETWORK_CONFIG = {}

try:
    from .mvtec_pipeline import (
        predict_mvtec,
        MVTecAnomalyDetector,
        DATASET_CONFIG as MVTEC_CONFIG,
        CATEGORY_INFO
    )
    _mvtec_available = True
    logger.info("✓ MVTec pipeline loaded successfully")
except ImportError as e:
    logger.error(f"✗ Failed to load mvtec_pipeline: {e}")
    _mvtec_available = False
    predict_mvtec = None
    MVTecAnomalyDetector = None
    MVTEC_CONFIG = {}
    CATEGORY_INFO = {}

try:
    from .xray_pipeline import (
        predict_xray,
        ChestXrayAnomalyDetector,
        DATASET_CONFIG as XRAY_CONFIG,
        DISEASE_INFO,
        get_disease_info,
        format_disease_report
    )
    _xray_available = True
    logger.info("✓ X-ray pipeline loaded successfully")
except ImportError as e:
    logger.error(f"✗ Failed to load xray_pipeline: {e}")
    _xray_available = False
    predict_xray = None
    ChestXrayAnomalyDetector = None
    XRAY_CONFIG = {}
    DISEASE_INFO = {}
    get_disease_info = None
    format_disease_report = None

# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    # Version info
    '__version__',
    '__author__',
    
    # Main prediction functions
    'predict_network',
    'predict_mvtec',
    'predict_xray',
    
    # Detector classes
    'NetworkAnomalyDetector',
    'MVTecAnomalyDetector',
    'ChestXrayAnomalyDetector',
    
    # Configuration & metadata
    'NETWORK_CONFIG',
    'MVTEC_CONFIG',
    'XRAY_CONFIG',
    'TRAFFIC_PRESETS',
    'CATEGORY_INFO',
    'DISEASE_INFO',
    
    # Utility functions
    'get_disease_info',
    'format_disease_report',
    'get_module_info',
    'check_modules_availability'
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_module_info():
    """
    Get information about all loaded modules
    
    Returns:
        dict: Information about each module including availability and config
    
    Example:
        >>> from modules import get_module_info
        >>> info = get_module_info()
        >>> print(info['network']['available'])
        True
    """
    return {
        'package_version': __version__,
        'author': __author__,
        'modules': {
            'network': {
                'available': _network_available,
                'description': 'Network Intrusion Detection (UNSW-NB15)',
                'models': 4,
                'dataset': 'UNSW-NB15',
                'config': NETWORK_CONFIG if _network_available else None
            },
            'mvtec': {
                'available': _mvtec_available,
                'description': 'Product Quality Inspection (MVTec AD)',
                'models': 4,
                'dataset': 'MVTec Anomaly Detection',
                'categories': len(CATEGORY_INFO) if _mvtec_available else 0,
                'config': MVTEC_CONFIG if _mvtec_available else None
            },
            'xray': {
                'available': _xray_available,
                'description': 'Medical Chest X-ray Analysis (NIH)',
                'models': 7,
                'dataset': 'NIH Chest X-ray14',
                'conditions': len(DISEASE_INFO) if _xray_available else 0,
                'config': XRAY_CONFIG if _xray_available else None
            }
        }
    }

def check_modules_availability():
    """
    Check which modules are available and working
    
    Returns:
        dict: Availability status for each module
    
    Example:
        >>> from modules import check_modules_availability
        >>> status = check_modules_availability()
        >>> if status['network']:
        ...     print("Network module ready!")
    """
    return {
        'network': _network_available,
        'mvtec': _mvtec_available,
        'xray': _xray_available,
        'all_available': _network_available and _mvtec_available and _xray_available
    }

def get_version_info():
    """
    Get detailed version information
    
    Returns:
        dict: Version details
    """
    return {
        'version': __version__,
        'title': __title__,
        'author': __author__,
        'description': __description__,
        'license': __license__,
        'status': __status__
    }

# ============================================================================
# MODULE INITIALIZATION
# ============================================================================

def _check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = {
        'torch': 'PyTorch',
        'sklearn': 'Scikit-learn',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'PIL': 'Pillow'
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing.append(name)
    
    if missing:
        logger.warning(f"Missing dependencies: {', '.join(missing)}")
        logger.warning("Install with: pip install torch scikit-learn numpy pandas pillow")
    
    return len(missing) == 0

# Check dependencies on import
_dependencies_ok = _check_dependencies()

# Log initialization summary
logger.info("="*60)
logger.info(f"Anomaly Detection Pipelines v{__version__}")
logger.info("="*60)
logger.info(f"Network Module: {'✓ Available' if _network_available else '✗ Unavailable'}")
logger.info(f"MVTec Module:   {'✓ Available' if _mvtec_available else '✗ Unavailable'}")
logger.info(f"X-ray Module:   {'✓ Available' if _xray_available else '✗ Unavailable'}")
logger.info(f"Dependencies:   {'✓ Complete' if _dependencies_ok else '✗ Incomplete'}")
logger.info("="*60)

# Warn if modules are missing
if not (_network_available and _mvtec_available and _xray_available):
    logger.warning("⚠ Some modules failed to load. API functionality may be limited.")
    logger.warning("Check error messages above for details.")

# ============================================================================
# EXAMPLES & DOCUMENTATION
# ============================================================================

EXAMPLES = {
    'network': """
# Network Intrusion Detection Example
from modules import predict_network, TRAFFIC_PRESETS

# Use a preset
result = predict_network({'preset': 'normal_web_browsing'})

# Or provide custom data
data = {
    'dur': 0.5, 'proto': 'tcp', 'service': 'http',
    'state': 'FIN', 'spkts': 12, 'dpkts': 10,
    'sbytes': 800, 'dbytes': 15000, 'rate': 40.0
}
result = predict_network(data)
print(result['ensemble']['prediction'])  # 'Normal' or 'Attack'
    """,
    
    'mvtec': """
# Product Quality Inspection Example
from modules import predict_mvtec

result = predict_mvtec('path/to/product_image.png')
print(result['ensemble']['prediction'])  # 'Normal' or 'Anomaly'
print(result['image_info']['category'])  # Detected product category
    """,
    
    'xray': """
# Medical X-ray Analysis Example
from modules import predict_xray, get_disease_info

result = predict_xray('path/to/chest_xray.png')

# Unsupervised analysis
print(result['ensemble']['prediction'])  # 'Normal' or 'Anomaly'

# Supervised diagnosis
for model_name, data in result['supervised_models'].items():
    disease = data['prediction']
    info = data['disease_info']
    print(f"{model_name}: {disease} - {info['description']}")
    """
}

def print_examples():
    """Print usage examples for all modules"""
    for module_name, example_code in EXAMPLES.items():
        print(f"\n{'='*60}")
        print(f"{module_name.upper()} MODULE EXAMPLE")
        print('='*60)
        print(example_code)

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def predict(module, *args, **kwargs):
    """
    Universal predict function that routes to appropriate module
    
    Args:
        module (str): 'network', 'mvtec', or 'xray'
        *args, **kwargs: Arguments to pass to the specific predict function
    
    Returns:
        dict: Prediction results
    
    Example:
        >>> from modules import predict
        >>> result = predict('network', network_data)
        >>> result = predict('mvtec', 'image.png')
    """
    module = module.lower()
    
    if module == 'network':
        if not _network_available:
            raise RuntimeError("Network module is not available")
        return predict_network(*args, **kwargs)
    
    elif module == 'mvtec':
        if not _mvtec_available:
            raise RuntimeError("MVTec module is not available")
        return predict_mvtec(*args, **kwargs)
    
    elif module == 'xray':
        if not _xray_available:
            raise RuntimeError("X-ray module is not available")
        return predict_xray(*args, **kwargs)
    
    else:
        raise ValueError(f"Unknown module: {module}. Choose 'network', 'mvtec', or 'xray'")

# Add predict to __all__
__all__.append('predict')
__all__.append('print_examples')
__all__.append('get_version_info')

# ============================================================================
# PACKAGE INITIALIZATION COMPLETE
# ============================================================================

if __name__ == "__main__":
    # Print info when module is run directly
    print(f"\n{__title__} v{__version__}")
    print(f"Author: {__author__}")
    print(f"\n{__description__}\n")
    
    # Show availability
    status = check_modules_availability()
    print("Module Availability:")
    for module, available in status.items():
        if module != 'all_available':
            icon = "✓" if available else "✗"
            print(f"  {icon} {module.capitalize()}")
    
    # Show examples
    print("\nFor usage examples, run:")
    print("  from modules import print_examples")
    print("  print_examples()")
