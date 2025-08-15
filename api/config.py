import os
from dotenv import load_dotenv

# Load environment variables only in local development
if not os.getenv("VERCEL"):
    load_dotenv()

# Environment detection
is_production = os.getenv("ENV") == "production" or os.getenv("VERCEL") == "1"