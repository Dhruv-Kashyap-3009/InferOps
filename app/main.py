import joblib
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

model = joblib.load("model/breast_cancer.joblib")

# scikit-learn stores the labels as 0 = malignant, 1 = benign
NAMES = ["malignant", "benign"]

app = FastAPI(title="Breast cancer classifier")


class TumorInput(BaseModel):
    # The 30 measurements of the breast cancer dataset, in dataset column order.
    # The field order matters: the values are sent to the model in this order.

    # Mean of each measurement over the cell nucleus
    mean_radius: float = Field(ge=0)
    mean_texture: float = Field(ge=0)
    mean_perimeter: float = Field(ge=0)
    mean_area: float = Field(ge=0)
    mean_smoothness: float = Field(ge=0)
    mean_compactness: float = Field(ge=0)
    mean_concavity: float = Field(ge=0)
    mean_concave_points: float = Field(ge=0)
    mean_symmetry: float = Field(ge=0)
    mean_fractal_dimension: float = Field(ge=0)

    # Standard error of each measurement
    radius_error: float = Field(ge=0)
    texture_error: float = Field(ge=0)
    perimeter_error: float = Field(ge=0)
    area_error: float = Field(ge=0)
    smoothness_error: float = Field(ge=0)
    compactness_error: float = Field(ge=0)
    concavity_error: float = Field(ge=0)
    concave_points_error: float = Field(ge=0)
    symmetry_error: float = Field(ge=0)
    fractal_dimension_error: float = Field(ge=0)

    # Worst (largest) value of each measurement
    worst_radius: float = Field(ge=0)
    worst_texture: float = Field(ge=0)
    worst_perimeter: float = Field(ge=0)
    worst_area: float = Field(ge=0)
    worst_smoothness: float = Field(ge=0)
    worst_compactness: float = Field(ge=0)
    worst_concavity: float = Field(ge=0)
    worst_concave_points: float = Field(ge=0)
    worst_symmetry: float = Field(ge=0)
    worst_fractal_dimension: float = Field(ge=0)


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: TumorInput):
    # model_dump() keeps the field order, which is the dataset column order
    row = list(data.model_dump().values())

    probabilities = model.predict_proba([row])[0]
    index = int(probabilities.argmax())

    return {
        "prediction": NAMES[int(model.classes_[index])],
        "confidence": round(float(probabilities[index]), 3),
    }
