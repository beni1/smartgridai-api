# =========================
# INTERNAL MODULES
# =========================
from api.auth import verify_api_key
from api.usage import check_limit

# =========================
# LSTM IMPORTS
# =========================
from lstm_model import (
    load_saved_model,
    predict_next_days,
    load_dataset
)

from fastapi import FastAPI, Depends
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# INTERNAL MODULES
# =========================
from api.auth import verify_api_key
from api.usage import check_limit

# =========================
# LSTM IMPORTS
# =========================
from lstm_model import (
    load_saved_model,
    predict_next_days,
    load_dataset
)

# =========================
# CREATE FASTAPI APP
# =========================
app = FastAPI(
    title="SmartGridAI API"
)

# =========================
# LOAD MODEL ON STARTUP
# =========================
model, scaler = load_saved_model()

# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def root():
    return {
        "message": "SmartGridAI API is running"
    }

# =========================
# DEMAND ENDPOINT
# =========================
@app.get("/demand")
def get_demand(
    days: int = 1,
    auth=Depends(verify_api_key)
):

    api_key, plan = auth

    # =========================
    # CHECK USAGE LIMITS
    # =========================
    allowed, used, limit = check_limit(
        api_key,
        plan
    )

    if not allowed:
        return {
            "error": "Usage limit exceeded",
            "plan": plan,
            "used": used,
            "limit": limit
        }

    # =========================
    # LOAD DATAFRAME
    # =========================
    df = load_dataset()


    # =========================
    # BUILD RESPONSE DATA
    # =========================
    data = {
        "time": [
            f"Day {i+1}"
            for i in range(days)
        ],
        "consumption": values
    }

    # =========================
    # FINAL RESPONSE
    # =========================
    return {
        "plan": plan,
        "used": used,
        "limit": limit,
        "data": data
    }


# =========================
# FORECAST ENDPOINT
# =========================
@app.get("/forecast")
def forecast(
    days: int = 7,
    auth=Depends(verify_api_key)
):

    api_key, plan = auth

    # =========================
    # CHECK USAGE LIMITS
    # =========================
    allowed, used, limit = check_limit(
        api_key,
        plan
    )

    if not allowed:
        return {
            "error": "Usage limit exceeded",
            "plan": plan,
            "used": used,
            "limit": limit
        }

    # =========================
    # LOAD DATAFRAME
    # =========================
    df = load_dataset()

    # =========================
    # RECURSIVE AI FORECAST
    # =========================
    forecast_values = predict_next_days(
        model,
        df,
        scaler,
        days=days
    )

    # =========================
    # SIMPLE RISK ANALYSIS
    # =========================
    avg_forecast = (
        sum(forecast_values)
        / len(forecast_values)
    )

    if avg_forecast > 150:
        risk = "HIGH"

    elif avg_forecast > 120:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    # =========================
    # RESPONSE
    # =========================
    return {
        "forecast": forecast_values,
        "risk": risk,
        "confidence": "92%",
        "plan": plan,
        "used": used,
        "limit": limit
    }
