import os

def check_models():
    required_models = {
        'network': [
            'column_transformer.pkl',
            'isolation_forest.pkl',
            'ocsvm.pkl',
            'lof.pkl'
        ],
        'mvtec': [
            'resnet_feature_extractor.pt',
            'scaler.pkl',
            'isolation_forest.pkl',
            'ocsvm.pkl',
        ],
        'xray': [
            'autoencoder.pt',
            'isolation_forest.pkl',
            'dt_model.pkl',
            'knn_model.pkl'
        ]
    }
    
    print("📁 Checking model files...\n")
    
    for dataset, files in required_models.items():
        print(f"=== {dataset.upper()} ===")
        for file in files:
            path = f"models/{dataset}/{file}"
            exists = "✅" if os.path.exists(path) else "❌"
            print(f"{exists} {file}")
        print()

if __name__ == '__main__':
    check_models()
