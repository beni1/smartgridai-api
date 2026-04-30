from fastapi import FastAPI, Header, HTTPException
import pandas as pd

app = FastAPI()

# =========================
# SIMPLE DEMAND API
# =========================
@app.get("/demand")
def get_demand(days: int = 1, x_api_key: str = Header(None)):

    # =========================
    # 🔐 API KEY CHECK
    # =========================
    if x_api_key != "free-user-key":
        raise HTTPException(status_code=403, detail="Invalid API key")

    # =========================
    # 📊 DATA GENERATION
    # =========================
    time = [f"Day {i+1}" for i in range(days)]
    consumption = [100 + i * 10 for i in range(days)]

    # =========================
    # 🔹 STEP 1 — VALUE LAYER
    # =========================
    max_demand = max(consumption)
    avg_demand = sum(consumption) / len(consumption)

    if max_demand > 130:
        peak_risk = "HIGH"
        recommendation = "Shift usage away from peak hours (6–8pm)"
        cost_impact = "INCREASED COST RISK"
    else:
        peak_risk = "LOW"
        recommendation = "Normal operation"
        cost_impact = "STABLE COST"

    # =========================
    # 🔹 STEP 2 — ALERT LAYER
    # =========================
    alert = "NORMAL"

    if max_demand > 140:
        alert = "⚠ CRITICAL: Overload risk"
    elif max_demand > 130:
        alert = "⚠ WARNING: High demand detected"

    # =========================
    # 🔹 STEP 3 — COST SAVINGS LAYER
    # =========================
    estimated_cost = round(sum(consumption) * 0.12, 2)

    savings_tip = "No optimization needed"

    if peak_risk == "HIGH":
        savings_tip = "Shift load to off-peak hours → save 8–15% cost"

    # =========================
    # 🚀 STEP 4 — FINAL RESPONSE
    # =========================
    return {
        "data": {
            "time": time,
            "consumption": consumption
        },
        "insights": {
            "peak_risk": peak_risk,
            "alert": alert,
            "cost_impact": cost_impact,
            "recommendation": recommendation,
            "estimated_cost": estimated_cost,
            "savings_tip": savings_tip
        },
        "plan": "free",
        "used": days,
        "limit": 7
    }
