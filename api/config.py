import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine the environment
is_production = os.getenv("ENV") == "production" or os.getenv("VERCEL") == "1"