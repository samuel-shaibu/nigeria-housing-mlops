# Import necessary libraries
from flask import Flask, request, jsonify
import joblib
import pandas as pd 


# initialize the flask app
app = Flask(__name__)

# Load the model globally
model = None

try:
    model = joblib.load('app/housing_model.pkl')
    print("Model loaded successfully...")

except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def home():
    return "Nigeria Housing Price Predictor is Live!"

# The API aspect
@app.route('/predict', methods=['POST'])
def predict():
    # check if model is loaded
    if not model:
        return jsonify({'error':'Model is not loaded'}), 500

    try:

        # Get JSON data from the request
        data = request.get_json()
        # Convert to Dataframe
        input_df = pd.DataFrame([data])
        # make prediction
        prediction = model.predict(input_df)[0]
        # return JSON response
        return jsonify({
            'prediction': prediction,
            'message' : "Success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Hugging Face Spaces defaults to port 7860, allows overriding via PORT 
    import os
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)