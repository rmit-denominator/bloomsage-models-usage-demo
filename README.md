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
    │   ├── favicon
    │   │   └── Logo_BloomSage Logomark.png
    │   ├── features.py
    │   ├── main.py
    │   └── requirements.txt
    ├── mockup-ecommerce
    │   ├── app.py
    │   ├── procfile
    │   ├── requirements.txt
    │   ├── static
    │   │   ├── imgs
    │   │   └── style.css
    │   └── templates
    │       ├── index.html
    │       └── product_detail.html
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

**Demo**: https://faithful-adequate-mudfish.ngrok-free.app/

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
Open another console for `ngrok`
```bash
ngrok tunnel --label edge=edghts_2atupyk74q8O638a0bdIkg9CPro http://localhost:8000
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
Open another console for `ngrok`
```bash
ngrok tunnel --label edge=edghts_2atupyk74q8O638a0bdIkg9CPro http://localhost:8000
```
#### Frontend Setup `cd frontend`:

**Demo**: https://bloomsage.streamlit.app/

- UNIX/Linux:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ./requirements.txt
  deactivate
  ```
  ```bash
  source .venv/bin/activate
  streamlit run ./main.py --server.port 8081
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

**Demo**: https://bloomsage-mockup.netlify.app/

- UNIX/Linux:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r ./requirements.txt
  deactivate
  ```
  ```bash
  source .venv/bin/activate
  flask --app app --debug run
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
  flask --app app --debug run
  ```

Refer to `backend/requirements.txt`, `frontend/requirements.txt`, `mockup-ecommerce/requirements.txt` for information on project dependencies.
