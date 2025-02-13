import os
import pathlib
import sys
import shutil
import ruamel.yaml
from ruamel.yaml import CommentedMap


def remove_file(file_path):
    """Remove a file if it exists."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Removed file: {file_path}")
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")


def remove_directory(dir_path):
    """Remove a directory and all its contents if it exists."""
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path)
            print(f"Removed directory: {dir_path}")
        except Exception as e:
            print(f"Error removing directory {dir_path}: {e}")


def modify_environment_yaml(env_file: pathlib.Path, to_be_deleted_deps: list[str]):
    """Remove unwanted libraries from environment.yml based on user input."""
    if not pathlib.Path.exists(env_file):
        print(f"{str(env_file)} not found.")
        return

    yaml = ruamel.yaml.YAML()
    yaml.indent(offset=2)

    try:
        env_data = yaml.load(env_file)
    except Exception as e:
        print(f"Error reading {str(env_file)}: {e}")
        return

    dependencies = env_data.get("dependencies", [])

    for i in range(len(dependencies) - 1, -1, -1):
        dep = dependencies[i]
        if (
            isinstance(dep, CommentedMap) and dict(dep) in to_be_deleted_deps
        ) or dep in to_be_deleted_deps:
            dependencies.remove(dep)

    try:
        with open(env_file, "w") as f:
            yaml.dump(env_data, f)
        print(f"Updated {env_file}")
    except Exception as e:
        print(f"Error writing {env_file}: {e}")


def main():
    to_be_deleted_deps = []
    use_dag_factory = "{{ cookiecutter.use_dag_factory }}".strip().lower()
    show_airflow_examples = (
        "{{ cookiecutter.show_airflow_dag_examples }}".strip().lower()
    )

    if use_dag_factory != "yes":
        to_be_deleted_deps.append("pip")
        to_be_deleted_deps.append({"pip": ["dag_factory"]})

    env_file = pathlib.Path().cwd() / "environment.yml"
    modify_environment_yaml(env_file, to_be_deleted_deps)

    # TODO: Dag factory flag should now show templates instead of examples
    # if use_dag_factory != "yes":
    #     dir_to_remove = os.path.join(os.getcwd(), "dags/examples/dag_factory")
    #     remove_directory(dir_to_remove)
    # else:
    #     dir_to_remove = os.path.join(os.getcwd(), "dags/examples/manual_dags")
    #     remove_directory(dir_to_remove)

    if show_airflow_examples != "yes":
        dir_to_remove = os.path.join(os.getcwd(), "dags/examples/dag_factory")
        remove_directory(dir_to_remove)
        dir_to_remove = os.path.join(os.getcwd(), "dags/examples/manual_dags")
        remove_directory(dir_to_remove)


if __name__ == "__main__":
    sys.exit(main())
