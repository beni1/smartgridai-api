from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base

# =========================
# FORECAST TABLE
# =========================

class Forecast(Base):

    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)

    forecast = Column(Float)

    risk = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)


# =========================
# API USAGE TABLE
# =========================

class APIUsage(Base):

    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)

    api_key = Column(String)

    requests = Column(Integer)

    date = Column(DateTime, default=datetime.utcnow)


# =========================
# MODEL TRAINING TABLE
# =========================

class ModelTraining(Base):

    __tablename__ = "model_training"

    id = Column(Integer, primary_key=True, index=True)

    epochs = Column(Integer)

    loss = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)
