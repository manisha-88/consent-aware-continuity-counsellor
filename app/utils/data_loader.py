from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "synthetic"

def _load_and_clean_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    if not path.exists():
        alt_path = Path("data/synthetic") / filename
        if alt_path.exists():
            path = alt_path
        else:
            raise FileNotFoundError(f"Could not find {filename} at {path} or {alt_path}")
            
    df = pd.read_csv(path, encoding="utf-8-sig")
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Clean all string/object columns to eliminate hidden spaces or quotes
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip().str.replace('"', "").str.replace("'", "")
        
    return df

def load_clients() -> pd.DataFrame:
    return _load_and_clean_csv("clients.csv")

def load_sessions() -> pd.DataFrame:
    return _load_and_clean_csv("sessions.csv")

def load_goals() -> pd.DataFrame:
    return _load_and_clean_csv("goals.csv")

def load_consent_choices() -> pd.DataFrame:
    df = _load_and_clean_csv("consent_choices.csv")
    if "status" in df.columns:
        df["status"] = df["status"].str.lower()
    return df

def load_pending_actions() -> pd.DataFrame:
    return _load_and_clean_csv("pending_actions.csv")

