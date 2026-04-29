import numpy as np
import os
import joblib

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# ✅ GLOBAL CONSTANT
WINDOW_SIZE = 10


# =========================
# STEP 1 — PREPARE DATA (MULTI-FEATURE)
# =========================
def prepare_data(df, window_size=WINDOW_SIZE):
    features = df[["Time", "Temperature", "Consumption"]].values

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(features)

    X, y = [], []

    for i in range(len(scaled_data) - window_size):
        X.append(scaled_data[i:i + window_size])
        y.append(scaled_data[i + window_size][2])  # Predict Consumption

    return np.array(X), np.array(y), scaler


# =========================
# STEP 3 — MODEL ARCHITECTURE
# =========================
def build_lstm_model(input_shape):
    model = Sequential()

    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(32))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mse')

    return model


# =========================
# ✅ SAVE MODEL
# =========================
def save_model(model, scaler):
    model.save("lstm_model.h5")
    joblib.dump(scaler, "scaler.save")


# =========================
# ✅ LOAD MODEL
# =========================
def load_saved_model():
    if os.path.exists("lstm_model.h5") and os.path.exists("scaler.save"):
        model = load_model("lstm_model.h5")
        scaler = joblib.load("scaler.save")
        return model, scaler
    return None, None


# =========================
# STEP 2 — TRAIN MODEL (UPDATED WITH SAVE)
# =========================
def train_lstm(df, callback=None):
    X, y, scaler = prepare_data(df)

    data_size = len(X)

    # ✅ SMART TRAINING (auto-adjust)
    if data_size < 50:
        epochs = 5
        batch_size = 8
    elif data_size < 200:
        epochs = 10
        batch_size = 16
    else:
        epochs = 15
        batch_size = 32

    model = build_lstm_model((X.shape[1], X.shape[2]))

    # ✅ Add callback support (for Streamlit progress UI)
    callbacks = []
    if callback:
        callbacks.append(callback)

    print(f"Training with {data_size} samples | epochs={epochs}, batch={batch_size}")

    model.fit(
        X,
        y,
        epochs=epochs,
        batch_size=batch_size,
        verbose=0,  # silent (UI will handle progress)
        callbacks=callbacks
    )

    # ✅ Save after training
    save_model(model, scaler)

    return model, scaler, epochs

# =========================
# STEP 4 — PREDICT
# =========================
def predict_next(model, df, scaler):
    features = df[["Time", "Temperature", "Consumption"]].values

    last_window = features[-WINDOW_SIZE:]

    scaled_window = scaler.transform(last_window)
    scaled_window = scaled_window.reshape((1, WINDOW_SIZE, 3))

    prediction = model.predict(scaled_window, verbose=0)

    # Rebuild full feature for inverse scaling
    dummy = np.zeros((1, 3))
    dummy[0, 2] = prediction[0, 0]

    return float(scaler.inverse_transform(dummy)[0][2])
