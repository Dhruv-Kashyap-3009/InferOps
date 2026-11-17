# InferOps — Iris classifier with a CI/CD pipeline

[![CI-CD](https://github.com/Dhruv-Kashyap-3009/InferOps/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Dhruv-Kashyap-3009/InferOps/actions/workflows/ci-cd.yml)

A small "MLOps in miniature" project: a scikit-learn Iris classifier served by FastAPI,
with a one-page web form, containerized with Docker, and shipped to Render by GitHub Actions.

## What it does

- Trains a `RandomForestClassifier` on the Iris dataset and saves it with joblib.
- Serves three routes with FastAPI: `GET /` (the form), `GET /health`, `POST /predict`.
- Returns only `{"prediction": "setosa"}` (or `versicolor` / `virginica`).
- Rejects missing, zero, negative, or non-numeric measurements with HTTP 422.

## How it fits together

```
              git push / pull request
                       │
                       ▼
              ┌──────────────────┐
              │  GitHub Actions  │
              │  job: test       │   flake8 → train model → pytest
              └────────┬─────────┘
                       │ only on push to main
                       ▼
              ┌──────────────────┐
              │  job: docker     │   build image → push to Docker Hub → Trivy scan
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │  job: deploy     │   curl the Render deploy hook
              └────────┬─────────┘
                       ▼
        ┌───────────────────────┐        ┌──────────────────────┐
        │        Render         │ pulls  │      Docker Hub      │
        │    web service        │◄───────│  iris-api:latest     │
        └───────────┬───────────┘        └──────────────────────┘
                    ▼
        FastAPI:  /   ·   /health   ·   /predict
                    │
                    ▼
        Browser form (plain HTML + fetch)
```

## Screenshots

The form at `GET /`:

![Home page](docs/screenshot-home.png)

After pressing Predict with a setosa sample:

![Prediction result](docs/screenshot-prediction.png)

## Run it locally

PowerShell:

```powershell
cd InferOps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python model\train.py
uvicorn app.main:app --reload
```

Command Prompt differs only in the activation line: `.\.venv\Scripts\activate.bat`.

Open <http://127.0.0.1:8000/> and press **Predict**. The API docs live at
<http://127.0.0.1:8000/docs>.

If PowerShell blocks the activation script, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Call the API

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
```

```json
{"prediction": "setosa"}
```

On PowerShell 5, `curl` is an alias for `Invoke-WebRequest` — use `curl.exe` instead.
The same request works against the deployed Render URL.

## Tests and linting

```powershell
python -m pytest -q
flake8 --max-line-length=88 app tests
```

Four tests cover the health route, a valid prediction, invalid input (422), and the home page.

## Docker

```powershell
docker build -t iris-api .
docker run --rm -p 8000:8000 iris-api
```

The trained model is **not** committed to git; both the image build and the CI test job
recreate it with `python model/train.py`. The container reads the `PORT` environment
variable (default `8000`), which is how Render chooses its port.

## Pipeline and secrets

| Job | Runs on | What it does |
|---|---|---|
| `test` | every push and pull request | flake8, train the model, pytest |
| `docker` | pushes to `main` only | build, push to Docker Hub, Trivy scan |
| `deploy` | after a successful `docker` job | calls the Render deploy hook |

Required repository secrets (Settings → Secrets and variables → Actions):

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token (Read & Write) |
| `RENDER_DEPLOY_HOOK` | Render service deploy hook URL |

Render is configured as a **Web Service from an existing image**:
`docker.io/<dockerhub-username>/iris-api:latest`. Every push to `main` publishes a new
image and triggers a redeploy.

## Project structure

```
InferOps/
├── app/
│   ├── __init__.py
│   ├── main.py              # 3 routes, 30 lines
│   └── static/index.html    # form + inline style/script
├── model/train.py           # trains and saves model/iris.joblib
├── tests/test_api.py        # 4 pytest tests
├── docs/                    # screenshots used by this README
├── .github/workflows/ci-cd.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```
