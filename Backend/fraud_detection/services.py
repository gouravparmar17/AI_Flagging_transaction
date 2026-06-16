import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from alerts.models import Alert
from .models import FraudPrediction

MODEL_DIR = Path(__file__).resolve().parent.parent / "ml_models"
MODEL_PATH = MODEL_DIR / "fraud_model.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
METRICS_PATH = MODEL_DIR / "model_metrics.json"

RISKY_MERCHANTS = {"unknown", "crypto_exchange", "offshore_transfer"}
RISKY_LOCATIONS = {"unknown", "high_risk_zone"}
HIGH_AMOUNT_BASELINE = 50000.0


class FraudScoringService:
    model = None
    scaler = None

    @classmethod
    def _load_model(cls):
        if cls.model is None and MODEL_PATH.exists():
            cls.model = joblib.load(MODEL_PATH)
        if cls.scaler is None and SCALER_PATH.exists():
            cls.scaler = joblib.load(SCALER_PATH)

    @classmethod
    def build_features(cls, payload):
        amount = float(payload.get("amount", 0))
        merchant = str(payload.get("merchant", "")).strip().lower()
        location = str(payload.get("location", "")).strip().lower()
        tx_type = str(payload.get("transaction_type", "")).strip().lower()
        device_id = str(payload.get("device_id", ""))
        ip_address = str(payload.get("ip_address", ""))

        amount_deviation = amount / 2500.0
        return pd.DataFrame(
            [
                {
                    "amount": amount,
                    "amount_log": np.log1p(max(amount, 0)),
                    "amount_deviation": amount_deviation,
                    "hour": 12,
                    "is_weekend": 0,
                    "merchant_risk": 1 if merchant in RISKY_MERCHANTS else 0,
                    "location_risk": 1 if location in RISKY_LOCATIONS else 0,
                    "device_fingerprint_len": len(device_id),
                    "ip_feature": len(ip_address),
                    "merchant": merchant or "unknown",
                    "location": location or "unknown",
                    "transaction_type": tx_type or "online",
                }
            ]
        )

    @classmethod
    def score(cls, payload):
        cls._load_model()
        features = cls.build_features(payload)

        if cls.model is not None:
            probability = float(cls.model.predict_proba(features)[0][1])
        else:
            amount_factor = min(float(payload.get("amount", 0)) / HIGH_AMOUNT_BASELINE, 1.0)
            online_factor = 0.2 if str(payload.get("transaction_type", "")).lower() == "online" else 0.0
            probability = max(0.01, min(0.99, amount_factor + online_factor))

        risk_score = int(round(probability * 100))
        confidence = round(50 + abs(probability - 0.5) * 100, 2)
        prediction = "Fraud" if probability >= 0.6 else "Safe"

        if risk_score >= 90:
            severity = "Critical"
        elif risk_score >= 75:
            severity = "High"
        elif risk_score >= 50:
            severity = "Medium"
        else:
            severity = "Low"

        return {
            "prediction": prediction,
            "fraud_probability": round(probability, 4),
            "risk_score": risk_score,
            "confidence": confidence,
            "severity": severity,
            "model_version": "v1",
        }


def create_prediction_for_transaction(user, transaction):
    score = FraudScoringService.score(
        {
            "amount": transaction.amount,
            "merchant": transaction.merchant,
            "location": transaction.location,
            "transaction_type": transaction.transaction_type,
            "device_id": transaction.device_id,
            "ip_address": transaction.ip_address,
        }
    )

    prediction = FraudPrediction.objects.create(
        user=user,
        transaction=transaction,
        fraud_probability=score["fraud_probability"],
        risk_score=score["risk_score"],
        confidence=score["confidence"],
        prediction=score["prediction"],
        model_version=score["model_version"],
    )

    if score["prediction"] == "Fraud":
        Alert.objects.create(user=user, transaction=transaction, severity=score["severity"], status="Open")

    return prediction, score


def load_metrics():
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text())
    return {}
