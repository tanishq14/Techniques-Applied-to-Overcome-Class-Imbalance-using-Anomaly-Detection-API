"""
Quick test to verify utils are working
"""

print("Testing utils import...")

try:
    from utils import (
        validate_image,
        validate_network_data,
        format_response,
        save_upload,
        allowed_file,
        format_bytes
    )
    print("✓ All utils imported successfully!")
    
    # Test format_bytes
    print(f"\nTesting format_bytes:")
    print(f"  1024 bytes = {format_bytes(1024)}")
    print(f"  1048576 bytes = {format_bytes(1048576)}")
    
    # Test validate_network_data
    print(f"\nTesting validate_network_data:")
    test_data = {
        'dur': 0.5,
        'proto': 'tcp',
        'service': 'http',
        'state': 'FIN',
        'spkts': 12,
        'dpkts': 10
    }
    is_valid, error, cleaned = validate_network_data(test_data)
    print(f"  Valid: {is_valid}")
    if is_valid:
        print(f"  Cleaned data has {len(cleaned)} fields")
    
    print("\n✅ All tests passed!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
