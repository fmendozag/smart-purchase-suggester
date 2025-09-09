import pandas as pd

def load_sales(path:str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, names=['sale_date','product_id','quantity','total_amount'])
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    return df.dropna()

def load_purchases(path:str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, names=['purchase_date','product_id','supplier_name','quantity_purchased','total_amount'])
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    return df

def load_products(path:str) -> pd.DataFrame:
    df = pd.read_csv(path,header=None, names=['product_id','product_code','product_name','current_stock','unit_conversion'])
    return df

