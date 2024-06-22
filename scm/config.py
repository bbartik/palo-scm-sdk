import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BASE_URL = os.getenv('BASE_URL', 'https://api.sase.paloaltonetworks.com/sse/config/v1')
TOKEN_URL = os.getenv('TOKEN_URL', 'https://auth.apps.paloaltonetworks.com/oauth2/access_token')
TSG_ID = os.getenv('TSG_ID')
