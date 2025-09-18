import pandas as pd

def select_suppliers1(purchases: pd.DataFrame) -> pd.DataFrame:

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


def select_suppliers(purchases: pd.DataFrame) -> pd.DataFrame:
    """
    Selecciona proveedor óptimo por producto según mejor precio en últimos 30 días,
    o el proveedor más reciente si no hay registros recientes.

    Params
    ------
    purchases : DataFrame con columnas:
        ['purchase_date', 'product_id', 'supplier_name', 'quantity_purchased', 'total_amount']

    Returns
    -------
    DataFrame con columnas:
        ['product_id', 'best_supplier', 'best_cost']
    """
    purchases = purchases.copy()

    # Convertir tipos y calcular unit_cost
    purchases["purchase_date"] = pd.to_datetime(purchases["purchase_date"], errors='coerce')
    purchases = purchases.dropna(subset=["purchase_date"])
    purchases["product_id"] = purchases["product_id"].astype(str).str.zfill(10)
    purchases["supplier_name"] = purchases["supplier_name"].astype(str)

    # Filtrar compras válidas
    purchases = purchases[purchases["quantity_purchased"] > 0].copy()
    purchases["unit_cost"] = purchases["total_amount"] / purchases["quantity_purchased"]

    # Fecha límite para compras recientes
    cutoff = purchases["purchase_date"].max() - pd.Timedelta(days=30)
    recent = purchases[purchases["purchase_date"] >= cutoff].copy()

    # 1. Mejores proveedores recientes
    recent_best = (
        recent.sort_values(["product_id", "unit_cost", "purchase_date"])
              .drop_duplicates("product_id", keep="first")
    )

    # 2. Productos sin compras recientes
    all_products = set(purchases["product_id"])
    recent_products = set(recent_best["product_id"])
    missing_products = all_products - recent_products

    fallback = (
        purchases[purchases["product_id"].isin(missing_products)]
        .sort_values(["product_id", "purchase_date"])
        .drop_duplicates("product_id", keep="last")
    )

    # 3. Combinar ambos
    best = pd.concat([recent_best, fallback], ignore_index=True)

    # 4. Devolver DataFrame final
    return best[["product_id", "supplier_name", "unit_cost"]].rename(
        columns={"supplier_name": "best_supplier", "unit_cost": "best_cost"}
    ).reset_index(drop=True)
