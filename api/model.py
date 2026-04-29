import numpy as np

def generate_demand(days=1):
    hours = np.arange(1, 24 * days + 1)

    # Smooth daily cycle
    daily_cycle = 120 + 30 * np.sin(2 * np.pi * (hours - 6) / 24)

    # Evening peak
    evening_boost = 40 * np.exp(-0.5 * ((hours % 24 - 19) / 3) ** 2)

    # Noise
    noise = np.random.normal(0, 8, len(hours))

    consumption = daily_cycle + evening_boost + noise
    consumption = np.maximum(consumption, 0)

    return {
        "time": hours.tolist(),
        "consumption": consumption.astype(int).tolist()
    }
