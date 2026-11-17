import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train a RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the model with joblib
joblib.dump(model, "model/iris.joblib")
print("Model trained and saved to model/iris.joblib")