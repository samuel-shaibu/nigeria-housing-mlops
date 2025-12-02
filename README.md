🏠 Nigeria Housing Price Predictor (End-to-End MLOps)
An end-to-end Machine Learning Microservice that predicts housing prices in Nigeria based on real-world data. This project demonstrates production-grade MLOps practices, including automated data pipelines, containerization, and Continuous Integration (CI).
🏗 System Architecture
The project follows a modular MLOps architecture, separating model training (Experimentation) from API serving (Production).
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
🛠 Tech StackCore: Python 3.12, Pandas, Scikit-Learn (Pipelines)API: Flask (RESTful Microservice)Containerization: Docker (Multi-stage builds, Slim images)CI/CD: GitHub Actions (Automated Testing)Environment: WSL 2 (Ubuntu Linux)🚀 Quick StartYou can run this project locally using Docker (recommended) or direct Python execution.Option 1: Using Docker (Production Simulation)Ensure Docker Desktop is running.
# 1. Build the lightweight container
docker build -t housing-predictor .

# 2. Run the container (Maps port 5000)
docker run -p 5000:5000 housing-predictor
Option 2: Local Python Env (Development)# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (Generates the .pkl artifact)
python model_development/train_model.py

# 4. Start the API server
python app/main.py
⚡ API Usag eOnce the server is running (at http://localhost:5000), you can send predictions via POST request.Endpoint: /predictMethod: POSTExample Request (cURL)curl -X POST [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) \
     -H "Content-Type: application/json" \
     -d '{"bedrooms": 4, "bathrooms": 4, "toilets": 5, "parking_space": 3, "town": "Lekki", "state": "Lagos"}'
Example Response{
    "formatted_price": "₦ 112,655,283.33",
    "predicted_price": 112655283.33379728,
    "status": "success"
}
📂 Project Structure nigeria-housing-mlops/
├── .github/workflows/    # CI/CD Pipeline Configuration
├── app/                  # Flask Production App
│   └── main.py           # API Entry Point
├── data/                 # Local Data Storage (Ignored by Git)
├── model_development/    # Data Science Environment
│   └── train_model.py    # Training & Serialization Script
├── tests/                # Automated Tests
│   └── test_app.py       # API Integration Tests
├── Dockerfile            # Container Instructions
├── requirements.txt      # Dependency Lockfile
└── README.md             # Project Documentation
🧪 TestingThe project includes automated integration tests using pytest to ensure API reliability.# Run tests locally
pytest
