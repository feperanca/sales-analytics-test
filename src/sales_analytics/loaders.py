from pathlib import Path
from sqlite3 import Connection
import logging

import pandas as pd

from .config import DATA_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_all_data(conn: Connection) -> None:
    load_customers(conn)
    load_orders(conn)
    load_order_items(conn)

def load_customers(conn: Connection) -> None:
    df = pd.read_csv(Path(DATA_DIR) / "customers.csv")
    df.to_sql("customers", conn, if_exists="replace", index=False)
    logger.info(f"Loaded {len(df)} customers")

def load_orders(conn: Connection) -> None:
    df = pd.read_csv(Path(DATA_DIR) / "orders.csv")
    df["total_amount"] = df["total_amount"].fillna(0.0)
    df.to_sql("orders", conn, if_exists="replace", index=False)
    logger.info(f"Loaded {len(df)} orders")

def load_order_items(conn: Connection) -> None:
    df = pd.read_csv(Path(DATA_DIR) / "order_items.csv")
    negative_qty = df[df["quantity"] < 0]
    missing_orders = df["order_id"].isna().sum()

    if not negative_qty.empty:
        logger.warning(
            f"Found {len(negative_qty)} rows with negative quantities"
        )
    if missing_orders > 0:
        logger.warning(
        f"Found {missing_orders} order items with missing order_id"
        )

    df.to_sql("order_items", conn, if_exists="replace", index=False)
    logger.info(f"Loaded {len(df)} order_items")