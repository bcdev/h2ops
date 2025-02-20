# import pathlib
# import shutil
# import subprocess
# import tempfile
#
# import yaml
# import pytest
# from cookiecutter.main import cookiecutter
#
#
# @pytest.fixture
# def temp_dir():
#     d = tempfile.mkdtemp()
#     yield d
#     shutil.rmtree(d)
#
#
# @pytest.mark.parametrize(
#     "extra_context, expected_folder_name, expect_dag_factory, expect_minio, "
#     "expect_examples",
#     [
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "yes",
#                 "show_airflow_dag_examples": "no",
#                 "use_dag_factory": "yes",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             True,
#             True,
#             False,
#         ),
#         # Case: no minio, but dag factory enabled
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "no",
#                 "show_airflow_dag_examples": "yes",
#                 "use_dag_factory": "yes",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             True,
#             False,
#             True,
#         ),
#         # Case: minio enabled, dag factory disabled
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "yes",
#                 "show_airflow_dag_examples": "no",
#                 "use_dag_factory": "no",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             False,
#             True,
#             False,
#         ),
#         # Case: neither minio nor dag factory enabled
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "no",
#                 "show_airflow_dag_examples": "yes",
#                 "use_dag_factory": "no",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             False,
#             False,
#             True,
#         ),
#     ],
# )
# def test_generated_project(
#     temp_dir,
#     extra_context,
#     expected_folder_name,
#     expect_dag_factory,
#     expect_minio,
#     expect_examples,
# ):
#     template_dir = str(pathlib.Path(__file__).parent.parent)
#
#     cookiecutter(
#         template=template_dir,
#         no_input=True,
#         extra_context=extra_context,
#         output_dir=temp_dir,
#     )
#
#     project_dir = pathlib.Path(temp_dir) / expected_folder_name
#     assert project_dir.exists(), "The generated project directory does not exist."
#
#     # Verify that README.md exists and includes the project name
#     readme_path = project_dir / "README.md"
#     assert readme_path.exists(), "README.md was not found in the generated project."
#     content = readme_path.read_text(encoding="utf-8")
#     assert (
#         extra_context["project_name"] in content
#     ), "The project name was not rendered in the README."
#
#     # Verify environment.yml
#     environment_path = project_dir / "environment.yml"
#     assert (
#         environment_path.exists()
#     ), "environment.yml was not found in the generated project."
#     content = environment_path.read_text(encoding="utf-8")
#
#     assert (
#         expected_folder_name in content
#     ), "The environment.yml does not contain the project name as the env name"
#
#     # Check for the examples folder
#     dag_factory_examples_path = project_dir / "dags" / "examples" / "dag_factory"
#     manual_dags_examples_path = project_dir / "dags" / "examples" / "manual-dags"
#     if expect_examples:
#         if expect_dag_factory:
#             assert (
#                 dag_factory_examples_path.exists()
#             ), "dag_factory folder was not found in the generated project."
#             assert (
#                 "dag_factory" in content
#             ), "The environment.yml does not contain dag_factory"
#         else:
#             assert (
#                 not manual_dags_examples_path.exists()
#             ), "manual_dags folder was not found in the generated project."
#             assert (
#                 "dag_factory" not in content
#             ), "The environment.yml contains dag_factory"
#     else:
#         assert (
#             not dag_factory_examples_path.exists()
#         ), "dag_factory folder  should not exist in the generated project."
#         assert (
#             not manual_dags_examples_path.exists()
#         ), "manual_dags folder should not exist in the generated project."
#
#     # For minio, check for minio-specific configuration based on expect_minio flag
#     docker_compose_path = project_dir / "docker-compose.yml"
#     content = docker_compose_path.read_text(encoding="utf-8")
#     if expect_minio:
#         assert (
#             "MINIO_ROOT_USER" in content
#         ), "The docker-compose.yml does not contain MINIO_ROOT_USER when minio is expected."
#         assert (
#             "MINIO_ROOT_PASSWORD" in content
#         ), "The docker-compose.yml does not contain MINIO_ROOT_PASSWORD when minio is expected."
#
#         assert (
#             "AWS_ACCESS_KEY_ID" in content
#         ), "The docker-compose.yml does not contain AWS_ACCESS_KEY_ID"
#         assert (
#             "AWS_SECRET_ACCESS_KEY" in content
#         ), "The docker-compose.yml does not contain AWS_SECRET_ACCESS_KEY"
#         assert (
#             "MLFLOW_S3_ENDPOINT_URL" in content
#         ), "The docker-compose.yml does not contain MLFLOW_S3_ENDPOINT_URL"
#
#         expected_default_artifact = "--default-artifact-root s3://${MLFLOW_BUCKET_NAME} --artifacts-destination s3://${MLFLOW_BUCKET_NAME}"
#
#         assert (
#             expected_default_artifact in content
#         ), "The docker-compose.yml does not contain default-artifact root as s3"
#         assert (
#             "- ./${DEFAULT_ARTIFACT_ROOT}:/${DEFAULT_ARTIFACT_ROOT}" not in content
#         ), "The docker-compose.yml still contains local artifacts dir."
#     else:
#         assert (
#             "MINIO_ROOT_USER" not in content
#         ), "The docker-compose.yml should not contain MINIO_ROOT_USER when minio is not expected."
#         assert (
#             "MINIO_ROOT_PASSWORD" not in content
#         ), "The docker-compose.yml should not contain MINIO_ROOT_PASSWORD when minio is not expected."
#
#         assert (
#             "AWS_ACCESS_KEY_ID" not in content
#         ), "The docker-compose.yml does not contain AWS_ACCESS_KEY_ID"
#         assert (
#             "AWS_SECRET_ACCESS_KEY" not in content
#         ), "The docker-compose.yml does not contain AWS_SECRET_ACCESS_KEY"
#         assert (
#             "MLFLOW_S3_ENDPOINT_URL" not in content
#         ), "The docker-compose.yml does not contain MLFLOW_S3_ENDPOINT_URL"
#
#         expected_default_artifact = "--default-artifact-root s3://${MLFLOW_BUCKET_NAME} --artifacts-destination s3://${MLFLOW_BUCKET_NAME}"
#         assert expected_default_artifact not in content, (
#             "The docker-compose.yml does not contain default-artifact root as " "s3"
#         )
#         assert (
#             "- ./${DEFAULT_ARTIFACT_ROOT}:/${DEFAULT_ARTIFACT_ROOT}" in content
#         ), "The docker-compose.yml still contains local artifacts dir."
#
#
# @pytest.mark.parametrize(
#     "extra_context, expected_folder_name, expect_dag_factory, expect_examples",
#     [
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "yes",
#                 "show_airflow_dag_examples": "no",
#                 "use_dag_factory": "yes",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             True,
#             False,
#         ),
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "no",
#                 "show_airflow_dag_examples": "yes",
#                 "use_dag_factory": "no",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             False,
#             True,
#         ),
#     ],
# )
# def test_full_directory_tree(
#     temp_dir, extra_context, expected_folder_name, expect_dag_factory, expect_examples
# ):
#     template_dir = str(pathlib.Path(__file__).parent.parent)
#
#     cookiecutter(
#         template=template_dir,
#         no_input=True,
#         extra_context=extra_context,
#         output_dir=temp_dir,
#     )
#
#     project_dir = pathlib.Path(temp_dir) / expected_folder_name
#
#     expected_files = {
#         "README.md",
#         "docker-compose.yml",
#         "environment.yml",
#         "my_package/__init__.py",
#         "dockerfiles/airflow/Dockerfile",
#         "dockerfiles/mlflow/Dockerfile",
#         "dockerfiles/mlflow/requirements.txt",
#         "notebooks/examples/mlflow_2_steps.ipynb",
#         "notebooks/examples/mlflow_docker_inference.ipynb",
#         "notebooks/examples/mlflow_inference.ipynb",
#         "my_package/preprocess/examples/__init__.py",
#         "my_package/preprocess/examples/mnist_run.py",
#         "my_package/preprocess/__init__.py",
#         "my_package/postprocess/example_postprocess.py",
#         "my_package/postprocess/example_postprocess.py",
#         "my_package/train/examples/mnist_run.py",
#         "my_package/train/examples/mnist_autolog_run.py",
#         "my_package/train/examples/example_bash.py",
#         "my_package/train/examples/example_postprocess.py",
#         "my_package/train/examples/__init__.py",
#         "my_package/train/__init__.py",
#         "my_package/__init__.py",
#         "my_package/utils/utils.py",
#         ".gitignore",
#         "local_inference.py",
#         "mlops-run.sh",
#     }
#
#     if expect_examples:
#         if expect_dag_factory:
#             expected_files.add("dags/examples/dag_factory/generate_dags.py")
#             expected_files.add("dags/examples/dag_factory/pipeline-config.yml")
#         else:
#             expected_files.add("dags/examples/manual_dags/example_dag.py")
#             expected_files.add(
#                 "dags/examples/manual_dags/example_ml_mnist_autolog_dag.py"
#             )
#             expected_files.add("dags/examples/manual_dags/example_ml_mnist_dag.py")
#             expected_files.add(
#                 "dags/examples/manual_dags/example_ml_single_step_dag.py"
#             )
#
#     actual_files = {
#         str(path.relative_to(project_dir))
#         for path in project_dir.glob("**/*")
#         if path.is_file()
#     }
#     print(actual_files)
#     for expected in expected_files:
#         assert (
#             expected in actual_files
#         ), f"Expected file '{expected}' not found in the project tree."
#
#
# @pytest.mark.parametrize(
#     "extra_context, expected_folder_name, expect_dag_factory",
#     [
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "yes",
#                 "show_airflow_dag_examples": "no",
#                 "use_dag_factory": "yes",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             True,
#         ),
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "no",
#                 "show_airflow_dag_examples": "no",
#                 "use_dag_factory": "no",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             },
#             "my_ml_project",
#             False,
#         ),
#     ],
# )
# def test_post_gen_hook_executed(
#     temp_dir, extra_context, expected_folder_name, expect_dag_factory
# ):
#     template_dir = str(pathlib.Path(__file__).parent.parent)
#     cookiecutter(
#         template=template_dir,
#         no_input=True,
#         extra_context=extra_context,
#         output_dir=temp_dir,
#     )
#
#     project_dir = pathlib.Path(temp_dir) / expected_folder_name
#
#     env_file = project_dir / "environment.yml"
#     assert env_file.exists(), "environment.yml file is missing."
#
#     with env_file.open("r", encoding="utf-8") as f:
#         env_data = yaml.safe_load(f)
#
#     dependencies = env_data.get("dependencies", [])
#     print(dependencies, expect_dag_factory)
#
#     if expect_dag_factory:
#         assert {
#             "pip": ["dag_factory"]
#         } in dependencies, (
#             "dag_factory should be in dependencies when use_dag_factory is 'yes'."
#         )
#     else:
#         assert {
#             "pip": ["dag_factory"]
#         } not in dependencies, (
#             "dag_factory should not be in dependencies when use_dag_factory is 'no'."
#         )
#
#
# @pytest.mark.parametrize(
#     "extra_context",
#     [
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "yes",
#                 "show_airflow_dag_examples": "no",
#                 "use_dag_factory": "yes",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             }
#         ),
#         (
#             {
#                 "project_name": "My ML Project",
#                 "use_minio": "no",
#                 "show_airflow_dag_examples": "no",
#                 "use_dag_factory": "no",
#                 "folder_name": "my_ml_project",
#                 "package_name": "my_package",
#             }
#         ),
#     ],
# )
# def test_ruff_linting(temp_dir, extra_context):
#     template_dir = str(pathlib.Path(__file__).parent.parent)
#
#     cookiecutter(
#         template=template_dir,
#         no_input=True,
#         extra_context=extra_context,
#         output_dir=temp_dir,
#     )
#
#     project_dir = pathlib.Path(temp_dir) / "my_ml_project"
#     result = subprocess.run(
#         ["ruff", "check", "."],
#         cwd=str(project_dir),
#         capture_output=True,
#         text=True,
#     )
#     assert result.returncode == 0, (
#         "Ruff linting failed.\n"
#         f"stdout:\n{result.stdout}\n"
#         f"stderr:\n{result.stderr}"
#     )

