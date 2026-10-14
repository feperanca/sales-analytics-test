from pathlib import Path
from sqlite3 import Connection
import pandas as pd

def compute_revenue_per_customer_month(conn: Connection, from_date: str = None, to_date: str = None) -> pd.DataFrame:
    query = """
    SELECT
        c.customer_id,
        c.name,
        c.country,
        strftime('%Y-%m', o.order_date) AS year_month,
        ROUND(SUM(o.total_amount), 2) AS revenue
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.total_amount >= 0
    """
    params = []
    if from_date:
        query += " AND o.order_date >= ?"
        params.append(from_date)

    if to_date:
        query += " AND o.order_date <= ?"
        params.append(to_date)
        
    query += """
    GROUP BY
        c.customer_id,
        c.name,
        c.country,
        year_month
    ORDER BY
        year_month ASC,
        revenue DESC
    """
    
    return pd.read_sql_query(query, conn, params=params)

    df = pd.DataFrame(columns=["customer_id", "name", "country", "year_month", "revenue"])
    df.loc[0] = [6, "Quantum Analytics", "US", "2025-01", 3200]  # Sample row
    return df

def compute_top_products(conn: Connection, limit: int = 5, from_date: str = None, to_date: str = None) -> pd.DataFrame:
    query = """
    SELECT
        i.product_name,
        o.order_date AS order_date,
	ROUND(SUM(i.quantity * i.unit_price), 2) AS total_revenue    
    FROM order_items i
    INNER JOIN orders o
        ON i.order_id = o.order_id
        WHERE 1=1
    """
    params = []
    if from_date:
                query += " AND o.order_date >= ?"
                params.append(from_date)
        
    if to_date:
                query += " AND o.order_date <= ?"
                params.append(to_date)
                
    query += """
    GROUP BY i.product_name,
    o.order_date
    ORDER BY total_revenue DESC
    LIMIT ?
    """

    return pd.read_sql_query(query, conn, params=params + [limit])
    df = pd.DataFrame(columns=["product_name", "total_revenue"])
    df.loc[0] = ["Laptop Pro", 6000]  # Sample row
    return df

def generate_reports(conn: Connection, output_dir: Path, from_date: str = None, to_date: str = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    df_rev = compute_revenue_per_customer_month(conn,from_date=from_date, to_date=to_date)
    df_rev.to_csv(output_dir / "revenue_per_customer_per_month.csv", index=False)

    df_top = compute_top_products(conn, limit=5,from_date=from_date, to_date=to_date)
    df_top.to_csv(output_dir / "top_products.csv", index=False)
