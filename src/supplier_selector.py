import pandas as pd

def select_suppliers(purchases: pd.DataFrame) -> pd.DataFrame:
    """
    Selecciona proveedor óptimo por producto según mejor precio en últimos 30 días,
    o el proveedor más reciente si no hay registros recientes.

    Mantiene la lógica original y añade: para cada proveedor se toma su ÚLTIMO precio durante los
    últimos 30 días y entre esos precios vigentes se elige el menor.
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

    # Si hay compras recientes:
    if not recent.empty:
        # 1) Para cada (product_id, supplier_name) tomar la última compra (precio vigente de ese proveedor)
        last_price_per_supplier = (
            recent
            .sort_values(["product_id", "supplier_name", "purchase_date"], ascending=[True, True, False])
            .drop_duplicates(["product_id", "supplier_name"], keep="first")
        )

        # 2) Entre esos últimos precios por proveedor, elegir el más barato por producto
        recent_best = (
            last_price_per_supplier
            .sort_values(["product_id", "unit_cost"])
            .drop_duplicates("product_id", keep="first")
        )
    else:
        # no hay recientes -> recent_best vacío
        recent_best = recent.iloc[0:0]  # DataFrame vacío con mismas columnas

    # 3) Productos sin compras recientes (fallback: última compra global)
    all_products = set(purchases["product_id"])
    recent_products = set(recent_best["product_id"]) if not recent_best.empty else set()
    missing_products = all_products - recent_products

    fallback = (
        purchases[purchases["product_id"].isin(missing_products)]
        .sort_values(["product_id", "purchase_date"], ascending=[True, False])
        .drop_duplicates("product_id", keep="first")
    )

    # 4) Combinar recientes (mejores entre proveedores) + fallback (última compra global)
    best = pd.concat([recent_best, fallback], ignore_index=True)

    # 5) Devolver DataFrame final con nombres consistentes
    return best[["product_id", "supplier_name", "unit_cost"]].rename(
        columns={"supplier_name": "best_supplier", "unit_cost": "best_cost"}
    ).reset_index(drop=True)
