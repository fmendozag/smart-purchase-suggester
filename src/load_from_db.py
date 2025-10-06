import pandas as pd
import urllib
from sqlalchemy import create_engine


def get_sqlalchemy_engine():
    driver = "ODBC Driver 17 for SQL Server"
    server = "ServerName"
    database = "DataBaseName"
    username = "YourUser"
    password = "YourPassword"

    # Parámetros ODBC codificados correctamente
    params = urllib.parse.quote_plus(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=Yes;"
    )

    connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
    return create_engine(connection_string)




# === Cargar Ventas ===
def load_sales_db() -> pd.DataFrame:
    query = """
    SELECT
        CONVERT(CHAR(10), f.Fecha, 103) AS sale_date,
        p.ID AS product_id,
        SUM(dt.Cantidad) AS quantity,
        SUM(dt.Total) AS total_amount
    FROM VEN_FACTURAS f
    INNER JOIN VEN_FACTURAS_DT dt ON f.ID = dt.FacturaID
    INNER JOIN INV_PRODUCTOS p ON dt.ProductoID = p.ID
    WHERE f.Anulado = 0
    GROUP BY CONVERT(CHAR(10), f.Fecha, 103), p.ID
    """
    engine = get_sqlalchemy_engine()
    df = pd.read_sql(query, engine)

    df['product_id'] = df['product_id'].astype(str).str.zfill(10)
    df['sale_date'] = pd.to_datetime(df['sale_date'], format="%d/%m/%Y", errors="coerce")
    df['quantity'] = df['quantity'].astype(float)
    df['total_amount'] = df['total_amount'].astype(float)
    return df.dropna()


# === Cargar Compras ===
def load_purchases_db() -> pd.DataFrame:
    query = """
    SELECT
        CONVERT(CHAR(10), c.Fecha, 103) AS purchase_date,
        p.ID AS product_id,
        ac.Nombre AS supplier_name,
        dt.Cantidad AS quantity_purchased,
        dt.Total AS total_amount
    FROM COM_FACTURAS c
    INNER JOIN COM_FACTURAS_DT dt ON c.ID = dt.FacturaID
    INNER JOIN INV_PRODUCTOS p ON p.ID = dt.ProductoID
    INNER JOIN ACR_ACREEDORES ac ON c.ProveedorID = ac.ID
    WHERE c.Anulado = 0
      AND YEAR(c.Fecha) > 2022
    GROUP BY CONVERT(CHAR(10), c.Fecha, 103), p.ID, ac.Nombre, dt.Cantidad, dt.Total
    ORDER BY product_id
    """
    engine = get_sqlalchemy_engine()
    df = pd.read_sql(query, engine)

    df['product_id'] = df['product_id'].astype(str).str.zfill(10)
    df['purchase_date'] = pd.to_datetime(df['purchase_date'], format="%d/%m/%Y", errors="coerce")
    df['quantity_purchased'] = df['quantity_purchased'].astype(float)
    df['total_amount'] = df['total_amount'].astype(float)
    df['supplier_name'] = df['supplier_name'].str.slice(0, 25)  # Limitar a 25 caracteres
    return df


# === Cargar Productos ===
def load_products_db() -> pd.DataFrame:
    query = """
    SELECT 
        product_id,
        product_code,
        product_name,
        unit_conversion,
        SUM(current_stock) AS current_stock
    FROM (
        SELECT 
            p.ID AS product_id,
            p.Código AS product_code,
            p.Nombre AS product_name,
            ISNULL(
                SUM(
                    CASE 
                        WHEN cd.Egreso = 1 THEN ROUND(-cd.Cantidad, 2)
                        ELSE ROUND(cd.Cantidad, 2)
                    END
                ), 
            0) AS current_stock,
            p.Conversión AS unit_conversion
        FROM INV_PRODUCTOS p
        INNER JOIN INV_PRODUCTOS_CARDEX cd ON p.ID = cd.ProductoID
        WHERE 
            p.Anulado = 0 
            AND cd.Anulado = 0 
            AND cd.BodegaID = '0000000001'
        GROUP BY 
            p.ID, p.Código, p.Nombre, p.Conversión

        UNION ALL

        SELECT 
            p.ID AS product_id,
            p.Código AS product_code,
            p.Nombre AS product_name,
            ISNULL(
                SUM(
                    CASE 
                        WHEN cd.Egreso = 1 THEN ROUND(-cd.Cantidad, 2)
                        ELSE ROUND(cd.Cantidad, 2)
                    END
                ), 
            0) AS current_stock,
            p.Conversión AS unit_conversion
        FROM [192.168.160.5].BELBRY.dbo.INV_PRODUCTOS p
        INNER JOIN [192.168.160.5].BELBRY.dbo.INV_PRODUCTOS_CARDEX cd ON p.ID = cd.ProductoID
        WHERE 
            p.Anulado = 0 
            AND cd.Anulado = 0 
            AND cd.BodegaID = '0000000011'
        GROUP BY 
            p.ID, p.Código, p.Nombre, p.Conversión
    ) AS UNION_RESULT
    GROUP BY
        product_id,
        product_code,
        product_name,
        unit_conversion
    ORDER BY 
        product_id
    """
    engine = get_sqlalchemy_engine()
    df = pd.read_sql(query, engine)

    df['product_id'] = df['product_id'].astype(str).str.zfill(10)
    return df


# === Cargar Empaques ===
def load_packaging_db() -> pd.DataFrame:
    query = """
    SELECT 
        ProductoID AS product_id,
        Nombre AS name,
        Factor AS unit_conversion
    FROM INV_PRODUCTOS_EMPAQUES
    """
    engine = get_sqlalchemy_engine()
    df = pd.read_sql(query, engine)

    df['product_id'] = df['product_id'].astype(str).str.zfill(10)
    return df
