from fastapi import FastAPI, Header, HTTPException
import pandas as pd

app = FastAPI()

# =========================
# ✅ ROOT ENDPOINT
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
    # 🔥 SMARTER ALERT SYSTEM
    # =========================
    peak = max(consumption)
    avg = sum(consumption) / len(consumption)

    # 📈 TREND DETECTION
    trend = consumption[-1] - consumption[0] if len(consumption) > 1 else 0

    # ⚡ DEFAULTS
    alert = "LOW"
    peak_risk = "STABLE"
    cost_impact = "NORMAL COST"
    recommendation = "Normal operation"
    savings_tip = "System already optimized"

    # =========================
    # 🚨 ANOMALY OVERRIDE
    # =========================
    if anomaly_detected:
        alert = "CRITICAL"
        peak_risk = "UNSTABLE"
        cost_impact = "EXTREME COST RISK"
        recommendation = "Investigate abnormal demand pattern immediately"
        savings_tip = "Immediate intervention required to prevent failure"

    # =========================
    # 🚨 EMERGENCY CONDITION
    # =========================
    elif peak > 150 or trend > 40:
        alert = "EMERGENCY"
        peak_risk = "SYSTEM FAILURE RISK"
        cost_impact = "CRITICAL COST ESCALATION"
        recommendation = "IMMEDIATE GRID STABILIZATION REQUIRED"
        savings_tip = "Emergency load shedding required to prevent blackout"

    # =========================
    # 🔴 CRITICAL CONDITION
    # =========================
    elif peak > 130 or trend > 25:
        alert = "HIGH"
        peak_risk = "CRITICAL"
        cost_impact = "VERY HIGH COST"
        recommendation = "Reduce load immediately or activate backup supply"
        savings_tip = "Immediate load reduction can save up to 20%"

    # =========================
    # 🟠 HIGH CONDITION
    # =========================
    elif peak > 115 or trend > 15:
        alert = "MEDIUM"
        peak_risk = "ELEVATED"
        cost_impact = "HIGH COST"
        recommendation = "Shift non-essential load to off-peak hours"
        savings_tip = "Load shifting can reduce cost by ~10–15%"

    # =========================
    # 🔮 SIMPLE PREDICTION SIGNAL
    # =========================
    if len(consumption) >= 2:
        next_trend = (
            "INCREASING"
            if consumption[-1] > consumption[-2]
            else "DECREASING"
        )
    else:
        next_trend = "UNKNOWN"

    # =========================
    # 💰 COST MODEL
    # =========================
    estimated_cost = round(sum(consumption) * 0.11, 2)

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
            "anomaly_reason": anomaly_reason,
            "trend": trend,
            "next_trend": next_trend
        },
        "plan": "free",
        "used": days,
        "limit": 7
    }
