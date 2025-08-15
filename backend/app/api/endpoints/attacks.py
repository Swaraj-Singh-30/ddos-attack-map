from fastapi import APIRouter
from ...services.data_fetcher import DataFetcher

router = APIRouter()
data_fetcher = DataFetcher()

@router.get("/attacks")
def get_attacks():
    # Fetch time-series data from AbuseIPDB and Cloudflare
    abuseipdb_data = data_fetcher.fetch_abuseipdb_data()
    cloudflare_data = data_fetcher.fetch_cloudflare_data()
    
    # NEW: Fetch geographical data from Cloudflare
    cloudflare_geo_data = data_fetcher.fetch_cloudflare_geo_data()

    # Return a combined response with all the data
    return {
        "message": "Attack data fetched successfully!",
        "abuseipdb_data": abuseipdb_data,
        "cloudflare_data": cloudflare_data,
        "cloudflare_geo_data": cloudflare_geo_data
    }