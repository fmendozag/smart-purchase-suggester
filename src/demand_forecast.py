import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_forecast(
    sales: pd.DataFrame, 
    days: int = 45, 
    method: str = "mean", 
    window: int = 7
) -> pd.DataFrame:
    """
    Calcula forecast de ventas diarias por producto según diferentes métodos.
    
    Params
    ------
    sales : DataFrame
        Debe contener ['sale_date','product_id','quantity']
    days : int
        Número de días hacia atrás que se analizarán (ej: últimos 45 días).
    method : str
        Método de forecast: "mean", "rolling", "weighted", "trend"
    window : int
        Ventana para el promedio móvil o ponderado.
    
    Returns
    -------
    DataFrame con ['product_id','forecast']
    """

    sales["sale_date"] = pd.to_datetime(sales["sale_date"])
    cutoff = sales["sale_date"].max() - pd.Timedelta(days=days)
    sales = sales[sales["sale_date"] >= cutoff]

    forecasts = []

    for product_id, group in sales.groupby("product_id"):
        # ventas diarias
        daily_sales = group.groupby("sale_date")["quantity"].sum().sort_index()

        if daily_sales.empty:
            forecasts.append({"product_id": product_id, "forecast": 0.0})
            continue

        forecast_value = 0.0

        if method == "mean":
            # promedio simple
            forecast_value = daily_sales.mean()

        elif method == "rolling":
            # promedio móvil últimos N días
            forecast_value = daily_sales.rolling(window=window).mean().iloc[-1]

        elif method == "weighted":
            # promedio ponderado → más peso a días recientes
            weights = np.arange(1, len(daily_sales[-window:]) + 1)
            forecast_value = np.average(daily_sales[-window:], weights=weights)

        elif method == "trend":
            # regresión lineal para capturar tendencia
            X = np.arange(len(daily_sales)).reshape(-1, 1)
            y = daily_sales.values
            model = LinearRegression().fit(X, y)
            forecast_value = model.predict([[len(daily_sales)]])[0]

        forecasts.append({
            "product_id": product_id, 
            "forecast": max(forecast_value, 0)  # evitar negativos
        })

    return pd.DataFrame(forecasts)
