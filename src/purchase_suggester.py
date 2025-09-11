import pandas as pd
import math

def suggest_purchases(
    forecast_df: pd.DataFrame, 
    stock_dict: dict, 
    days_to_cover: int = 7, 
    box_size: int = None
) -> pd.DataFrame:
    """
    Genera sugerido de compras a partir del forecast diario y stock actual.

    Params
    ------
    forecast_df : DataFrame
        Debe contener ['product_id','forecast'] (forecast = ventas promedio diarias).
    stock_dict : dict
        Diccionario con stock actual {product_id: stock}.
    days_to_cover : int
        Días de cobertura que quieres (ej: 7, 15, 30).
    box_size : int, optional
        Si se indica, redondea la compra sugerida a múltiplos de este valor.

    Returns
    -------
    DataFrame con ['product_id','daily_forecast','stock','needed','suggested']
    """
    results = []

    for _, row in forecast_df.iterrows():
        pid = row["product_id"]
        daily_forecast = row["forecast"]

        # Unidades que necesito en el periodo
        needed = daily_forecast * days_to_cover

        # Stock actual (si no está en dict → 0)
        stock = stock_dict.get(pid, 0)

        # Lo que falta
        to_buy = max(needed - stock, 0)

        # Redondeo a caja si aplica
        if box_size and to_buy > 0:
            to_buy = math.ceil(to_buy / box_size) * box_size

        results.append({
            "product_id": pid,
            "daily_forecast": round(daily_forecast, 2),
            "stock": stock,
            "needed": round(needed, 2),
            "suggested": int(to_buy)
        })

    return pd.DataFrame(results)
 