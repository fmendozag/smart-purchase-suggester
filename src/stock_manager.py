import pandas as pd

def calculate_min_stock(sales: pd.DataFrame, days: int = 3) -> pd.DataFrame:
    """Calcula stock mínimo dinámico para cubrir X días de demanda."""
    sales["sale_date"] = pd.to_datetime(sales["sale_date"])
    avg_daily = sales.groupby("product_id")["quantity"].mean().reset_index()
    avg_daily["min_stock"] = avg_daily["quantity"] * days
    return avg_daily[["product_id","min_stock"]]
