# Nigeria Housing Price Predictor (End-to-End MLOps)

[![GitHub Actions CI](https://github.com/samuel-shaibu/nigeria-housing-mlops/actions/workflows/python-app.yml/badge.svg)](https://github.com/samuel-shaibu/nigeria-housing-mlops/actions)

An end-to-end **Machine Learning Microservice** that predicts housing prices in Nigeria using real-world data.  
This project demonstrates **production-grade MLOps practices**, including automated data pipelines, containerization, CI integration, and model deployment.

---

## System Architecture

The project follows a modular MLOps architecture, separating:
- **Experimentation (Model Development)**
- **Production (API Serving & Deployment)**

```mermaid
graph LR
    A[Raw Data CSV] -->|ETL Pipeline| B(Preprocessing & Cleaning)
    B -->|Train| C{Random Forest Model}
    C -->|Serialize| D[Model Artifact .pkl]
    D -->|Load| E[Flask Microservice]
    E -->|Dockerize| F[Production Container]
    
    subgraph CI_CD [GitHub Actions Pipeline]
    G[Push Code] --> H[Install Dependencies]
    H --> I[Run Pytest]
    I -->|Pass| J[Build Docker Image]
    end

Tech Stack
Core

Python 3.12
Pandas
Scikit-Learn (Pipelines)

API

Flask (RESTful Microservice)

Containerization

Docker (Multi-stage builds, Slim images)

CI/CD

GitHub Actions (Automated Testing)

Environment

WSL 2 (Ubuntu Linux)


Quick Start
You can run this project using Docker (recommended) or directly via Python.
Option 1: Using Docker (Production Simulation)
# Build the container
docker build -t housing-predictor .

# Run the container
docker run -p 5000:5000 housing-predictor
Option 2: Local Python Environment (Development)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

# Train the model (creates model.pkl)
python model_development/train_model.py

# Start the API
python app/main.py
The API will be available at http://localhost:5000

API Usage
Endpoint
POST /predict
Example Request (JSON payload)
{
  "bedrooms": 4,
  "bathrooms": 4,
  "toilets": 5,
  "parking_space": 3,
  "town": "Lekki",
  "state": "Lagos"
}
Example Response
{
  "formatted_price": "₦ 112,655,283.33",
  "predicted_price": 112655283.33379728,
  "status": "success"
}

Project Structure
nigeria-housing-mlops/
├── .github/workflows/    # CI/CD Pipeline
├── app/
│   └── main.py           # Flask API
├── data/                 # Local data (gitignored)
├── model_development/
│   └── train_model.py
├── tests/
│   └── test_app.py
├── Dockerfile
├── requirements.txt
└── README.md

Testing
pytest
Enjoy predicting housing prices across Nigeria!