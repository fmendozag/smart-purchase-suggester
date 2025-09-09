import pandas as pd

def calculate_moving_average(sales:pd.DataFrame, window: int ) -> pd.DataFrame:
     sales["sale_date"] = pd.to_datetime(sales["sale_date"])
    
     forecasts = []

    # Iterar sobre cada producto
     for product_id, group in sales.groupby("product_id"):
        # Agrupar por fecha
        daily_sales = group.groupby("sale_date")["quantity"].sum().sort_index()
        
        # Calcular promedio móvil
        rolling_mean = daily_sales.rolling(window=window).mean()
        
        # Último valor del promedio móvil (el forecast)
        forecast = rolling_mean.iloc[-1] if not rolling_mean.empty else 0.0
        
        forecasts.append({"product_id": product_id, "forecast": forecast})
    
     return pd.DataFrame(forecasts)