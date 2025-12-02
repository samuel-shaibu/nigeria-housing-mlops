# import necessary libraries
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib

# Clean Data
def clean_price(price_str):
    # if it is already a number, return it.
    if isinstance(price_str, (int, float)):
        return float(price_str)

    # --- FIX: Un-indented this block so it runs for strings ---
    # Remove '₦', commas, and whitespace
    clean_str = str(price_str).replace('₦', '').replace(',', '').strip()

    try:
        return float(clean_str)
    except ValueError:
        return None

# handle numbers (impute missing values) vs categories (convert text to numbers).
def build_pipeline(model_type='rf'):
    # 1. Handle Numeric Data (Bedrooms, Bathrooms)
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # 2. Handle Categorical Data (Town, State)
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # 3. Bundle them together
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, ['bedrooms', 'bathrooms', 'toilets', 'parking_space']),
            ('cat', categorical_transformer, ['town', 'state'])
        ]
    )

    # 4. Build the model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42)) # Increased estimators
    ])

    return model


if __name__ == '__main__':
    print("Loading Data...")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'nigeria_houses.csv')
    
    # Error handling in case file isn't found
    if not os.path.exists(DATA_PATH):
        print(f"Error: File not found at {DATA_PATH}")
        exit()
        
    df = pd.read_csv(DATA_PATH)

    # Standardise column names
    # MAPPING: 'CSV Name': 'Code Name'
    df = df.rename(
        columns={
            'Bedrooms': 'bedrooms',
            'Bathrooms': 'bathrooms',
            'Toilets': 'toilets',
            'Parking Spaces': 'parking_space', # Matches your CSV exactly
            'District': 'town',                # <--- THE FIX: Map District to town
            'State': 'state',
            'Price': 'price',
        }
    )

    # Apply our cleaning function
    df['cleaned_price'] = df['price'].apply(clean_price)

    # Filter out bad data (rows without prices)
    df = df.dropna(subset=['cleaned_price'])
    
    # --- CRITICAL FIX FOR SCORE ---
    # Filter out Rent (too low) and Outliers (too high)
    # Keeping only prices between 1 Million and 500 Million
    print(f"Original Row Count: {len(df)}")
    df = df[(df['cleaned_price'] > 1_000_000) & (df['cleaned_price'] < 500_000_000)]
    print(f"Cleaned Row Count (Sales Only): {len(df)}")
    # ------------------------------

    # Define X (Features) and y(Target)
    # Ensure these columns actually exist in your CSV after renaming
    features = ['bedrooms', 'bathrooms', 'toilets', 'parking_space', 'town', 'state']
    # Select only columns that exist
    features = [c for c in features if c in df.columns]
    
    X = df[features]
    y = df['cleaned_price']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build and Train
    print("Training model...")
    model = build_pipeline()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model Score (R^2): {score:.2f}")

    # SAVE THE ARTIFACT
    # Ensure app folder exists
    model_path = os.path.join(BASE_DIR, 'app', 'housing_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")