import pathlib
import shutil
import subprocess
import tempfile
from itertools import product
from typing import Dict, Any, Set

import yaml
import pytest
from cookiecutter.main import cookiecutter

BASE_CONTEXT = {
    "project_name": "My ml project",
    "project_description": "Some description",
    "author_name": "John Doe",
    "author_email": "john@doe.com",
    "folder_name": "my_ml_project",
    "package_name": "my_package",
}

CORE_FILES = {
    "mlops-run.sh",
    "docker-compose.yml",
    "README.md",
    ".env",
    ".gitignore",
    "MLOps.md",
    "environment.yml",
    "scripts/example_script",
    "dags/README.md",
    "dockerfiles/README.md",
    "dockerfiles/mlflow/requirements.txt",
    "dockerfiles/mlflow/Dockerfile",
    "dockerfiles/airflow/Dockerfile",
    "notebooks/README.md",
    "notebooks/examples/mlflow_direct_inference.ipynb",
    "notebooks/examples/mlflow_local_deploy_inference.ipynb",
    "notebooks/examples/mlfow_introduction.ipynb",
    "data/add_your_data_here",
    "my_package/README.md",
    "my_package/__init__.py",
    "my_package/dataloader/change_me_data.py",
    "my_package/dataloader/__init__.py",
    "my_package/utils/utils.py",
    "my_package/utils/__init__.py",
    "my_package/model_pipeline/change_me_model_pipeline.py",
    "my_package/model_pipeline/__init__.py",
    "my_package/models/change_me_model.py",
    "my_package/models/__init__.py",
    "my_package/train/change_me_train.py",
    "my_package/train/__init__.py",
    "my_package/postprocess/change_me_postprocess.py",
    "my_package/postprocess/__init__.py",
    "my_package/preprocess/change_me_preprocess.py",
    "my_package/preprocess/__init__.py",
}


