# Load and clean datasets
import os
import pandas as pd

# Get project root whether in script or notebook
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))

def load_raw_data(file):
    if os.path.isabs(file):
        data_path = file
    else:
        data_path = os.path.join(BASE_DIR, "data", "raw", file)

    print(f"📂 Loading from: {data_path}")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ File not found at: {data_path}")

    df = pd.read_csv(data_path)
    return df



def clean_raw_data(df):
    # Drop rows with any missing values
    df = df.dropna()

    # Fill missing values appropriately (if dropna isn't used)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)

    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(df, drop_first=True)        
    print(f"🧹 Cleaned data shape: {df_encoded.shape}")
    return df_encoded

def save_preprocessed_data(df_encoded, filename="cleaned_data.csv"):
    process_path = os.path.join(BASE_DIR, "data", "processed", filename)
    df_encoded.to_csv(process_path, index=False)
    print(f"💾 Saved cleaned data to: {process_path}")




    
