# In backend/app/ml/trainer.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
import joblib
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

# Add the project's root directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.services.data_fetcher import DataFetcher

def create_mixed_data(live_data):
    # Live data typically contains only high-confidence scores.
    # We'll mix it with a small sample of low-confidence IPs to ensure the model trains on both classes.
    sample_data = {
        'ipAddress': ['1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4', '5.5.5.5'],
        'countryCode': ['US', 'DE', 'FR', 'CN', 'GB'],
        'abuseConfidenceScore': [10, 20, 30, 40, 50],
        'lastReportedAt': [datetime.utcnow().isoformat() for _ in range(5)]
    }
    sample_df = pd.DataFrame(sample_data)
    live_df = pd.DataFrame(live_data)
    
    # Combine the dataframes
    return pd.concat([live_df, sample_df], ignore_index=True)


def train_model():
    print("Starting model training with mixed data...")
    
    # Step 1: Data Preparation - Fetch live data and mix it with sample data
    data_fetcher = DataFetcher()
    abuseipdb_data = data_fetcher.fetch_abuseipdb_data()

    if not abuseipdb_data or "error" in abuseipdb_data:
        print("Error: Could not fetch data from AbuseIPDB. Training aborted.")
        print(abuseipdb_data)
        return
        
    df = create_mixed_data(abuseipdb_data)

    # Step 2: Feature Engineering - Create a target variable
    df['isDDoS'] = df['abuseConfidenceScore'].apply(lambda x: 1 if x > 90 else 0)

    # Separate features and target
    X = df[['abuseConfidenceScore', 'countryCode']]
    y = df['isDDoS']
    
    # One-Hot Encoding for countryCode
    encoder = OneHotEncoder(handle_unknown='ignore')
    country_encoded = encoder.fit_transform(X[['countryCode']]).toarray()
    country_feature_names = encoder.get_feature_names_out(['countryCode'])
    
    # Combine numerical features and encoded country features
    X_final = pd.concat([df[['abuseConfidenceScore']], 
                         pd.DataFrame(country_encoded, columns=country_feature_names)], axis=1)

    # Step 3: Train the Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_final, y)

    # Step 4: Save the trained model and encoder
    model_dir = "backend/app/ml/models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    joblib.dump(model, os.path.join(model_dir, 'ddos_classifier.pkl'))
    joblib.dump(encoder, os.path.join(model_dir, 'country_encoder.pkl'))

    print("Model training complete. Model saved.")
    
if __name__ == "__main__":
    train_model()