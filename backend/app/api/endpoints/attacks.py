from fastapi import APIRouter
from ...services.data_fetcher import DataFetcher
import joblib
import pandas as pd
import os

router = APIRouter()
data_fetcher = DataFetcher()

# Load the trained model and encoder when the API starts
model_path = os.path.join("/app", "app", "ml", "models", "ddos_classifier.pkl")
encoder_path = os.path.join("/app", "app", "ml", "models", "country_encoder.pkl")

# Use a try-except block to handle cases where the model files might not exist yet
try:
    classifier = joblib.load(model_path)
    encoder = joblib.load(encoder_path)
    print("ML model and encoder loaded successfully.")
except FileNotFoundError:
    print("Warning: ML model files not found. Please run trainer.py first.")
    classifier = None
    encoder = None

@router.get("/attacks")
def get_attacks():
    abuseipdb_data = data_fetcher.fetch_abuseipdb_data()
    cloudflare_data = data_fetcher.fetch_cloudflare_data()
    cloudflare_geo_data = data_fetcher.fetch_cloudflare_geo_data()

    # Apply ML model if it's loaded and data is available
    if classifier and abuseipdb_data and not "error" in abuseipdb_data:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(abuseipdb_data)
        
        # Select the features for prediction
        X_to_predict = df[['abuseConfidenceScore', 'countryCode']]
        
        # One-hot encode the countryCode using the saved encoder
        country_encoded = encoder.transform(X_to_predict[['countryCode']]).toarray()
        country_feature_names = encoder.get_feature_names_out(['countryCode'])
        
        # Combine and predict
        X_final = pd.concat([X_to_predict[['abuseConfidenceScore']], 
                           pd.DataFrame(country_encoded, columns=country_feature_names)], axis=1)
        
        # Make predictions and get confidence scores
        predictions = classifier.predict(X_final)
        confidence_scores = classifier.predict_proba(X_final)[:, 1]

        # Add predictions and confidence to the original data
        df['isDDoS_prediction'] = predictions
        df['ddos_confidence'] = confidence_scores
        
        # Update the response with the new, enhanced data
        abuseipdb_data = df.to_dict('records')

    return {
        "message": "Attack data fetched successfully!",
        "abuseipdb_data": abuseipdb_data,
        "cloudflare_data": cloudflare_data,
        "cloudflare_geo_data": cloudflare_geo_data
    }