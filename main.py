import os
import httpx
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

# আপনার AlienVault Key
REAL_KEY = "78e6adcc9f7f6135d2dcb2cc802f5b444dbf80d7aaf734b61a6e151be37e2004"

# আপনার নিজের বানানো পাসওয়ার্ড
MY_KEY = "moseur777"

@app.get("/")
def home():
    return {"message": "API is working!"}

@app.get("/osint/{domain}")
async def get_data(domain: str, x_api_key: str = Header(None)):
    # পাসওয়ার্ড চেক
    if x_api_key != MY_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key. Access Denied.")
    
    # AlienVault থেকে ডেটা আনা
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general"
    
    # এই হেডারটাই AlienVault-এর জন্য সঠিক
    headers = {"X-OTX-API-KEY": REAL_KEY.strip()} 
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # AlienVault থেকে এরর আসলে ধরবে
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"AlienVault API Error: {e.response.status_code}", "details": e.response.text}
    except Exception as e:
        return {"error": "Internal Server Error", "details": str(e)}
