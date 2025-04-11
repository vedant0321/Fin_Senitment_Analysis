import requests
import os
import time
from typing import List, Dict, Any, Optional

class FinancialNewsClient:
    def __init__(self, api_key="put your api key"):
        self.api_key = api_key or os.environ.get("None")
        if not self.api_key:
            raise ValueError("Finnhub API key is required. Set it in the FINNHUB_API_KEY environment variable.")
        self.base_url = "https://finnhub.io/api/v1"
        
    def get_company_news(self, ticker: str, from_date: str, to_date: str, limit: Optional[int] = 50) -> List[Dict[str, Any]]:
        """Retrieve news for a specific company ticker within a date range."""
        endpoint = f"{self.base_url}/company-news"
        params = {
            "symbol": ticker,
            "from": from_date,
            "to": to_date,
            "token": self.api_key
        }
        
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                response = requests.get(endpoint, params=params, timeout=10)
                
                if response.status_code == 429:  # Rate limit exceeded
                    retry_after = int(response.headers.get('Retry-After', 60))
                    if attempt < max_retries - 1:
                        time.sleep(retry_after)
                        continue
                
                if response.status_code != 200:
                    error_msg = f"API request failed with status code {response.status_code}"
                    try:
                        error_details = response.json()
                        error_msg += f": {error_details}"
                    except:
                        error_msg += f": {response.text}"
                    raise Exception(error_msg)
                
                # Check for valid JSON response
                try:
                    news_items = response.json()
                except Exception as e:
                    raise Exception(f"Failed to parse API response: {str(e)}")
                
                # Handle empty response
                if not news_items:
                    return []
                
                # Make sure response is a list of news items
                if not isinstance(news_items, list):
                    raise Exception(f"Unexpected API response format: {news_items}")
                
                # Limit the number of news items if necessary
                return news_items[:limit] if limit else news_items
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise Exception(f"Failed to connect to Finnhub API after {max_retries} attempts: {str(e)}")
        
        return []  
