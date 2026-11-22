import os
import httpx
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

REAL_KEY = "78e6adcc9f7f6135d2dcb2cc802f5b444dbf80d7aaf734b61a6e151be37e2004"
MY_KEY = "moseur777"

@app.get("/")
def home():
    return {"message": "API is working!"}

@app.get("/osint/{domain}")
async def get_data(domain: str, x_api_key: str = Header(None)):
    if x_api_key != MY_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key. Access Denied.")
    
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general"
    headers = {"X-OTX-API-KEY": REAL_KEY}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()
