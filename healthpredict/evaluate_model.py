import os
import sys
import pandas as pd
import numpy as np
import torch
from sklearn.metrics import r2_score, mean_absolute_error

# Add path
sys.path.append(os.getcwd())
try:
    from healthpredict.predictor.ml_models import health_predictor
except ImportError:
    sys.path.append(os.path.join(os.getcwd(), 'healthpredict'))
    from predictor.ml_models import health_predictor

def evaluate():
    print("Evaluating model accuracy...")
    
    # Load test data
    if os.path.exists('healthpredict/test_data.csv'):
        data = pd.read_csv('healthpredict/test_data.csv')
    elif os.path.exists('test_data.csv'):
        data = pd.read_csv('test_data.csv')
    else:
        print("Test data not found!")
        return

    # Prepare targets
    target_cols = ['heart_disease_risk', 'diabetes_risk', 'cancer_risk']
    # Note: stroke_risk might be missing in test_data, so we skip it or calculate it
    if 'stroke_risk' in data.columns:
        target_cols.append('stroke_risk')
    
    y_true = data[target_cols].values
    y_pred = []
    
    # Predict
    for _, row in data.iterrows():
        # Convert row to dict
        row_dict = row.to_dict()
        result = health_predictor.predict_health_risks(row_dict)
        
        preds = [result[f'{col}'] for col in target_cols]
        y_pred.append(preds)
        
    y_pred = np.array(y_pred)
    
    # Calculate metrics
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # Accuracy estimation: 100 - MAE (since risks are 0-100)
    accuracy = 100 - mae
    
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R2 Score: {r2:.4f}")
    print(f"Estimated Accuracy (100 - MAE): {accuracy:.2f}%")

if __name__ == "__main__":
    evaluate()
