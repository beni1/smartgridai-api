import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# =========================
# CONFIG
# =========================
API_URL = "https://smartgridai-api.onrender.com/forecast"
HISTORY_URL = "https://smartgridai-api.onrender.com/history"
API_KEY = "free-user-key"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SmartGridAI-Nigeria",
    layout="wide"
)

st.title("⚡ SmartGridAI-Nigeria")
st.caption(
    "AI-Powered Smart Grid Monitoring & Energy Forecasting"
)

# =========================
# SIDEBAR CONTROLS
# =========================
st.sidebar.header("⚙ Dashboard Controls")

days = st.sidebar.slider(
    "Select Forecast Days",
    min_value=1,
    max_value=7,
    value=5
)

auto_refresh = st.sidebar.checkbox(
    "Enable Live Dashboard",
    value=False
)

refresh_rate = st.sidebar.slider(
    "Refresh Interval (seconds)",
    min_value=5,
    max_value=60,
    value=10
)

# =========================
# MAIN FORECAST SECTION
# =========================
st.subheader("🔮 Generate AI Forecast")

if st.button("Generate Forecast"):

    with st.spinner(
        "Generating AI energy insights..."
    ):

        try:

            response = requests.get(
                API_URL,
                params={"days": days},
                headers={"x-api-key": API_KEY},
                timeout=120
            )

            # =========================
            # ERROR HANDLING
            # =========================
            if response.status_code != 200:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.stop()

            result = response.json()

            # =========================
            # SIDEBAR API USAGE
            # =========================
            st.sidebar.subheader("📊 API Usage")

            st.sidebar.write(
                f"Plan: {result.get('plan', 'N/A')}"
            )

            st.sidebar.write(
                f"Usage: {result.get('used', 0)} / "
                f"{result.get('limit', 0)}"
            )

            # =========================
            # DATA EXTRACTION
            # =========================
            forecast_values = result.get(
                "forecast",
                []
            )

            insights = result.get(
                "insights",
                {}
            )

            time_data = [
                f"Day {i+1}"
                for i in range(len(forecast_values))
            ]

            # =========================
            # DATAFRAME
            # =========================
            df = pd.DataFrame({
                "Time": time_data,
                "Consumption": forecast_values
            })

            # =========================
            # FORECAST CHART
            # =========================
            st.subheader(
                "📈 Energy Consumption Forecast"
            )

            st.line_chart(
                df.set_index("Time")
            )

            # =========================
            # FORECAST TABLE
            # =========================
            st.subheader("📋 Forecast Data")

            st.dataframe(
                df,
                use_container_width=True
            )

            # =========================
            # RISK DISPLAY
            # =========================
            risk = result.get("risk", "LOW")

            st.subheader("🚨 Forecast Risk")

            if risk == "HIGH":

                st.error(
                    f"🚨 RISK LEVEL: {risk}"
                )

            elif risk == "MEDIUM":

                st.warning(
                    f"⚠️ RISK LEVEL: {risk}"
                )

            else:

                st.success(
                    f"✅ RISK LEVEL: {risk}"
                )

            # =========================
            # AI ANOMALY ALERTS
            # =========================
            st.subheader(
                "🔍 AI Anomaly Detection"
            )

            if result.get("anomaly_detected"):

                st.error(
                    f"⚠️ "
                    f"{result.get('anomaly_reason')}"
                )

            else:

                st.success(
                    "✅ No anomaly detected"
                )

            # =========================
            # OPTIONAL AI INSIGHTS
            # =========================
            if insights:

                st.subheader(
                    "⚡ AI Energy Intelligence"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Peak Risk",
                    insights.get(
                        "peak_risk",
                        "N/A"
                    )
                )

                col2.metric(
                    "Alert Status",
                    insights.get(
                        "alert",
                        "N/A"
                    )
                )

                col3.metric(
                    "Cost Impact",
                    insights.get(
                        "cost_impact",
                        "N/A"
                    )
                )

                # =========================
                # COST SECTION
                # =========================
                st.markdown(
                    "### 💰 Estimated Cost Impact"
                )

                st.success(
                    f"${insights.get('estimated_cost', 0):.2f}"
                )

                # =========================
                # RECOMMENDATION
                # =========================
                st.markdown(
                    "### 🧠 Recommended Action"
                )

                st.info(
                    insights.get(
                        "recommendation",
                        "No recommendation"
                    )
                )

                # =========================
                # SAVINGS TIP
                # =========================
                st.markdown(
                    "### 💡 Optimization Tip"
                )

                st.warning(
                    insights.get(
                        "savings_tip",
                        "No tip available"
                    )
                )

                # =========================
                # TREND ANALYSIS
                # =========================
                st.markdown(
                    "### 📊 Demand Trend"
                )

                trend = insights.get(
                    "trend",
                    0
                )

                next_trend = insights.get(
                    "next_trend",
                    "UNKNOWN"
                )

                st.write(
                    f"Trend Change: {trend}%"
                )

                st.write(
                    f"Next Prediction Trend: "
                    f"{next_trend}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Connection error: "
                "Unable to connect to API."
            )

        except requests.exceptions.Timeout:

            st.error(
                "Request timeout: "
                "API took too long to respond."
            )

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )

