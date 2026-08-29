import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")


def load_transactions():
    df = pd.read_csv(DATA_PATH)
    return df