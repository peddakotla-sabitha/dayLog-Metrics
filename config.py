from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "data.json"
APP_NAME = "DayLog Metrics"
DATABASE_URL = "postgresql+psycopg2://postgres:191036@localhost:5432/daylog_metrics"