# =========================================================
# PHASE 2 — ANALYTICS DASHBOARD
# =========================================================
st.markdown("---")

st.header(
    "📊 SmartGridAI Analytics Dashboard"
)

try:

    # =========================
    # FETCH HISTORY
    # =========================
    history_response = requests.get(
        HISTORY_URL,
        headers={"x-api-key": API_KEY},
        timeout=120
    )

    if history_response.status_code == 200:

        history = history_response.json()

        # =========================
        # CONVERT TO DATAFRAME
        # =========================
        history_df = pd.DataFrame(history)

        # =========================
        # DISPLAY HISTORY TABLE
        # =========================
        st.subheader(
            "🗂 Historical Forecast Records"
        )

        st.dataframe(
            history_df,
            use_container_width=True
        )

        # =========================
        # FORECAST HISTORY CHART
        # =========================
        if (
            "timestamp" in history_df.columns
            and "forecast" in history_df.columns
        ):

            st.subheader(
                "📈 Historical Forecast Trend"
            )

            fig = px.line(
                history_df,
                x="timestamp",
                y="forecast",
                title="Forecast History"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =========================
        # RISK DASHBOARD
        # =========================
        if "risk" in history_df.columns:

            st.subheader("🚨 Risk Analytics")

            risk_counts = (
                history_df["risk"]
                .value_counts()
            )

            st.bar_chart(risk_counts)

            high_count = risk_counts.get(
                "HIGH",
                0
            )

            medium_count = risk_counts.get(
                "MEDIUM",
                0
            )

            low_count = risk_counts.get(
                "LOW",
                0
            )

            r1, r2, r3 = st.columns(3)

            r1.metric(
                "HIGH",
                high_count
            )

            r2.metric(
                "MEDIUM",
                medium_count
            )

            r3.metric(
                "LOW",
                low_count
            )

        # =========================
        # API USAGE ANALYTICS
        # =========================
        st.subheader(
            "📡 API Usage Analytics"
        )

        total_requests = len(history_df)

        active_users = (
            history_df["api_key"].nunique()
            if "api_key" in history_df.columns
            else 1
        )

        usage_limit = 100

        a1, a2, a3 = st.columns(3)

        a1.metric(
            "Total Requests",
            total_requests
        )

        a2.metric(
            "Active Users",
            active_users
        )

        a3.metric(
            "Usage Limit",
            usage_limit
        )

    else:

        st.warning(
            "History endpoint unavailable."
        )

except Exception as e:

    st.error(
        f"Analytics error: {e}"
    )

# =========================================================
# LIVE AUTO REFRESH
# TEMPORARILY DISABLED
# =========================================================
if auto_refresh:

    st.info(
        "🔄 Live dashboard temporarily "
        "disabled for stability."
    )

    # time.sleep(refresh_rate)

    # st.rerun()
