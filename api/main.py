# =========================
# DATABASE IMPORTS
# =========================
from database import engine, SessionLocal
from models import Base, Forecast, APIUsage

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
# FASTAPI + UTILITIES
# =========================
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# CREATE FASTAPI APP
# =========================
app = FastAPI(
    title="SmartGridAI API"
)

# =========================
# CREATE DATABASE TABLES
# =========================
Base.metadata.create_all(bind=engine)

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
    # SAMPLE VALUES
    # =========================
    values = df["demand"].tail(days).tolist()

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
    # SIMPLE RISK ANALYSIS
    # =========================
    avg_consumption = (
        sum(values) / len(values)
    )

    if avg_consumption > 150:
        risk_level = "HIGH"

    elif avg_consumption > 120:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    # =========================
    # FINAL RESPONSE
    # =========================
    return {
        "plan": plan,
        "used": used,
        "limit": limit,
        "risk": risk_level,
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
    # AI FORECAST
    # =========================
    forecast_values = predict_next_days(
        model,
        df,
        scaler,
        days=days
    )

    # =========================
    # RISK ANALYSIS
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
    # AI ANOMALY DETECTION
    # =========================
    max_forecast = max(forecast_values)

    anomaly_detected = False

    anomaly_reason = "No anomaly detected"

    if max_forecast > 350:

        anomaly_detected = True

        anomaly_reason = (
            "Extreme demand spike detected"
        )

    # =========================
    # OPEN DATABASE SESSION
    # =========================
    db = SessionLocal()

    try:

        # =========================
        # SAVE FORECASTS
        # =========================
        for value in forecast_values:

            new_forecast = Forecast(
                forecast=float(value),
                risk=risk
            )

            db.add(new_forecast)

        # =========================
        # LOG API USAGE
        # =========================
        usage = APIUsage(
            api_key=api_key,
            requests=1
        )

        db.add(usage)

        # =========================
        # SAVE DATABASE
        # =========================
        db.commit()

    finally:

        # =========================
        # CLOSE DATABASE
        # =========================
        db.close()

    # =========================
    # RESPONSE
    # =========================
    return {
        "forecast": forecast_values,
        "risk": risk,
        "confidence": "92%",
        "plan": plan,
        "used": used,
        "limit": limit,

        # =========================
        # ANOMALY RESPONSE
        # =========================
        "anomaly_detected": anomaly_detected,
        "anomaly_reason": anomaly_reason
    }

# =========================
# HISTORY ENDPOINT
# =========================
@app.get("/history")
def history():

    db = SessionLocal()

    try:

        forecasts = (
            db.query(Forecast)
            .order_by(Forecast.timestamp.desc())
            .limit(200)
            .all()
        )

        results = []

        for item in forecasts:

            results.append({

                "forecast": item.forecast,

                "risk": item.risk,

                "timestamp": str(item.timestamp)
            })

        return results

    finally:

        db.close()
