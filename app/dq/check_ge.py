# Minimal GE placeholder: query data from Postgres and run trivial expectations.
import os
import pandas as pd
from sqlalchemy import create_engine

try:
    from great_expectations.dataset import PandasDataset
except Exception as e:
    print("[WARN] Great Expectations not available, skipping placeholder:", e)
    raise SystemExit(0)

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "demo")
DB_USER = os.getenv("POSTGRES_USER", "demo")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "demo123")
TABLE = os.getenv("APP_DB_TABLE", "demo_data")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

df = pd.read_sql(f"SELECT * FROM {TABLE} LIMIT 1000", engine)
dataset = PandasDataset(df)

result1 = dataset.expect_column_to_exist("name")
result2 = dataset.expect_table_row_count_to_be_between(min_value=1)

ok = result1["success"] and result2["success"]
print("GE results:", {"exist_name": result1["success"], "rowcount_ok": result2["success"]})
raise SystemExit(0 if ok else 1)
