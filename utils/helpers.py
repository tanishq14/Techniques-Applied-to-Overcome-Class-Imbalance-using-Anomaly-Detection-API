"""
============================================================================
HELPER FUNCTIONS
Utility functions for the Anomaly Detection API
============================================================================
"""

from werkzeug.utils import secure_filename
from flask import jsonify
from datetime import datetime
import os
import time

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'dcm', 'gif'}

def allowed_file(filename):
    """
    Check if file has an allowed extension
    
    Args:
        filename (str): Name of the file
        
    Returns:
        bool: True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image(file):
    """
    Validate uploaded image file
    
    Args:
        file: Flask FileStorage object
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size (basic check)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size == 0:
        return False, "File is empty"
    
    # Optional: Check max size (e.g., 16MB)
    max_size = 16 * 1024 * 1024  # 16MB
    if file_size > max_size:
        return False, f"File too large. Maximum size: {format_bytes(max_size)}"
    
    return True, None


def validate_network_data(data):
    """
    Validate network traffic data
    
    Args:
        data (dict): Input network features
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None, cleaned_data: dict or None)
    """
    # Minimum required fields for basic prediction
    required_fields = ['dur', 'proto', 'service', 'state']
    
    # Check required fields
    missing = [field for field in required_fields if field not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}", None
    
    # Clean and validate data
    try:
        cleaned_data = {
            # Basic required fields
            'dur': float(data.get('dur', 0)),
            'proto': str(data.get('proto', '')),
            'service': str(data.get('service', '')),
            'state': str(data.get('state', '')),
            
            # Common optional fields with defaults
            'spkts': int(data.get('spkts', 0)),
            'dpkts': int(data.get('dpkts', 0)),
            'sbytes': int(data.get('sbytes', 0)),
            'dbytes': int(data.get('dbytes', 0)),
            'rate': float(data.get('rate', 0)),
        }
        
        # Add all other optional fields if present (for full feature set)
        optional_fields = [
            'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss',
            'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb',
            'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean',
            'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src',
            'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm',
            'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login',
            'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm',
            'ct_srv_dst', 'is_sm_ips_ports'
        ]
        
        for field in optional_fields:
            if field in data:
                try:
                    cleaned_data[field] = float(data[field])
                except (ValueError, TypeError):
                    cleaned_data[field] = 0
        
        # Preserve preset information if exists
        if 'preset' in data:
            cleaned_data['preset'] = data['preset']
        
        return True, None, cleaned_data
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid data format: {str(e)}", None


def format_response(success, data=None, error=None, code=200):
    """
    Format standardized API response
    
    Args:
        success (bool): Whether the operation succeeded
        data (dict): Response data (if successful)
        error (str): Error message (if failed)
        code (int): HTTP status code
        
    Returns:
        tuple: (jsonified response, status code)
    """
    response = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
    }
    
    if success:
        response['data'] = data
    else:
        response['error'] = error
    
    return jsonify(response), code


def save_upload(file, upload_folder):
    """
    Save uploaded file securely with unique timestamp
    
    Args:
        file: Flask FileStorage object
        upload_folder (str): Directory to save file
        
    Returns:
        str: Path to saved file
    """
    # Secure the filename
    filename = secure_filename(file.filename)
    
    # Add timestamp to avoid collisions
    timestamp = int(time.time() * 1000)  # Millisecond precision
    name, ext = os.path.splitext(filename)
    unique_filename = f"{timestamp}_{name}{ext}"
    
    # Ensure upload folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    return filepath


def format_bytes(bytes_value):
    """
    Format bytes into human-readable format
    
    Args:
        bytes_value (int): Number of bytes
        
    Returns:
        str: Formatted string (e.g., "1.5 MB")
    """
    if bytes_value < 1024:
        return f"{bytes_value} B"
    elif bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.1f} KB"
    elif bytes_value < 1024 * 1024 * 1024:
        return f"{bytes_value / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_value / (1024 * 1024 * 1024):.1f} GB"
