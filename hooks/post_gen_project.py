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


def modify_environment_yaml(env_file):
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

    include_lib_gusty = "{{ cookiecutter.include_lib_gusty }}".strip().lower()
    for dep in dependencies:
        if dep == "gusty" and include_lib_gusty != "yes":
            continue
        new_dependencies.append(dep)
    env_data["dependencies"] = new_dependencies

    try:
        with open(env_file, "w") as f:
            yaml.dump(env_data, f, default_flow_style=False)
        print(f"Updated {env_file}")
    except Exception as e:
        print(f"Error writing {env_file}: {e}")


def main():
    env_file = os.path.join(os.getcwd(), "environment.yml")
    modify_environment_yaml(env_file)


if __name__ == "__main__":
    sys.exit(main())
