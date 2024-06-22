import base64
import httpx
from .config import CLIENT_ID, CLIENT_SECRET, TOKEN_URL, TSG_ID

def get_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_str.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'client_credentials',
        'scope': f'tsg_id:{TSG_ID}'
    }
    
    response = httpx.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()
    token = response.json().get('access_token')
    return token

def get_headers():
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    return headers
