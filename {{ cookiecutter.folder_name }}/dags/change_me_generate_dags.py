from pathlib import Path
from airflow import DAG  # noqa
import dagfactory

#################################################
# Note: Please update the file name of the config file below (FILENAME) after
# you have renamed the config file.
# Then, please delete this comment block.
#################################################
{% if cookiecutter.show_examples == "yes" %}
FILENAME = "example_config.yml"
{% else %}
FILENAME = "change_me_config.yml"
{% endif %}

BASE_DIR = Path(__file__).resolve().parent
config_file = BASE_DIR / FILENAME
print(f"Loading config file from: {config_file}")

if not config_file.exists():
    raise FileNotFoundError(f"Config file not found: {config_file}")

dag_factory = dagfactory.DagFactory(str(config_file))

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())
