import numpy as np
import os
import joblib
import pandas as pd

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# =========================
# GLOBAL CONSTANT
# =========================
WINDOW_SIZE = 10

# =========================
# LOAD CSV DATASET
# =========================
def load_dataset():
    df = pd.read_csv("data/power_data.csv")

    # Create synthetic Time column
    df["Time"] = np.arange(len(df))

    # Create synthetic Temperature column
    df["Temperature"] = np.random.randint(
        25,
        40,
        size=len(df)
    )

    # Reorder columns
    df = df[
        ["Time", "Temperature", "consumption"]
    ]

    # Rename for consistency
    df.columns = [
        "Time",
        "Temperature",
        "Consumption"
    ]

    return df

# =========================
# PREPARE DATA
# =========================
def prepare_data(
    df,
    window_size=WINDOW_SIZE
):

    features = df[
        ["Time", "Temperature", "Consumption"]
    ].values

    scaler = MinMaxScaler()

    scaled_data = scaler.fit_transform(
        features
    )

    X, y = [], []

    for i in range(
        len(scaled_data) - window_size
    ):

        X.append(
            scaled_data[i:i + window_size]
        )

        # Predict Consumption
        y.append(
            scaled_data[i + window_size][2]
        )

    return (
        np.array(X),
        np.array(y),
        scaler
    )

# =========================
# BUILD MODEL
# =========================
def build_lstm_model(input_shape):

    model = Sequential()

    model.add(
        LSTM(
            64,
            return_sequences=True,
            input_shape=input_shape
        )
    )

    model.add(
        LSTM(32)
    )

    model.add(
        Dense(1)
    )

    model.compile(
        optimizer='adam',
        loss='mse'
    )

    return model

# =========================
# SAVE MODEL
# =========================
def save_model(model, scaler):

    os.makedirs("model", exist_ok=True)

    model.save(
        "model/lstm_model.keras"
    )

    joblib.dump(
        scaler,
        "model/scaler.pkl"
    )

# =========================
# LOAD MODEL
# =========================
def load_saved_model():

    model_path = "model/lstm_model.keras"
    scaler_path = "model/scaler.pkl"

    if (
        os.path.exists(model_path)
        and
        os.path.exists(scaler_path)
    ):

        model = load_model(model_path)

        scaler = joblib.load(
            scaler_path
        )

        return model, scaler

    return None, None

# =========================
# TRAIN MODEL
# =========================
def train_lstm(
    df,
    callback=None
):

    X, y, scaler = prepare_data(df)

    data_size = len(X)

    # Smart training adjustment
    if data_size < 50:
        epochs = 5
        batch_size = 8

    elif data_size < 200:
        epochs = 10
        batch_size = 16

    else:
        epochs = 15
        batch_size = 32

    model = build_lstm_model(
        (
            X.shape[1],
            X.shape[2]
        )
    )

    callbacks = []

    if callback:
        callbacks.append(callback)

    print(
        f"Training with {data_size} samples | "
        f"epochs={epochs}, batch={batch_size}"
    )

    model.fit(
        X,
        y,
        epochs=epochs,
        batch_size=batch_size,
        verbose=1,
        callbacks=callbacks
    )

    # Save model after training
    save_model(model, scaler)

    return model, scaler, epochs

# =========================
# MULTI-STEP FORECASTING
# =========================
def predict_next_days(
    model,
    df,
    scaler,
    days=5
):

    # -------------------------
    # Extract latest features
    # -------------------------
    features = df[
        ["Time", "Temperature", "Consumption"]
    ].values

    # -------------------------
    # Take last window
    # -------------------------
    last_window = features[-WINDOW_SIZE:]

    # Scale window
    scaled_window = scaler.transform(
        last_window
    )

    predictions = []

    # -------------------------
    # Recursive forecasting loop
    # -------------------------
    for i in range(days):

        # Reshape for LSTM
        input_window = scaled_window.reshape(
            (1, WINDOW_SIZE, 3)
        )

        # Predict next consumption
        pred_scaled = model.predict(
            input_window,
            verbose=0
        )

        predicted_consumption_scaled = pred_scaled[0][0]

        # -------------------------
        # Generate next synthetic features
        # -------------------------

        # Next time value
        next_time = last_window[-1][0] + 1

        # Slight temperature variation
        next_temp = (
            last_window[-1][1]
            + np.random.uniform(-1, 1)
        )

        # Create new scaled row
        new_row = np.array([
            next_time,
            next_temp,
            0
        ]).reshape(1, -1)

        # Scale new row
        scaled_new_row = scaler.transform(
            new_row
        )

        # Insert predicted consumption
        scaled_new_row[0][2] = (
            predicted_consumption_scaled
        )

        # -------------------------
        # Inverse transform prediction
        # -------------------------
        dummy = np.zeros((1, 3))

        dummy[0][0] = scaled_new_row[0][0]
        dummy[0][1] = scaled_new_row[0][1]
        dummy[0][2] = predicted_consumption_scaled

        prediction_actual = scaler.inverse_transform(
            dummy
        )[0][2]

        predictions.append(
            round(float(prediction_actual), 2)
        )

        # -------------------------
        # Update recursive window
        # -------------------------
        scaled_window = np.vstack([
            scaled_window[1:],
            scaled_new_row
        ])

        # Update actual last_window too
        last_window = np.vstack([
            last_window[1:],
            [next_time, next_temp, prediction_actual]
        ])

    return predictions

    features = df[
        ["Time", "Temperature", "Consumption"]
    ].values

    last_window = features[-WINDOW_SIZE:]

    scaled_window = scaler.transform(
        last_window
    )

    scaled_window = scaled_window.reshape(
        (1, WINDOW_SIZE, 3)
    )

    prediction = model.predict(
        scaled_window,
        verbose=0
    )

    # Dummy array for inverse scaling
    dummy = np.zeros((1, 3))

    dummy[0, 2] = prediction[0, 0]

    return float(
        scaler.inverse_transform(dummy)[0][2]
    )

# =========================
# RUN TRAINING DIRECTLY
# =========================
if __name__ == "__main__":

    print("Loading dataset...")

    df = load_dataset()

    print(df.head())

    print("Training LSTM model...")

    model, scaler, epochs = train_lstm(df)

    print("Training complete.")

    print("Model saved to:")
    print("model/lstm_model.keras")

    print("Scaler saved to:")
    print("model/scaler.pkl")
