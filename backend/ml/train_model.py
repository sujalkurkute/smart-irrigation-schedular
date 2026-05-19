import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from sklearn.model_selection import cross_val_score
# Load dataset
df = pd.read_csv("irrigation_prediction.csv")

# Show sample data
print(df.head())

# Show columns
print(df.columns)

# Remove missing values
df = df.dropna()

# Categorical columns
categorical_columns = [
    "Soil_Type",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Season",
    "Irrigation_Type",
    "Water_Source",
    "Mulching_Used",
    "Region",
    "Irrigation_Need"
]

# Store encoders
label_encoders = {}

# Encode categorical columns
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# FEATURES
X = df[[
    "Soil_Type",
    "Soil_pH",
    "Soil_Moisture",
    "Organic_Carbon",
    "Electrical_Conductivity",
    "Temperature_C",
    "Humidity",
    "Rainfall_mm",
    "Sunlight_Hours",
    "Wind_Speed_kmh",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Season",
    "Water_Source",
    "Field_Area_hectare",
    "Mulching_Used",
    "Region"
]]
# TARGET
y = df["Irrigation_Need"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestClassifier(
    n_estimators=40,
    max_depth=5,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features="sqrt",
    random_state=42
)

scores = cross_val_score(model, X, y, cv=5)

print(f"\nCross Validation Accuracy: {scores.mean():.2f}")
# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy:.2f}")

# Save trained model
joblib.dump(model, "irrigation_model.pkl")

# Save encoders
joblib.dump(label_encoders, "label_encoders.pkl")

print("\nModel saved successfully!")