import streamlit as st
import requests
import pandas as pd
import os

# ✅ LSTM IMPORTS
from lstm_model import train_lstm, predict_next, load_saved_model

# =========================
# CONFIG
# =========================
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/demand"
)
API_KEY = "free-user-key"

st.set_page_config(page_title="SmartGridAI", layout="wide")
st.title("⚡ SmartGridAI - Energy Demand Dashboard")

# =========================
# LOAD MODEL
# =========================
if "model" not in st.session_state:
    model, scaler = load_saved_model()
    if model is not None:
        st.session_state["model"] = model
        st.session_state["scaler"] = scaler
        st.success("✅ Loaded saved AI model!")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Controls")
days = st.sidebar.slider("Select number of days", 1, 7, 1)

# =========================
# FETCH DATA FROM API
# =========================
if st.button("Generate Demand Data"):
    with st.spinner("Fetching data from API..."):
        try:
            response = requests.get(
                API_URL,
                params={"days": days},
                headers={"x-api-key": API_KEY}
            )

            data = response.json()

            if "data" not in data:
                st.error(f"API Error: {data}")
            else:
                time = data["data"]["time"]
                consumption = data["data"]["consumption"]

                df = pd.DataFrame({
                    "Time": time,
                    "Consumption": consumption
                })

                # ✅ Add temperature feature
                df["Temperature"] = 25 + (df.index % 10)

                st.session_state["df"] = df

                # =========================
                # DISPLAY CHART
                # =========================
                st.subheader("📈 Demand Curve")
                st.line_chart(df.set_index("Time"))

                col1, col2, col3 = st.columns(3)
                col1.metric("Plan", data["plan"])
                col2.metric("Used", data["used"])
                col3.metric("Limit", data["limit"])

                st.subheader("📋 Raw Data")
                st.dataframe(df)

                # =========================
                # 💰 MONETIZATION DISPLAY (NEW)
                # =========================
                if "insights" in data:
                    st.subheader("💡 Energy Intelligence Insights")

                    insights = data["insights"]

                    st.write("🚨 Alert:", insights["alert"])
                    st.write("⚡ Peak Risk:", insights["peak_risk"])
                    st.write("💰 Cost Impact:", insights["cost_impact"])
                    st.write("📌 Recommendation:", insights["recommendation"])
                    st.write("💸 Estimated Cost:", insights["estimated_cost"])
                    st.write("📉 Savings Tip:", insights["savings_tip"])

        except Exception as e:
            st.error(f"Connection error: {e}")

# =========================
# 🤖 AI PREDICTION (LSTM)
# =========================
st.subheader("🤖 AI Prediction (LSTM)")

if st.button("Train AI Model"):
    if "df" in st.session_state:

        if "model" in st.session_state:
            st.info("Model already loaded. Skipping training.")
        else:
            df = st.session_state["df"]

            st.info(f"Training on {len(df)} data points...")

            progress_bar = st.progress(0)
            status_text = st.empty()

            from tensorflow.keras.callbacks import Callback

            class StreamlitCallback(Callback):
                def on_epoch_end(self, epoch, logs=None):
                    total_epochs = self.params["epochs"]
                    progress = (epoch + 1) / total_epochs
                    progress_bar.progress(progress)
                    status_text.text(f"Epoch {epoch+1}/{total_epochs} completed")

            with st.spinner("Training AI model..."):
                model, scaler, epochs = train_lstm(
                    df,
                    callback=StreamlitCallback()
                )

            st.session_state["model"] = model
            st.session_state["scaler"] = scaler

            progress_bar.progress(1.0)
            status_text.text("Training complete!")

            st.success("Model trained and saved!")

    else:
        st.warning("Generate data first!")

# =========================
# 🔮 PREDICTION
# =========================
if st.button("Predict Next Demand"):
    if "model" in st.session_state and "df" in st.session_state:

        prediction = predict_next(
            st.session_state["model"],
            st.session_state["df"],
            st.session_state["scaler"]
        )

        st.metric("Next Demand Prediction", round(prediction, 2))

    else:
        st.warning("Train model first!")
