import pandas as pd

def select_suppliers(purchases: pd.DataFrame) -> pd.DataFrame:
    """
    Selecciona proveedor óptimo por producto según mejor precio en últimos 30 días
    o último proveedor si no hay registros recientes.
    
    Params
    ------
    purchases : DataFrame con ['purchase_date','product_id','supplier_id','unit_cost']
    
    Returns
    -------
    DataFrame con ['product_id','best_supplier','best_cost']
    """
    purchases["purchase_date"] = pd.to_datetime(purchases["purchase_date"])
    cutoff = purchases["purchase_date"].max() - pd.Timedelta(days=30)
    
    recent = purchases[purchases["purchase_date"] >= cutoff]

    if not recent.empty:
        best = recent.sort_values(["product_id","unit_cost"]).drop_duplicates("product_id", keep="first")
    else:
        best = purchases.sort_values("purchase_date").drop_duplicates("product_id", keep="last")

    return best[["product_id","supplier_id","unit_cost"]].rename(
        columns={"supplier_id":"best_supplier","unit_cost":"best_cost"}
    )
