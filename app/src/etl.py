import os
import time
import pandas as pd
from sqlalchemy import create_engine, text

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "demo")
DB_USER = os.getenv("POSTGRES_USER", "demo")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "demo123")
TABLE = os.getenv("APP_DB_TABLE", "demo_data")

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_data", "data.csv")


def wait_for_db(engine, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            time.sleep(2)
    return False


def main():
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        future=True,
    )
    if not wait_for_db(engine):
        print("[ERROR] Postgres is not reachable")
        return 1

    df = pd.read_csv(CSV_PATH)
    # Simple transform
    df["amount"] = df["amount"].astype(float)
    df["name"] = df["name"].astype(str)

    with engine.begin() as conn:
        conn.execute(
            text(
                f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id SERIAL PRIMARY KEY,
                name TEXT,
                amount NUMERIC,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """
            )
        )
        df[["name", "amount"]].to_sql(TABLE, con=conn, if_exists="append", index=False)

    print(f"[OK] Loaded {len(df)} rows into {TABLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
