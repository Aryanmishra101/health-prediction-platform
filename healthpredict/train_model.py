import os
import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
import joblib
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the current directory to the path to import predictor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from predictor.ml_models import HealthRiskNN
except ImportError:
    # Fallback if running from root
    sys.path.append(os.path.join(os.getcwd(), 'healthpredict'))
    from predictor.ml_models import HealthRiskNN

class HealthDataset(Dataset):
    def __init__(self, features, targets):
        self.features = torch.FloatTensor(features)
        self.targets = torch.FloatTensor(targets)
        
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]

def train_model():
    logger.info("Starting model training process...")
    
    # 1. Load Data
    data_files = [
        'health_prediction_data.csv',
        'training_data.csv',
        'test_data.csv'
    ]
    
    dfs = []
    for file in data_files:
        if os.path.exists(file):
            logger.info(f"Loading {file}...")
            dfs.append(pd.read_csv(file))
        else:
            logger.warning(f"File {file} not found, skipping.")
            
    if not dfs:
        logger.error("No data files found!")
        return
        
    full_data = pd.concat(dfs, ignore_index=True)
    logger.info(f"Total samples: {len(full_data)}")
    
    # 2. Preprocessing
    # Define features (must match HealthPredictor)
    numeric_features = [
        'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature',
        'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
        'fasting_glucose', 'hba1c', 'creatinine', 'hemoglobin',
        'stress_level', 'sleep_hours'
    ]
    
    categorical_features = [
        'gender', 'smoking_status', 'alcohol_consumption', 'exercise_level', 'family_medical_history'
    ]
    
    binary_features = [
        'chest_pain', 'shortness_of_breath', 'fatigue', 'frequent_urination',
        'excessive_thirst', 'unexplained_weight_loss', 'blurred_vision',
        'dizziness', 'palpitations'
    ]
    
    # Handle missing columns by filling with defaults
    for col in numeric_features:
        if col not in full_data.columns:
            full_data[col] = 0
    for col in categorical_features:
        if col not in full_data.columns:
            full_data[col] = 'none'
    for col in binary_features:
        if col not in full_data.columns:
            full_data[col] = False

    # Process Features
    processed_features = []
    
    # Numeric
    X_numeric = full_data[numeric_features].fillna(0).values
    
    # Categorical Mappings
    categorical_mappings = {
        'gender': {'male': 0, 'female': 1, 'other': 2},
        'smoking_status': {'never': 0, 'former': 1, 'current': 2},
        'alcohol_consumption': {'never': 0, 'occasional': 1, 'moderate': 2, 'heavy': 3},
        'exercise_level': {'sedentary': 0, 'light': 1, 'moderate': 2, 'vigorous': 3},
        'family_medical_history': {'none': 0, 'heart_disease': 1, 'diabetes': 2, 'cancer': 3, 'multiple': 4}
    }
    
    X_categorical = []
    for feature in categorical_features:
        mapping = categorical_mappings.get(feature, {})
        values = full_data[feature].map(lambda x: mapping.get(str(x).lower(), 0)).values
        X_categorical.append(values)
    X_categorical = np.column_stack(X_categorical)
    
    # Binary
    X_binary = []
    for feature in binary_features:
        # Handle string 'True'/'False' or actual booleans
        values = full_data[feature].astype(str).map(lambda x: 1 if x.lower() == 'true' else 0).values
        X_binary.append(values)
    X_binary = np.column_stack(X_binary)
    
    # Combine all features BEFORE scaling numeric
    # Wait, the predictor scales ALL features? No, let's check predictor code.
    # Predictor: features = numeric + categorical + binary. Then scaler.transform(features).
    # So we must combine first, then scale.
    
    X = np.hstack([X_numeric, X_categorical, X_binary])
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Targets
    target_cols = ['heart_disease_risk', 'diabetes_risk', 'cancer_risk', 'stroke_risk']
    
    # Calculate stroke_risk if missing (using rule-based logic approximation)
    if 'stroke_risk' not in full_data.columns:
        logger.info("Calculating missing stroke_risk based on heart and diabetes risks...")
        full_data['stroke_risk'] = full_data[['heart_disease_risk', 'diabetes_risk']].apply(
            lambda x: max(x['heart_disease_risk'] * 0.7, x['diabetes_risk'] * 0.6), axis=1
        )
        
    y = full_data[target_cols].fillna(0).values / 100.0  # Normalize to 0-1
    
    # 3. Train
    dataset = HealthDataset(X_scaled, y)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    input_size = X.shape[1]
    model = HealthRiskNN(input_size=input_size)
    
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 50
    logger.info(f"Training for {epochs} epochs...")
    
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            
            outputs = model(batch_X)
            
            # Combine outputs into tensor [batch, 4]
            pred = torch.cat([
                outputs['heart_disease'],
                outputs['diabetes'],
                outputs['cancer'],
                outputs['stroke']
            ], dim=1)
            
            loss = criterion(pred, batch_y)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        if (epoch + 1) % 10 == 0:
            logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
            
    # 4. Save
    save_dir = os.path.join('healthpredict', 'ml_models')
    os.makedirs(save_dir, exist_ok=True)
    
    # Save Model
    model_path = os.path.join(save_dir, 'health_risk_model.pth')
    torch.save({
        'model_state_dict': model.state_dict(),
        'input_size': input_size,
        'hidden_sizes': model.hidden_sizes,
        'dropout_rate': model.dropout_rate,
        'version': '2.0.0'
    }, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Save Scaler
    scaler_path = os.path.join(save_dir, 'feature_scaler.pkl')
    joblib.dump(scaler, scaler_path)
    logger.info(f"Scaler saved to {scaler_path}")
    
    # Save Feature Names
    feature_names = numeric_features + categorical_features + binary_features
    features_path = os.path.join(save_dir, 'feature_names.json')
    with open(features_path, 'w') as f:
        json.dump(feature_names, f)
    logger.info(f"Feature names saved to {features_path}")
    
    logger.info("Training complete!")

if __name__ == "__main__":
    train_model()
