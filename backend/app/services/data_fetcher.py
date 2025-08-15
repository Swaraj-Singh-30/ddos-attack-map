import requests
import os
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self):
        # Retrieve API keys from environment variables
        self.abuseipdb_api_key = os.getenv("ABUSEIPDB_API_KEY")
        self.cloudflare_api_token = os.getenv("CLOUDFLARE_API_TOKEN")

        # Define API endpoints
        self.abuseipdb_url = "https://api.abuseipdb.com/api/v2/blacklist"
        self.cloudflare_url = "https://api.cloudflare.com/client/v4/radar/attacks/layer3/timeseries"
        
        # Updated: Layer 7 Top Locations (Origin)
        self.cloudflare_geo_url = "https://api.cloudflare.com/client/v4/radar/attacks/layer7/top/locations/origin"
        
        print(f"Loaded Cloudflare Token: {self.cloudflare_api_token}")

    def fetch_abuseipdb_data(self):
        """Fetches a list of reported malicious IPs from AbuseIPDB."""
        if not self.abuseipdb_api_key:
            return {"error": "AbuseIPDB API key not found"}

        headers = {
            'Accept': 'application/json',
            'Key': self.abuseipdb_api_key
        }
        
        params = {
            'limit': 100,
            'confidenceMinimum': 90
        }

        try:
            response = requests.get(self.abuseipdb_url, headers=headers, params=params)
            print(f"AbuseIPDB Response Status: {response.status_code}")
            if response.status_code != 200:
                print(f"AbuseIPDB Response Body: {response.text}")
            
            response.raise_for_status()
            return response.json()['data']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching AbuseIPDB data: {e}")
            return {"error": "Failed to fetch AbuseIPDB data"}

    def fetch_cloudflare_data(self):
        """Fetches high-level DDoS attack data from Cloudflare Radar."""
        if not self.cloudflare_api_token:
            return {"error": "Cloudflare API token not found"}

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.cloudflare_api_token}'
        }

        params = {
            'location': 'IN',
            'dateRange': '7d'
        }

        try:
            response = requests.get(self.cloudflare_url, headers=headers, params=params)
            print(f"Cloudflare Response Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Cloudflare Response Body: {response.text}")

            response.raise_for_status()
            return response.json()['result']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Cloudflare data: {e}")
            return {"error": "Failed to fetch Cloudflare data"}

    def fetch_cloudflare_geo_data(self):
        """Fetches Layer 7 DDoS attack origin locations from Cloudflare Radar."""
        if not self.cloudflare_api_token:
            return {"error": "Cloudflare API token not found"}

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.cloudflare_api_token}'
        }

        date_end = datetime.utcnow()
        date_start = date_end - timedelta(days=7)

        params = {
            'dateStart': date_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'dateEnd': date_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'limit': 20
        }

        try:
            print(f"Cloudflare Geo URL: {self.cloudflare_geo_url}")
            print(f"Cloudflare Geo Params: {params}")
            response = requests.get(self.cloudflare_geo_url, headers=headers, params=params)
            print(f"Cloudflare Geo Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Cloudflare Geo Body: {response.text}")
            response.raise_for_status()
            return response.json()['result']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Cloudflare geo data: {e}")
            return {"error": "Failed to fetch Cloudflare geo data"}
