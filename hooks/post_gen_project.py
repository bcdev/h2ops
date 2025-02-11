import os
import sys
import yaml
import shutil


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


def modify_environment_yaml(env_file: str, to_be_deleted_deps: list[str]):
    """Remove unwanted libraries from environment.yml based on user input."""
    if not os.path.exists(env_file):
        print(f"{env_file} not found.")
        return
    try:
        with open(env_file, "r") as f:
            env_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading {env_file}: {e}")
        return

    dependencies = env_data.get("dependencies", [])
    new_dependencies = []

    for dep in dependencies:
        for to_be_deleted_dep in to_be_deleted_deps:
            if dep == to_be_deleted_dep:
                continue
        new_dependencies.append(dep)
    env_data["dependencies"] = new_dependencies

    try:
        with open(env_file, "w") as f:
            yaml.dump(env_data, f)
        print(f"Updated {env_file}")
    except Exception as e:
        print(f"Error writing {env_file}: {e}")


def main():
    to_be_deleted_deps = []
    use_dag_factory = "{{ cookiecutter.use_dag_factory }}".strip().lower()

    if use_dag_factory:
        to_be_deleted_deps.append("dag_factory")

    env_file = os.path.join(os.getcwd(), "environment.yml")
    modify_environment_yaml(env_file, to_be_deleted_deps)

    if use_dag_factory != "yes":
        dir_to_remove = os.path.join(os.getcwd(), "dags/examples/dag_factory")
        remove_directory(dir_to_remove)
    else:
        dir_to_remove = os.path.join(os.getcwd(), "dags/examples/manual_dags")
        remove_directory(dir_to_remove)


if __name__ == "__main__":
    sys.exit(main())
