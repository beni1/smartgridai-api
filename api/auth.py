from fastapi import Header, HTTPException
from api.keys import API_KEYS

def verify_api_key(x_api_key: str = Header(None)):
    print("Received key:", x_api_key)  # ✅ MOVE IT HERE

    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key missing")

    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return x_api_key, API_KEYS[x_api_key]
