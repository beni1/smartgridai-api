from fastapi import FastAPI, Header, HTTPException
import pandas as pd

app = FastAPI()

# =========================
# ✅ ROOT ENDPOINT (NEW)
# =========================
@app.get("/")
def root():
    return {
        "message": "SmartGridAI API is running",
        "endpoint": "/demand",
        "status": "OK"
    }

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
    # 🚨 ANOMALY DETECTION
    # =========================
    anomaly_detected = False
    anomaly_reason = "No anomaly"

    for i in range(1, len(consumption)):
        change = consumption[i] - consumption[i - 1]

        if change > 15:
            anomaly_detected = True
            anomaly_reason = "Sudden demand spike detected"
            break

    if not anomaly_detected:
        variance = max(consumption) - min(consumption)
        if variance > 40:
            anomaly_detected = True
            anomaly_reason = "High demand fluctuation detected"

    # =========================
    # 🔥 SMART ALERT LOGIC
    # =========================
    peak = max(consumption)
    avg = sum(consumption) / len(consumption)

    if anomaly_detected:
        alert = "CRITICAL"
        peak_risk = "UNSTABLE"
        cost_impact = "EXTREME COST RISK"
        recommendation = "Investigate abnormal demand pattern immediately"

    elif peak > 130:
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
    # 💰 COST MODEL
    # =========================
    estimated_cost = round(sum(consumption) * 0.11, 2)

    # =========================
    # 💡 SAVINGS LOGIC
    # =========================
    if alert == "CRITICAL":
        savings_tip = "Immediate intervention required to prevent failure"
    elif alert == "HIGH":
        savings_tip = "Immediate load reduction can save up to 20%"
    elif alert == "MEDIUM":
        savings_tip = "Load shifting can reduce cost by ~10%"
    else:
        savings_tip = "System already optimized"

    # =========================
    # 🚀 FINAL RESPONSE
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
            "savings_tip": savings_tip,
            "anomaly_detected": anomaly_detected,
            "anomaly_reason": anomaly_reason
        },
        "plan": "free",
        "used": days,
        "limit": 7
    }
