import pandas as pd
import math
from .stock_manager import calculate_min_stock
from .supplier_selector import select_suppliers
import numpy as np

def generate_purchase_suggestion(
    sales_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    stock_df: pd.DataFrame,
    products_df: pd.DataFrame,
    purchases_df: pd.DataFrame,
    coverage_days: int = 7,
    safety_days: int = 3
) -> pd.DataFrame:
    """
    Genera la tabla final de sugerido de compras.
    Args:
      sales_df: ventas crudas (necesario para calcular min_stock con tu función).
      forecast_df: DataFrame con ['product_id','forecast'] (forecast diario).
      stock_df: DataFrame con ['product_id','current_stock'].
      products_df: DataFrame con ['product_id','product_code','product_name', ...].
      purchases_df: historial de compras (para seleccionar proveedor).
      coverage_days: días que queremos cubrir (7,15,21,30).
      safety_days: días de stock de seguridad (ej. 2 o 3).
    Returns:
      DataFrame final con columnas legibles: product_code, product_name, current_stock,
      min_stock (int), expected_demand (int), suggested_purchase (int), best_supplier, best_cost, est_total_cost
    """

    # Normalizar tipos de product_id (strings, padded)
    for df in (forecast_df, stock_df, products_df, purchases_df):
        if 'product_id' in df.columns:
            df['product_id'] = df['product_id'].astype(str)

    # Asegurar columnas en stock_df
    if 'current_stock' not in stock_df.columns:
        stock_df = stock_df.rename(columns={stock_df.columns[1]: 'current_stock'})  # si tiene otro nombre

    # 1) calcular min_stock (safety stock) usando tu función que toma ventas y coverage_days (safety_days)
    min_stock_df = calculate_min_stock(sales_df, coverage_days=safety_days)  # devuelve product_id,min_stock (float)

    # 2) expected demand = forecast diario * coverage_days
    forecast_df = forecast_df.copy()
    forecast_df['forecast'] = pd.to_numeric(forecast_df['forecast'], errors='coerce').fillna(0.0)
    forecast_df['expected_demand'] = forecast_df['forecast'] * coverage_days

    # 3) merge: forecast + stock + min_stock
    merged = forecast_df.merge(stock_df[['product_id','current_stock']], on='product_id', how='left')
    merged = merged.merge(min_stock_df, on='product_id', how='left')

    # rellenar nulos
    merged['current_stock'] = merged['current_stock'].fillna(0)
    merged['min_stock'] = merged['min_stock'].fillna(0)

    # 4) cálculo sugerido: expected_demand + min_stock - current_stock
    merged['raw_suggested'] = (merged['expected_demand'] + merged['min_stock']) - merged['current_stock']
    merged['suggested_purchase'] = np.where(merged['raw_suggested'] > 0, np.ceil(merged['raw_suggested']), 0).astype(int)

    # redondeos: min_stock entero (ceil)
    merged['min_stock'] = np.ceil(merged['min_stock']).astype(int)
    # expected_demand a entero (ceil) para mostrar
    merged['expected_demand'] = np.ceil(merged['expected_demand']).astype(int)

    # 5) seleccionar proveedor óptimo (usa la función que tengas)
    suppliers_df = select_suppliers(purchases_df)  # debe retornar product_id, best_supplier, best_cost
    # asegurar tipos
    suppliers_df['product_id'] = suppliers_df['product_id'].astype(str)

    merged = merged.merge(suppliers_df[['product_id','best_supplier','best_cost']], on='product_id', how='left')

    # 6) merge con productos para mostrar code/name
    # asegurar nombres en products_df: product_id, product_code, product_name
    if 'product_code' not in products_df.columns and 'product_name' not in products_df.columns:
        # si products tiene otros nombres, intenta deducir:
        products_df = products_df.rename(columns={products_df.columns[1]:'product_code', products_df.columns[2]:'product_name'})

    merged = merged.merge(products_df[['product_id','product_code','product_name']], on='product_id', how='left')

    # 7) cálculo estimado total cost (si best_cost existe)
    merged['best_cost'] = pd.to_numeric(merged['best_cost'], errors='coerce')
    merged['best_cost_rounded'] = merged['best_cost'].round(2)
    merged['est_total_cost'] = (merged['best_cost'] * merged['suggested_purchase']).round(2)

    # 8) seleccionar y reordenar columnas amigables (ocultamos product_id al final)
    final = merged[[
        'product_id','product_code','product_name',
        'current_stock','min_stock','expected_demand','suggested_purchase',
        'best_supplier','best_cost_rounded','est_total_cost'
    ]].rename(columns={
        'best_cost_rounded':'best_cost'
    })
    

    # 9) Si quieres ocultar product_id para mostrar, puedes:
    display_df = final.drop(columns=['product_id']).copy()

    # 10) informar si hay productos sin proveedor
    display_df['best_supplier'] = display_df['best_supplier'].fillna("UNKNOWN")
    display_df['best_cost'] = display_df['best_cost'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")
    
    display_df =  display_df[display_df['suggested_purchase'] > 0].reset_index(drop=True)

    return display_df




'''def generate_purchase_suggestion(sales: pd.DataFrame, stock: pd.DataFrame, coverage_days: int = 7) -> pd.DataFrame:
    """
    Genera sugerencias de compra en base al stock mínimo requerido vs. stock actual.
    Usa el cálculo dinámico de min_stock de los últimos 2 meses.
    """

    # 1. Calcular stock mínimo requerido dinámicamente
    min_stock_df = calculate_min_stock(sales, coverage_days)

    # 2. Unir con stock actual
    merged = min_stock_df.merge(stock, on="product_id", how="left")

    # Asegurarse de que la columna de stock actual exista
    if "current_stock" not in merged.columns:
        merged["current_stock"] = 0  

    # 3. Calcular sugerido
    merged["suggested_purchase"] = (merged["min_stock"] - merged["current_stock"]).clip(lower=0)

    return merged[["product_id", "current_stock", "min_stock", "suggested_purchase"]]'''