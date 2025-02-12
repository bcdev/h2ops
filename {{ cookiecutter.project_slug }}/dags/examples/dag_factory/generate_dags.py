from pathlib import Path
from airflow import DAG
import dagfactory

BASE_DIR = Path(__file__).resolve().parent
config_file = BASE_DIR / "pipeline-config.yml"
print(f"Loading config file from: {config_file}")

if not config_file.exists():
    raise FileNotFoundError(f"Config file not found: {config_file}")

dag_factory = dagfactory.DagFactory(str(config_file))

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())
