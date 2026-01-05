from PIL import Image
import os
import sys

# ensure upload dir
os.makedirs('static/uploads', exist_ok=True)
img_path = 'static/uploads/test_mvtec_direct.png'
Image.new('L', (224,224), color=128).save(img_path)
print('Saved image:', img_path)

try:
    # ensure project root is on sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from modules import predict_mvtec
    res = predict_mvtec(img_path)
    import json
    print('Prediction result:')
    print(json.dumps(res, indent=2))
except Exception as e:
    import traceback
    print('Prediction raised exception:')
    traceback.print_exc()
