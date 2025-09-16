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
    purchases = purchases.copy()
    purchases["purchase_date"] = pd.to_datetime(purchases["purchase_date"], errors='coerce')
    purchases["product_id"] = purchases["product_id"].astype(str).str.zfill(10)
    
    purchases = purchases[purchases["quantity_purchased"] > 0].copy()
    purchases['unit_cost'] = purchases['total_amount'] / purchases['quantity_purchased']
    
    cutoff = purchases["purchase_date"].max() - pd.Timedelta(days=30) 
    
    recent = purchases[purchases["purchase_date"] >= cutoff].copy()
    
    #recent['unit_cost'] = recent['total_amount'] / recent['quantity_purchased']

    if not recent.empty:
        best = recent.sort_values(["product_id","unit_cost"]).drop_duplicates("product_id", keep="first")
    else:
        best = purchases.sort_values("purchase_date").drop_duplicates("product_id", keep="last")

    return best[["product_id","supplier_name","unit_cost"]].rename(
        columns={"supplier_name":"best_supplier","unit_cost":"best_cost"}
    )
