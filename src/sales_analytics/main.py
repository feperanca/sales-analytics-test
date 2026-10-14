import argparse
from pathlib import Path

from .db import create_in_memory_db
from .loaders import load_all_data
from .analytics import generate_reports
from .config import DEFAULT_REPORTS_DIR


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_REPORTS_DIR),
        help="Directory where reports will be generated"
    )

    parser.add_argument(
        "--from-date",
        help="Filter start date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--to-date",
        help="Filter end date (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    conn = create_in_memory_db()

    load_all_data(conn)

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id)"
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date)"
    )

    generate_reports(
        conn,
        output_dir=Path(args.output_dir),
        from_date=args.from_date,
        to_date=args.to_date
    )


if __name__ == "__main__":
    main()