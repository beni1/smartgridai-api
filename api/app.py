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
    # 🔥 SMART ALERT LOGIC (UPDATED)
    # =========================
    peak = max(consumption)
    avg = sum(consumption) / len(consumption)

    # 🔴 Dynamic thresholds
    if peak > 130:
        alert = "HIGH"
        peak_risk = "CRITICAL"
        cost_impact = "VERY HIGH COST"
        recommendation = "Reduce load immediately or activate backup supply"

    elif peak > 115:
        alert = "MEDIUM"
        peak_risk = "ELEVATED"
        cost_impact = "HIGH COST"
        recommendation = "Shift non-essential load to off-peak hours"

    else:
        alert = "LOW"
        peak_risk = "STABLE"
        cost_impact = "NORMAL COST"
        recommendation = "Normal operation"

    # =========================
    # 💰 COST MODEL (IMPROVED)
    # =========================
    estimated_cost = round(sum(consumption) * 0.11, 2)

    # =========================
    # 💡 SAVINGS LOGIC
    # =========================
    if alert == "HIGH":
        savings_tip = "Immediate load reduction can save up to 20%"
    elif alert == "MEDIUM":
        savings_tip = "Load shifting can reduce cost by ~10%"
    else:
        savings_tip = "System already optimized"

    # =========================
    # 🚀 FINAL RESPONSE (UPDATED)
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
