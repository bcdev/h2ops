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
    show_ml_package_examples = (
        "{{ cookiecutter.show_ml_package_examples }}".strip().lower()
    )
    use_minio = "{{ cookiecutter.use_minio }}".strip().lower()

    print("minio", use_minio)

    if use_dag_factory != "yes":
        to_be_deleted_deps.append("pip")
        to_be_deleted_deps.append({"pip": ["dag_factory"]})

    env_file = pathlib.Path().cwd() / "environment.yml"
    modify_environment_yaml(env_file, to_be_deleted_deps)

    if use_minio == "yes":
        remove_file(
            os.path.join(
                os.getcwd(),
                "{{ cookiecutter.package_name }}",
                "dataloader/example_data_without_minio.py",
            )
        )
        remove_file(
            os.path.join(
                os.getcwd(),
                "{{ cookiecutter.package_name }}",
                "preprocess/example_preprocess_without_minio.py",
            )
        )
        remove_file(
            os.path.join(
                os.getcwd(),
                "{{ cookiecutter.package_name }}",
                "train/example_train_without_minio.py",
            )
        )
    else:
        remove_file(
            os.path.join(
                os.getcwd(),
                "{{ cookiecutter.package_name }}",
                "dataloader/example_data.py",
            )
        )
        remove_file(
            os.path.join(
                os.getcwd(),
                "{{ cookiecutter.package_name }}",
                "preprocess/example_preprocess.py",
            )
        )
        remove_file(
            os.path.join(
                os.getcwd(),
                "{{ cookiecutter.package_name }}",
                "train/example_train.py",
            )
        )

    if show_airflow_examples != "yes":
        remove_file(os.path.join(os.getcwd(), "dags/example_config.yml"))
        remove_file(os.path.join(os.getcwd(), "dags/example_dag.py"))

    if use_dag_factory == "yes":
        remove_file(os.path.join(os.getcwd(), "dags/change_me_dag.py"))
        remove_file(os.path.join(os.getcwd(), "dags/example_dag.py"))
    else:
        remove_file(os.path.join(os.getcwd(), "dags/change_me_config.yml"))
        remove_file(os.path.join(os.getcwd(), "dags/change_me_generate_dags.py"))
        remove_file(os.path.join(os.getcwd(), "dags/example_config.yml"))

    if show_ml_package_examples != "yes":
        file_paths_config = [
            "dataloader/example_data.py",
            "dataloader/example_data_without_minio.py",
            "model_pipeline/example_model_pipeline.py",
            "models/example_model.py",
            "postprocess/example_postprocess.py",
            "preprocess/example_preprocess.py",
            "preprocess/example_preprocess_without_minio.py",
            "train/example_train.py",
            "train/example_train_without_minio.py",
        ]

        for file_path_relative in file_paths_config:
            full_file_path = os.path.join(
                os.getcwd(), "{{ cookiecutter.package_name }}", file_path_relative
            )
            remove_file(full_file_path)


if __name__ == "__main__":
    sys.exit(main())
