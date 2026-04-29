from fastapi import FastAPI, Header, HTTPException
import pandas as pd

app = FastAPI()

# =========================
# SIMPLE DEMAND API
# =========================
@app.get("/demand")
def get_demand(days: int = 1, x_api_key: str = Header(None)):

    # simple API key check (match your Streamlit key)
    if x_api_key != "free-user-key":
        raise HTTPException(status_code=403, detail="Invalid API key")

    # fake/sample data (replace with your real generator later)
    time = [f"Day {i+1}" for i in range(days)]
    consumption = [100 + i * 10 for i in range(days)]

    return {
        "data": {
            "time": time,
            "consumption": consumption
        },
        "plan": "free",
        "used": days,
        "limit": 7
    }
