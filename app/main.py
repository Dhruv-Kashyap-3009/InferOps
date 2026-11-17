import joblib
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

model = joblib.load("model/iris.joblib")
NAMES = ["setosa", "versicolor", "virginica"]
app = FastAPI()


class IrisInput(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: IrisInput):
    row = [data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]
    return {"prediction": NAMES[int(model.predict([row])[0])]}
