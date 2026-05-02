import streamlit as st
import requests
import pandas as pd

# =========================
# CONFIG
# =========================
API_URL = "https://smartgridai-api.onrender.com/demand"
API_KEY = "free-user-key"

st.set_page_config(
    page_title="SmartGridAI-Nigeria",
    layout="wide"
)

st.title("⚡ SmartGridAI-Nigeria")
st.caption("AI-Powered Smart Grid Monitoring & Energy Forecasting")

# =========================
# USER INPUT
# =========================
days = st.slider(
    "Select Number of Days",
    min_value=1,
    max_value=7,
    value=5
)

# =========================
# FETCH DATA BUTTON
# =========================
if st.button("Generate Forecast"):

    with st.spinner("Generating AI energy insights..."):

        try:
            response = requests.get(
                API_URL,
                params={"days": days},
                headers={"x-api-key": API_KEY},
                timeout=30
            )

            # =========================
            # API ERROR HANDLING
            # =========================
            if response.status_code != 200:
                st.error(f"API Error: {response.status_code}")
                st.stop()

            result = response.json()

            # =========================
            # USAGE INFO
            # =========================
            st.sidebar.subheader("📊 API Usage")

            st.sidebar.write(f"Plan: {result.get('plan', 'N/A')}")
            st.sidebar.write(
                f"Usage: {result.get('used', 0)} / {result.get('limit', 0)}"
            )

            # =========================
            # DATA EXTRACTION
            # =========================
            data = result.get("data", {})
            insights = result.get("insights", {})

            time_data = data.get("time", [])
            consumption_data = data.get("consumption", [])

            # =========================
            # DATAFRAME
            # =========================
            df = pd.DataFrame({
                "Time": time_data,
                "Consumption": consumption_data
            })

            # =========================
            # CHART
            # =========================
            st.subheader("📈 Energy Consumption Forecast")

            st.line_chart(
                df.set_index("Time")
            )

            # =========================
            # TABLE
            # =========================
            st.subheader("📋 Forecast Data")

            st.dataframe(
                df,
                use_container_width=True
            )

            # =========================
            # 🔥 INSIGHTS DISPLAY (UPGRADED)
            # =========================
            if insights:

                st.subheader("⚡ AI Energy Intelligence")

                # 🎯 TOP METRICS
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Peak Risk",
                    insights.get("peak_risk", "N/A")
                )

                col2.metric(
                    "Alert Status",
                    insights.get("alert", "N/A")
                )

                col3.metric(
                    "Cost Impact",
                    insights.get("cost_impact", "N/A")
                )

                # 💰 COST SECTION
                st.markdown("### 💰 Estimated Cost Impact")

                st.success(
                    f"${insights.get('estimated_cost', 0):.2f}"
                )

                # 🚨 ALERT COLOR LOGIC
                alert = insights.get("alert", "NORMAL")

                if alert == "HIGH":
                    st.error(f"🚨 ALERT: {alert}")

                elif alert == "MEDIUM":
                    st.warning(f"⚠️ ALERT: {alert}")

                else:
                    st.success(f"✅ ALERT: {alert}")

                # 🧠 RECOMMENDATION
                st.markdown("### 🧠 Recommended Action")

                st.info(
                    insights.get(
                        "recommendation",
                        "No recommendation"
                    )
                )

                # 💡 SAVINGS TIP
                st.markdown("### 💡 Optimization Tip")

                st.warning(
                    insights.get(
                        "savings_tip",
                        "No tip available"
                    )
                )

                # 📈 TREND ANALYSIS
                st.markdown("### 📊 Demand Trend")

                trend = insights.get("trend", 0)
                next_trend = insights.get("next_trend", "UNKNOWN")

                st.write(f"Trend Change: {trend}%")
                st.write(f"Next Prediction Trend: {next_trend}")

                # 🚨 ANOMALY DETECTION
                st.markdown("### 🔍 Anomaly Detection")

                anomaly = insights.get("anomaly_detected", False)
                anomaly_reason = insights.get(
                    "anomaly_reason",
                    "No anomaly"
                )

                if anomaly:
                    st.error(f"⚠️ {anomaly_reason}")
                else:
                    st.success(f"✅ {anomaly_reason}")

        except requests.exceptions.ConnectionError:
            st.error("Connection error: Unable to connect to API.")

        except requests.exceptions.Timeout:
            st.error("Request timeout: API took too long to respond.")

        except Exception as e:
            st.error(f"Unexpected error: {e}")
