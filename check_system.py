"""
============================================================================
ANOMALY DETECTION API - SYSTEM CHECK
============================================================================
Diagnostic script to verify all components are working correctly
Run this before starting the API to ensure everything is configured properly

Usage:
    python check_system.py
    python check_system.py --verbose
    python check_system.py --fix  # Attempt to fix common issues
============================================================================
"""

import sys
import os
from pathlib import Path
import argparse

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}")
    print(f"{text}")
    print(f"{'='*80}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    print(f"  {text}")

# ============================================================================
# DEPENDENCY CHECKS
# ============================================================================

def check_python_version():
    """Check if Python version is adequate"""
    print_header("Checking Python Version")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} (Required: 3.8+)")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("Checking Python Dependencies")
    
    required = {
        'flask': 'Flask',
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'sklearn': 'Scikit-learn',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'PIL': 'Pillow',
        'scipy': 'SciPy'
    }
    
    missing = []
    installed = []
    
    for package, name in required.items():
        try:
            mod = __import__(package)
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{name}: {version}")
            installed.append(name)
        except ImportError:
            print_error(f"{name}: Not installed")
            missing.append(package)
    
    if missing:
        print_warning(f"\nMissing packages: {', '.join(missing)}")
        print_info("Install with: pip install " + " ".join(missing))
        return False
    
    return True

# ============================================================================
# FILE STRUCTURE CHECKS
# ============================================================================

def check_directory_structure():
    """Verify required directories exist"""
    print_header("Checking Directory Structure")
    
    required_dirs = {
        'modules': 'Pipeline modules',
        'models': 'Trained models',
        'templates': 'HTML templates',
        'static/css': 'CSS files',
        'static/js': 'JavaScript files',
        'uploads': 'Upload directory'
    }
    
    all_exist = True
    
    for directory, description in required_dirs.items():
        path = Path(directory)
        if path.exists() and path.is_dir():
            print_success(f"{directory}/ - {description}")
        else:
            print_error(f"{directory}/ - Missing ({description})")
            all_exist = False
    
    return all_exist

def check_required_files():
    """Check if critical files exist"""
    print_header("Checking Required Files")
    
    critical_files = {
        'app.py': 'Flask application',
        'modules/__init__.py': 'Module package',
        'modules/network_pipeline.py': 'Network pipeline',
        'modules/mvtec_pipeline.py': 'MVTec pipeline',
        'modules/xray_pipeline.py': 'X-ray pipeline',
        'templates/index.html': 'Homepage',
        'static/css/style.css': 'Stylesheet',
        'static/js/main.js': 'JavaScript'
    }
    
    all_exist = True
    
    for filepath, description in critical_files.items():
        path = Path(filepath)
        if path.exists() and path.is_file():
            size_kb = path.stat().st_size / 1024
            print_success(f"{filepath} - {description} ({size_kb:.1f} KB)")
        else:
            print_error(f"{filepath} - Missing ({description})")
            all_exist = False
    
    return all_exist

# ============================================================================
# MODEL CHECKS
# ============================================================================

def check_models():
    """Check if trained models exist"""
    print_header("Checking Trained Models")
    
    model_dirs = {
        'models/network': ['isolation_forest.pkl', 'ocsvm.pkl', 'elliptic_envelope.pkl', 'lof.pkl'],
        'models/mvtec': ['resnet_feature_extractor.pt', 'isolation_forest.pkl', 'ocsvm.pkl'],
        'models/xray': ['autoencoder.pt', 'isolation_forest.pkl', 'dt_model.pkl', 'knn_model.pkl']
    }
    
    all_models = []
    missing_models = []
    
    for directory, models in model_dirs.items():
        dir_path = Path(directory)
        print_info(f"\n{directory}:")
        
        if not dir_path.exists():
            print_error(f"  Directory not found")
            missing_models.extend(models)
            continue
        
        for model_file in models:
            model_path = dir_path / model_file
            if model_path.exists():
                size_mb = model_path.stat().st_size / (1024 * 1024)
                print_success(f"  {model_file} ({size_mb:.2f} MB)")
                all_models.append(model_file)
            else:
                print_error(f"  {model_file} - Missing")
                missing_models.append(model_file)
    
    if missing_models:
        print_warning(f"\n⚠ Missing {len(missing_models)} model files")
        print_info("Models must be trained before API can function")
        return False
    
    return True

