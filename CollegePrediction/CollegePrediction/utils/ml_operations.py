# ml_operations.py
# ml_operations.py

from pycaret.classification import predict_model
from pycaret.classification import load_model
import pandas as pd

# Load the PyCaret model
def load_pycaret_model():
    model_path = 'models\multiclass.pkl'  # Update with the correct path
    model = load_model(model_path)
    return model

# Make predictions using the loaded model
def predict(input_data):
    model = load_pycaret_model()
    input_df = pd.DataFrame([input_data])  # Convert input_data to a DataFrame
    result = predict_model(model, input_df)
    return result['Label'].tolist()