DAG_FACTORY_FILES = [
    "dags/change_me_config.yml",
    "dags/change_me_generate_dags.py",
]

EXAMPLE_DAG_FACTORY_FILES = [
    "dags/example_config.yml",
]

MANUAL_DAGS_FILES = [
    "dags/change_me_dag.py",
]

EXAMPLE_MANUAL_DAGS_FILES = [
    "dags/example_dag.py",
]

EXAMPLE_ML_PACKAGE_FILES = [
    "my_package/dataloader/example_data.py",
    "my_package/model_pipeline/example_model_pipeline.py",
    "my_package/postprocess/example_postprocess.py",
    "my_package/preprocess/example_preprocess.py",
    "my_package/train/example_train.py",
    "my_package/models/example_model.py",
]

EXAMPLE_ML_PACAKGE_WITHOUT_MINIO = [
    "my_package/dataloader/example_data_without_minio.py",
    "my_package/preprocess/example_preprocess_without_minio.py",
    "my_package/train/example_train_without_minio.py",
]

# Possible choices for each parameter to create combinations of them.
PARAMETER_OPTIONS = {
    "use_minio": ["yes", "no"],
    "show_airflow_dag_examples": ["yes", "no"],
    "use_dag_factory": ["yes", "no"],
    "show_ml_package_examples": ["yes", "no"],
}


