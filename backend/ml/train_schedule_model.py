import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import xgboost as xgb
import joblib
import os

print("⏳ Loading dataset...")
df = pd.read_csv("schedule_training_data.csv")

# =========================================================
# ADD RANDOM NOISE TO REDUCE OVERFITTING
# =========================================================

np.random.seed(42)

df["temperature"] += np.random.normal(0, 2, len(df))
df["humidity"] += np.random.normal(0, 5, len(df))
df["rainfall"] += np.random.normal(0, 3, len(df))
df["wind_speed"] += np.random.normal(0, 1, len(df))
df["soil_moisture"] += np.random.normal(0, 4, len(df))

# Clip values to realistic ranges
df["humidity"] = df["humidity"].clip(0, 100)
df["soil_moisture"] = df["soil_moisture"].clip(0, 100)
df["rainfall"] = df["rainfall"].clip(0)

# =========================================================
# ENCODE CATEGORICAL COLUMNS
# =========================================================

le_crop = LabelEncoder()
le_soil = LabelEncoder()
le_time = LabelEncoder()
le_next = LabelEncoder()

df["crop_enc"] = le_crop.fit_transform(df["crop"])
df["soil_condition_enc"] = le_soil.fit_transform(df["soil_condition"])

df["recommended_time_enc"] = le_time.fit_transform(
    df["recommended_time"]
)

df["next_irrigation_day_enc"] = le_next.fit_transform(
    df["next_irrigation_day"]
)

# =========================================================
# FEATURES
# =========================================================

FEATURES = [
    "temperature",
    "humidity",
    "rainfall",
    "wind_speed",
    "sunlight",
    "soil_moisture",
    "crop_enc",
    "soil_condition_enc"
]

X = df[FEATURES]

# =========================================================
# TARGETS
# =========================================================

targets = {
    "irrigate_today": df["irrigate_today"],
    "recommended_time": df["recommended_time_enc"],
    "next_irrigation_day": df["next_irrigation_day_enc"],
    "water_amount_mm": df["water_amount_mm"],
}

# =========================================================
# DISTRICT-BASED SPLIT
# =========================================================

TEST_DISTRICTS = [
    "Nagpur",
    "Kolhapur",
    "Latur",
    "Sindhudurg"
]

TRAIN_DISTRICTS = [
    d for d in df["district"].unique()
    if d not in TEST_DISTRICTS
]

train_df = df[df["district"].isin(TRAIN_DISTRICTS)]
test_df = df[df["district"].isin(TEST_DISTRICTS)]

X_train = train_df[FEATURES]
X_test = test_df[FEATURES]

# =========================================================
# TRAIN MODELS
# =========================================================

os.makedirs("ml", exist_ok=True)

for target_name, y in targets.items():

    print(f"\n⏳ Training model: {target_name}")

    y_train = y.loc[train_df.index]
    y_test = y.loc[test_df.index]

    print(
        f"Train size : {len(X_train):,} rows "
        f"({len(TRAIN_DISTRICTS)} districts)"
    )

    print(
        f"Test size  : {len(X_test):,} rows "
        f"({len(TEST_DISTRICTS)} districts)"
    )

    # =====================================================
    # REGRESSION MODEL
    # =====================================================

    if target_name == "water_amount_mm":

        model = xgb.XGBRegressor(
            n_estimators=40,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.7,
            colsample_bytree=0.7,
            reg_alpha=2,
            reg_lambda=3,
            random_state=42,
            verbosity=0
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        rmse = np.sqrt(np.mean((preds - y_test) ** 2))

        print(f"✅ RMSE: {rmse:.2f} mm")

        # Cross Validation
        scores = cross_val_score(
            model,
            X,
            y,
            cv=5,
            scoring='neg_root_mean_squared_error'
        )

        rmse_scores = -scores

        print(
            f"✅ Cross-validation RMSE: "
            f"{rmse_scores.mean():.2f} ± "
            f"{rmse_scores.std():.2f}"
        )

    # =====================================================
    # CLASSIFICATION MODELS
    # =====================================================

    else:

        model = xgb.XGBClassifier(
            n_estimators=40,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.7,
            colsample_bytree=0.7,
            min_child_weight=5,
            reg_alpha=2,
            reg_lambda=3,
            gamma=1,
            random_state=42,
            verbosity=0,
            eval_metric="mlogloss"
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)

        print(f"✅ Accuracy: {acc * 100:.2f}%")

        # Cross Validation
        scores = cross_val_score(
            model,
            X,
            y,
            cv=5,
            scoring='accuracy'
        )

        print(
            f"✅ Cross-validation accuracy: "
            f"{scores.mean() * 100:.2f}% ± "
            f"{scores.std() * 100:.2f}%"
        )

    # =====================================================
    # SAVE MODEL
    # =====================================================

    joblib.dump(
        model,
        f"ml/schedule_{target_name}_model.pkl"
    )

    print(
        f"💾 Saved: "
        f"ml/schedule_{target_name}_model.pkl"
    )

# =========================================================
# SAVE ENCODERS
# =========================================================

encoders = {
    "crop": le_crop,
    "soil_condition": le_soil,
    "time": le_time,
    "next_day": le_next,
}

joblib.dump(
    encoders,
    "ml/schedule_label_encoders.pkl"
)

print("\n💾 Saved: ml/schedule_label_encoders.pkl")

print("\n🎉 All models trained successfully!")