# BloomSage ML Pipeline Demo

**REQUIRED PYTHON VERSION: 3.10**

This is a very barebone project intended as a demonstration on how to utilize our machine learning pipeline for real-time inference in a web application with 2 components: Backend API (using FastAPI) and Frontend UI (using Streamlit).

Please note that this project is only configured to run on your local machine, and no consideration were made for streamlining deployment.

As such, please note that both `backend/.env` and `frontend/.env` environment secrets are version tracked. This is **BAD** practice in a real deployment environment and should be avoided when developing our actual application.

I assume that you are proficient in using the terminal in both POSIX (Linux and MacOS) and Windows environment, and understand the basics of full-stack web application development.

---

## Project Structure

    .
    ├── backend/
    │   ├── backend/
    │   │   ├── util/
    │   │   │   ├── input_processing.py
    │   │   │   └── __init__.py
    │   │   ├── ml_pipeline.py
    │   │   └── __init__.py
    │   ├── .env
    │   ├── requirements.txt
    │   ├── ml_fetch.py
    │   └── main.py
    ├── frontend/
    │   │   └── .streamlit/
    │   │       └── config.toml
    │   ├── .env
    │   ├── requirements.txt
    │   └── main.py
    ├── .gitignore
    └── README.md

These folders will be created during ML assets fetching:

1. `backend/data/`: This folder contains the compiled and compressed recommender database.
2. `backend/models/`: This folder contains trained models.

---

## Getting Started 🚀

Clone this repository:

```bash
git clone https://github.com/rmit-denominator/bloomsage-models-usage-demo.git
```

### Setup Development Environment and fetch ML Assets (Compiled recommender database and trained models from [BloomSage ML Repository Latest Release](https://github.com/rmit-denominator/bloomsage-ml/releases/latest)):

#### Backend Setup:

From the project root directory:

- POSIX Systems:
  ```bash
  cd backend
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ./requirements.txt
  python ./ml_fetch.py
  deactivate
  ```
- Windows Systems:
  ```bash
  cd backend
  python -m venv venv
  venv/Script/activate
  pip install -r ./requirements.txt
  python ./ml_fetch.py
  deactivate
  ```

#### Frontend Setup:

From the project root directory:

- POSIX Systems:
  ```bash
  cd frontend
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ./requirements.txt
  deactivate
  ```
- Windows Systems:
  ```bash
  cd frontend
  python -m venv venv
  venv/Script/activate
  pip install -r ./requirements.txt
  deactivate
  ```

Refer to `backend/requirements.txt` and `frontend/requirements.txt` for information on project dependencies.

### Start Backend and Frontend servers as separate processes:

**Tips:** Use two terminals.

#### Backend:

From the project root directory:

- POSIX Systems:
  ```bash
  cd backend
  source .venv/bin/activate
  python ./main.py
  ```
- Windows Systems:
  ```bash
  cd backend
  venv/Script/activate
  python ./main.py
  ```

#### Frontend:

From the project root directory:

- POSIX Systems:
  ```bash
  cd frontend
  source .venv/bin/activate
  streamlit run ./main.py
  ```
- Windows Systems:
  ```bash
  cd frontend
  venv/Script/activate
  streamlit run ./main.py
  ```

After this, the backend server will be available on [http://localhost:8000](http://localhost:8000/), and the frontend server will be available on [http://localhost:8080](http://localhost:8080).

Please refer to my code, as well as [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://docs.streamlit.io/) documentation for more information.