def generate_test_cases():
    param_names = list(PARAMETER_OPTIONS.keys())
    param_values = list(PARAMETER_OPTIONS.values())

    test_cases = []

    for values in product(*param_values):
        context = BASE_CONTEXT.copy()
        context.update(dict(zip(param_names, values)))

        expects = {
            "dag_factory": context["use_dag_factory"] == "yes",
            "minio": context["use_minio"] == "yes",
            "dag_examples": context["show_airflow_dag_examples"] == "yes",
            "ml_examples": context["show_ml_package_examples"] == "yes",
        }

        test_cases.append({"context": context, "expects": expects})

    return test_cases


TEST_CASES = generate_test_cases()


@pytest.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def generate_project(temp_dir: str, context: Dict[str, Any]) -> pathlib.Path:
    template_dir = str(pathlib.Path(__file__).parent.parent)
    cookiecutter(
        template=template_dir,
        no_input=True,
        extra_context=context,
        output_dir=temp_dir,
    )
    return pathlib.Path(temp_dir) / context["folder_name"]


def get_all_files(directory: pathlib.Path) -> Set[str]:
    return {
        str(path.relative_to(directory))
        for path in directory.glob("**/*")
        if path.is_file()
    }


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_project_generation(temp_dir: str, test_case: Dict[str, Any]):
    print(test_case)
    context = test_case["context"]
    expects = test_case["expects"]
    project_dir = generate_project(temp_dir, context)

    assert project_dir.exists(), "Project directory not created"

    # Verify README content
    readme_content = (project_dir / "README.md").read_text(encoding="utf-8")
    print(readme_content)
    assert context["project_name"] in readme_content, "Project name not in " "README"

    # Check environment.yml content
    env_path = project_dir / "environment.yml"
    with env_path.open(encoding="utf-8") as f:
        env_data = yaml.safe_load(f)
        assert context["folder_name"] in env_data["name"], "Wrong environment name"
        if expects["dag_factory"]:
            assert {"pip": ["dag_factory"]} in env_data["dependencies"]
        else:
            assert {"pip": ["dag_factory"]} not in env_data["dependencies"]

    # Check docker-compose.yml for Minio configuration
    docker_compose = (project_dir / "docker-compose.yml").read_text()
    minio_configs = [
        "MINIO_ROOT_USER",
        "MINIO_ROOT_PASSWORD",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "MLFLOW_S3_ENDPOINT_URL",
    ]
    artifact_config = "--default-artifact-root s3://${MLFLOW_BUCKET_NAME} --artifacts-destination s3://${MLFLOW_BUCKET_NAME}"
    local_artifacts = "- ./${DEFAULT_ARTIFACT_ROOT}:/${DEFAULT_ARTIFACT_ROOT}"

    for config in minio_configs:
        assert (config in docker_compose) == expects["minio"]
    if expects["minio"]:
        assert artifact_config in docker_compose
        assert local_artifacts not in docker_compose
    else:
        assert artifact_config not in docker_compose
        assert local_artifacts in docker_compose

    # Verify file structure
    actual_files = get_all_files(project_dir)
    core_files_copy = CORE_FILES.copy()
    print("corefile", core_files_copy)

    if expects["dag_examples"]:
        if expects["dag_factory"]:
            core_files_copy.update(EXAMPLE_DAG_FACTORY_FILES)
        else:
            core_files_copy.update(EXAMPLE_MANUAL_DAGS_FILES)

    if expects["ml_examples"]:
        if expects["minio"]:
            core_files_copy.update(EXAMPLE_ML_PACKAGE_FILES)
        else:
            core_files_copy.update(EXAMPLE_ML_PACAKGE_WITHOUT_MINIO)

    if expects["dag_factory"]:
        core_files_copy.update(DAG_FACTORY_FILES)
    else:
        core_files_copy.update(MANUAL_DAGS_FILES)

    print("expects[ml_examples]", expects["ml_examples"])
    print("corefile", core_files_copy)
    print("actualfile", actual_files)
    # Check core files
    for file in core_files_copy:
        assert file in actual_files, f"Missing core file: {file}"

    # Check DAG-related files
    if expects["dag_examples"]:
        if expects["dag_factory"]:
            for file in DAG_FACTORY_FILES:
                assert file in actual_files, f"Missing DAG factory file: {file}"
            for file in MANUAL_DAGS_FILES:
                assert file not in actual_files, f"Unexpected manual DAG file: {file}"
        else:
            for file in MANUAL_DAGS_FILES:
                assert file in actual_files, f"Missing manual DAG file: {file}"
            for file in DAG_FACTORY_FILES:
                assert file not in actual_files, f"Unexpected DAG factory file: {file}"


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_ruff_linting(temp_dir: str, test_case: Dict[str, Any]):
    project_dir = generate_project(temp_dir, test_case["context"])
    result = subprocess.run(
        ["ruff", "check", "."],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
    )
    assert (
        result.returncode == 0
    ), f"Linting failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