# ============================================================================
# MODULE LOADING CHECKS
# ============================================================================

def check_module_imports():
    """Try importing all pipeline modules"""
    print_header("Testing Module Imports")
    
    all_imported = True
    
    try:
        print_info("Importing modules package...")
        from modules import (
            predict_network, predict_mvtec, predict_xray,
            check_modules_availability
        )
        print_success("modules package imported")
        
        # Check availability
        status = check_modules_availability()
        
        for module_name, available in status.items():
            if module_name == 'all_available':
                continue
            
            if available:
                print_success(f"{module_name}_pipeline: Available")
            else:
                print_error(f"{module_name}_pipeline: Failed to load")
                all_imported = False
        
    except ImportError as e:
        print_error(f"Import failed: {e}")
        all_imported = False
    
    return all_imported

# ============================================================================
# API FUNCTIONALITY CHECKS
# ============================================================================

def check_flask_app():
    """Check if Flask app can be initialized"""
    print_header("Testing Flask Application")
    
    try:
        from app import app
        print_success("Flask app imported successfully")
        
        # Check configuration
        print_info(f"Upload folder: {app.config.get('UPLOAD_FOLDER', 'Not set')}")
        print_info(f"Max file size: {app.config.get('MAX_CONTENT_LENGTH', 0) / (1024*1024):.0f} MB")
        print_info(f"Debug mode: {app.config.get('DEBUG', False)}")
        
        # Check routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print_info(f"Registered routes: {len(routes)}")
        
        return True
    except Exception as e:
        print_error(f"Flask app check failed: {e}")
        return False

# ============================================================================
# FIX COMMON ISSUES
# ============================================================================

def fix_common_issues():
    """Attempt to fix common setup issues"""
    print_header("Attempting to Fix Common Issues")
    
    # Create missing directories
    required_dirs = ['modules', 'models', 'templates', 'static/css', 'static/js', 'uploads']
    for directory in required_dirs:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created directory: {directory}/")
    
    # Create model subdirectories
    model_dirs = ['models/network', 'models/mvtec', 'models/xray']
    for directory in model_dirs:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created directory: {directory}/")
    
    print_info("\nNote: You still need to:")
    print_info("  1. Train and save models to models/ directory")
    print_info("  2. Install missing Python packages")

# ============================================================================
# MAIN CHECK ROUTINE
# ============================================================================

def run_all_checks(verbose=False):
    """Run all system checks"""
    print(f"\n{Colors.BOLD}ANOMALY DETECTION API - SYSTEM CHECK{Colors.END}")
    print(f"Diagnostic tool to verify system configuration\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_required_files),
        ("Trained Models", check_models),
        ("Module Imports", check_module_imports),
        ("Flask App", check_flask_app)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_error(f"Check '{check_name}' failed with exception: {e}")
            results.append((check_name, False))
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        if result:
            print_success(f"{check_name}")
        else:
            print_error(f"{check_name}")
    
    print(f"\n{Colors.BOLD}Score: {passed}/{total} checks passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All checks passed! System is ready.{Colors.END}")
        print(f"\nYou can now start the API with:")
        print(f"  {Colors.BLUE}python app.py{Colors.END}\n")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please fix issues above.{Colors.END}\n")
        return False

# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='System check for Anomaly Detection API',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output'
    )
    
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Attempt to fix common issues'
    )
    
    args = parser.parse_args()
    
    if args.fix:
        fix_common_issues()
        print()
    
    success = run_all_checks(verbose=args.verbose)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
