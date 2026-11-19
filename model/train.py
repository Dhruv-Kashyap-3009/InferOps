import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 569 tumor samples, each described by 30 measurements taken from a digitised
# image of a cell nucleus. Labels: 0 = malignant, 1 = benign.
data = load_breast_cancer()

# Keep 20% of the samples out of training so the accuracy we print is honest
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42, stratify=data.target
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy on {len(X_test)} held-out samples: {accuracy:.3f}")

# Save the model with joblib
joblib.dump(model, "model/breast_cancer.joblib")
print("Model trained and saved to model/breast_cancer.joblib")
