import os
from dotenv import load_dotenv

# Load environment variables only in local development
if not os.getenv("VERCEL"):
    load_dotenv()

# Environment detection
is_production = os.getenv("ENV") == "production" or os.getenv("VERCEL") == "1"


# External URLS
DEV_TO_API_URL = "https://dev.to/api/articles/me"