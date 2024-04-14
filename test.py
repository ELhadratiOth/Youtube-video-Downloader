import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

print(os.getenv('MY_SECRET_KEY'))