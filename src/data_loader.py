import pandas as pd

def load_sales(path:str) -> pd.DataFrame:
    df = pd.read_csv(path, 
                     sep=';',
                     header=None, 
                     names=['sale_date','product_id','quantity','total_amount'],
                     dtype=str)
    df['product_id'] = df['product_id'].astype(str).str.zfill(10)
    df['sale_date'] = pd.to_datetime(df['sale_date'], format="%d/%m/%Y", errors="coerce")
    df['quantity'] = df['quantity'].str.replace(",", ".", regex=False).astype(float)
    df['total_amount'] = df['total_amount'].str.replace(",", ".", regex=False).astype(float)
    return df.dropna()

def load_purchases(path:str) -> pd.DataFrame:
    df = pd.read_csv(path, 
                     sep=';',
                     header=None, 
                     names=['purchase_date','product_id','supplier_name','quantity_purchased','total_amount'],
                     dtype=str)
    df['purchase_date'] = pd.to_datetime(df['purchase_date'],dayfirst=True, errors='coerce')
    df['product_id'] = df['product_id'].astype(str).str.zfill(10)
    df['quantity_purchased'] = df['quantity_purchased'].str.replace(",", ".", regex=False).astype(float)
    df['total_amount'] = df['total_amount'].str.replace(",", ".", regex=False).astype(float)

    return df

def load_products(path:str) -> pd.DataFrame:
    df = pd.read_csv(path,
                     sep=';',
                     header=None, 
                     names=['product_id','product_code','product_name','current_stock','unit_conversion'])
    df['product_id'] = df['product_id'].astype(str).str.zfill(10)    
    return df

