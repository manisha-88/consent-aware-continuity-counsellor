from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "synthetic"


def load_clients() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "clients.csv")


def load_sessions() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sessions.csv")


def load_goals() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "goals.csv")


def load_consent_choices() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "consent_choices.csv")


def load_pending_actions() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "pending_actions.csv")