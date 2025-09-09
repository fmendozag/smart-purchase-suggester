import pandas as pd

def load_sales(path:str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, names=[''])

def load_purchases(path:str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=['Date'])

def load_products(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

