import os
from config import DEV_TO_API_URL

class DevToService:
    """
    Service to interact with the Dev.to API.
    """
    def __init__(self):
        self.api_url = DEV_TO_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "api-key": os.getenv("DEV_TO_API_KEY"),  # Ensure this is set in your environment
            "Cache-Control": "max-age=604800, must-revalidate"
        }

    def get_articles(self):
        """
        Fetch articles from the Dev.to API.
        """
        import requests
        
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[DevToService][get_articles] >> Error fetching articles: {e}")
            return None
        
        