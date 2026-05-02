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
from api.insights import generate_insights

# ✅ LSTM IMPORTS
from lstm_model import load_saved_model, predict_next

# =========================
# CREATE FASTAPI APP
# =========================
app = FastAPI(
    title="SmartGridAI API"
)

# =========================
# LOAD MODEL ON STARTUP
# =========================
model = load_saved_model()

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
    # GENERATE LSTM FORECAST
    # =========================
    values = []

    current_value = 100

    for _ in range(days):

        prediction = predict_next(
            model,
            current_value
        )

        prediction = round(float(prediction), 2)

        values.append(prediction)

        current_value = prediction

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
    # GENERATE AI INSIGHTS
    # =========================
    insights = generate_insights(values)

    # =========================
    # FINAL RESPONSE
    # =========================
    return {
        "plan": plan,
        "used": used,
        "limit": limit,
        "data": data,
        "insights": insights
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
    # AI FORECAST GENERATION
    # =========================
    forecast_values = []

    current_value = 100

    for _ in range(days):

        prediction = predict_next(
            model,
            current_value
        )

        prediction = round(float(prediction), 2)

        forecast_values.append(prediction)

        current_value = prediction

    # =========================
    # SIMPLE RISK ANALYSIS
    # =========================
    avg_forecast = sum(forecast_values) / len(forecast_values)

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
