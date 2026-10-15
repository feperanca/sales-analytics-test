import argparse
from datetime import datetime
from pathlib import Path

from .db import create_in_memory_db
from .loaders import load_all_data
from .analytics import generate_reports
from .config import DEFAULT_REPORTS_DIR

# validate dates format YYYY-MM-DD
def valid_date(date_string: str) -> str:
    """Validate if the received string is a real date in YYYY-MM-DD format."""
    try:
        # try to parse the date string to check if it's valid
        datetime.strptime(date_string, "%Y-%m-%d")
        return date_string  # if works, return the string as is
    except ValueError:
        # raise error if it's not a valid date or format is incorrect
        raise argparse.ArgumentTypeError(
            # This message will appear directly in the user's terminal
            f"Invalid date: '{date_string}'. Correct format: YYYY-MM-DD and date must be valid."
        )

def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_REPORTS_DIR),
        help="Directory where reports will be generated"
    )

    parser.add_argument(
        "--from-date",
        type=valid_date,
        help="Filter start date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--to-date",
        type=valid_date,
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