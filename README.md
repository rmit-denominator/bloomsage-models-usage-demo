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
    │   ├── machine_learning/
    │   │   ├── util/
    │   │   │   ├── input_processing.py
    │   │   │   └── __init__.py
    │   │   ├── pipeline.py
    │   │   └── __init__.py
    │   ├── .env
    │   ├── requirements.txt
    │   ├── ml_fetch.py
    │   └── main.py
    ├── frontend
        ├── favicon
        │   └── Logo_BloomSage Logomark.png
        ├── features.py
        ├── main.py
        └── requirements.txt
    ├── mockup-ecommerce
        ├── app.py
        ├── procfile
        ├── requirements.txt
        ├── static
        │   ├── imgs
        │   └── style.css
        └── templates
            ├── index.html
            └── product_detail.html
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

***At the same time, open 3 terminal consoles to run 3 servers below***
### Setup Development Environment and fetch ML Assets (Compiled recommender database and trained models from [BloomSage ML Repository Latest Release](https://github.com/rmit-denominator/bloomsage-ml/releases/latest)):

#### Backend Setup `cd backend`:

- UNIX/Linux:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ./requirements.txt
  python ./ml_fetch.py
  deactivate
  ```
  ```bash
  source .venv/bin/activate
  python ./main.py
  ```
- Windows Systems:
  ```bash
  python -m venv venv
  venv/Script/activate
  pip install -r ./requirements.txt
  python ./ml_fetch.py
  deactivate
  ```
  ```bash
  venv/Script/activate
  python ./main.py
  ```

#### Frontend Setup `cd frontend`:

- UNIX/Linux:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ./requirements.txt
  deactivate
  ```
  ```bash
  source .venv/bin/activate
  streamlit run ./main.py
  ```
- Windows Systems:
  ```bash
  python -m venv venv
  venv/Script/activate
  pip install -r ./requirements.txt
  deactivate
  ```
  ```bash
  venv/Script/activate
  streamlit run ./main.py
  ```

#### Mockup Ecommerce Setup `cd mockup-ecommerce`:
- UNIX/Linux:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ./requirements.txt
  deactivate
  ```
  ```bash
  source .venv/bin/activate
  python ./app.py
  ```
- Windows Systems:
  ```bash
  python -m venv venv
  venv/Script/activate
  pip install -r ./requirements.txt
  deactivate
  ```
  ```bash
  venv/Script/activate
  python ./app.py
  ```

Refer to `backend/requirements.txt` and `frontend/requirements.txt` for information on project dependencies.
