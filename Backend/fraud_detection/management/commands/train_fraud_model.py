import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

MODEL_DIR = Path(__file__).resolve().parents[3] / "ml_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


class Command(BaseCommand):
    help = "Train fraud detection model and save artifacts"

    def handle(self, *args, **options):
        rng = np.random.default_rng(42)
        rows = 1200
        df = pd.DataFrame(
            {
                "amount": rng.uniform(1, 100000, rows),
                "merchant": rng.choice(["Amazon", "Walmart", "Unknown", "Crypto_Exchange"], rows),
                "location": rng.choice(["Indore", "Mumbai", "Unknown", "High_Risk_Zone"], rows),
                "transaction_type": rng.choice(["Online", "POS", "International"], rows),
                "device_id": rng.choice(["devA", "devB", "", "new_device"], rows),
                "ip_address": rng.choice(["10.0.0.1", "192.168.1.1", "", "172.16.5.2"], rows),
            }
        )

        df = df.drop_duplicates().fillna("")
        df["amount_log"] = np.log1p(df["amount"])
        df["is_weekend"] = rng.integers(0, 2, len(df))
        df["hour"] = rng.integers(0, 24, len(df))
        df["merchant_risk"] = df["merchant"].str.lower().isin(["unknown", "crypto_exchange"]).astype(int)
        df["location_risk"] = df["location"].str.lower().isin(["unknown", "high_risk_zone"]).astype(int)
        df["device_fingerprint_len"] = df["device_id"].str.len()
        df["ip_feature"] = df["ip_address"].str.len()
        df["amount_deviation"] = df["amount"] / max(df["amount"].mean(), 1)

        score = (
            (df["amount"] > 40000).astype(int)
            + df["merchant_risk"]
            + df["location_risk"]
            + (df["transaction_type"].str.lower() == "international").astype(int)
        )
        df["target"] = (score >= 2).astype(int)

        features = [
            "amount",
            "amount_log",
            "amount_deviation",
            "hour",
            "is_weekend",
            "merchant_risk",
            "location_risk",
            "device_fingerprint_len",
            "ip_feature",
            "merchant",
            "location",
            "transaction_type",
        ]

        X = df[features]
        y = df["target"]

        num_cols = [
            "amount",
            "amount_log",
            "amount_deviation",
            "hour",
            "is_weekend",
            "merchant_risk",
            "location_risk",
            "device_fingerprint_len",
            "ip_feature",
        ]
        cat_cols = ["merchant", "location", "transaction_type"]

        preprocess = ColumnTransformer(
            [
                ("num", StandardScaler(), num_cols),
                ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ]
        )

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        models = {
            "random_forest": RandomForestClassifier(n_estimators=120, random_state=42),
            "xgboost": XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.1, eval_metric="logloss"),
            "logistic_regression": LogisticRegression(max_iter=200),
        }

        metrics = {}
        best_name = ""
        best_f1 = -1
        best_pipeline = None

        for name, model in models.items():
            pipeline = Pipeline([("preprocess", preprocess), ("model", model)])
            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)
            metrics[name] = {
                "accuracy": round(float(accuracy_score(y_test, preds)), 4),
                "precision": round(float(precision_score(y_test, preds, zero_division=0)), 4),
                "recall": round(float(recall_score(y_test, preds, zero_division=0)), 4),
                "f1_score": round(float(f1_score(y_test, preds, zero_division=0)), 4),
                "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
            }
            if metrics[name]["f1_score"] > best_f1:
                best_f1 = metrics[name]["f1_score"]
                best_name = name
                best_pipeline = pipeline

        joblib.dump(best_pipeline, MODEL_DIR / "fraud_model.pkl")
        # scaler artifact for compatibility with requirement
        scaler = StandardScaler().fit(X_train[num_cols])
        joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

        metrics["selected_model"] = best_name
        (MODEL_DIR / "model_metrics.json").write_text(json.dumps(metrics, indent=2))

        self.stdout.write(self.style.SUCCESS(f"Model training complete. Selected model: {best_name}"))
