import pandas as pd
from datetime import datetime, timedelta

def calculate_min_stock(sales: pd.DataFrame, coverage_days: int = 3) -> pd.DataFrame:
    """Calcula stock mínimo dinámico para cubrir X días de demanda, usando solo los últimos 2 meses de ventas."""
    
    # Asegurarse de que sale_date sea datetime
    sales["sale_date"] = pd.to_datetime(sales["sale_date"])

    # Calcular fecha de corte (hace 2 meses desde hoy)
    today = pd.Timestamp.today()
    two_months_ago = today - pd.DateOffset(months=2)

    # Filtrar ventas de los últimos 2 meses
    recent_sales = sales[sales["sale_date"] >= two_months_ago]

    # Calcular promedio diario por producto
    avg_daily = recent_sales.groupby("product_id")["quantity"].mean().reset_index()
    
    # Calcular stock mínimo
    avg_daily["min_stock"] = avg_daily["quantity"] * coverage_days
    
    return avg_daily[["product_id", "min_stock"]]

