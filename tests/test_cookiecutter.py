import pathlib
import shutil
import tempfile

import yaml
import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


@pytest.mark.parametrize(
    "extra_context, expected_project_slug, expect_dag_factory, expect_minio",
    [
        (
            {
                "project_name": "My ML Project",
                "use_minio": "yes",
                "show_airflow_dag_examples": "false",
                "use_dag_factory": "yes",
            },
            "my_ml_project",
            True,
            True,
        ),
        # Case: no minio, but dag factory enabled
        (
            {
                "project_name": "My ML Project",
                "use_minio": "no",
                "show_airflow_dag_examples": "false",
                "use_dag_factory": "yes",
            },
            "my_ml_project",
            True,
            False,
        ),
        # Case: minio enabled, dag factory disabled
        (
            {
                "project_name": "My ML Project",
                "use_minio": "yes",
                "show_airflow_dag_examples": "false",
                "use_dag_factory": "no",
            },
            "my_ml_project",
            False,
            True,
        ),
        # Case: neither minio nor dag factory enabled
        (
            {
                "project_name": "My ML Project",
                "use_minio": "no",
                "show_airflow_dag_examples": "false",
                "use_dag_factory": "no",
            },
            "my_ml_project",
            False,
            False,
        ),
    ],
)
def test_generated_project(
    temp_dir, extra_context, expected_project_slug, expect_dag_factory, expect_minio
):
    template_dir = str(pathlib.Path(__file__).parent.parent)

    cookiecutter(
        template=template_dir,
        no_input=True,
        extra_context=extra_context,
        output_dir=temp_dir,
    )

    project_dir = pathlib.Path(temp_dir) / expected_project_slug
    assert project_dir.exists(), "The generated project directory does not exist."

    # Verify that README.md exists and includes the project name
    readme_path = project_dir / "README.md"
    assert readme_path.exists(), "README.md was not found in the generated project."
    content = readme_path.read_text(encoding="utf-8")
    assert (
        extra_context["project_name"] in content
    ), "The project name was not rendered in the README."

    # Check for the dag_factory examples folder
    if expect_dag_factory:
        dag_factory_examples_path = project_dir / "dags" / "examples" / "dag_factory"
        assert (
            dag_factory_examples_path.exists()
        ), "dag_factory folder was not found in the generated project."
    else:
        manual_dags_examples_path = project_dir / "dags" / "examples" / "manual-dags"
        assert (
            not manual_dags_examples_path.exists()
        ), "dag_factory folder should not exist in the generated project."

    # Verify environment.yml
    environment_path = project_dir / "environment.yml"
    assert (
        environment_path.exists()
    ), "environment.yml was not found in the generated project."
    content = environment_path.read_text(encoding="utf-8")
    assert "dag_factory" in content, "The environment.yml does not contain dag_factory"
    assert (
        expected_project_slug in content
    ), "The environment.yml does not contain the project name as the env name"

    # For minio, check for minio-specific configuration based on expect_minio flag
    docker_compose_path = project_dir / "docker-compose.yml"
    content = docker_compose_path.read_text(encoding="utf-8")
    if expect_minio:
        assert (
            "MINIO_ROOT_USER" in content
        ), "The docker-compose.yml does not contain MINIO_ROOT_USER when minio is expected."
        assert (
            "MINIO_ROOT_PASSWORD" in content
        ), "The docker-compose.yml does not contain MINIO_ROOT_PASSWORD when minio is expected."

        assert (
            "AWS_ACCESS_KEY_ID" in content
        ), "The docker-compose.yml does not contain AWS_ACCESS_KEY_ID"
        assert (
            "AWS_SECRET_ACCESS_KEY" in content
        ), "The docker-compose.yml does not contain AWS_SECRET_ACCESS_KEY"
        assert (
            "MLFLOW_S3_ENDPOINT_URL" in content
        ), "The docker-compose.yml does not contain MLFLOW_S3_ENDPOINT_URL"

        expected_default_artifact = "--default-artifact-root s3://${MLFLOW_BUCKET_NAME} --artifacts-destination s3://${MLFLOW_BUCKET_NAME}"

        assert (
            expected_default_artifact in content
        ), "The docker-compose.yml does not contain default-artifact root as s3"
        assert (
            "- ./${DEFAULT_ARTIFACT_ROOT}:/${DEFAULT_ARTIFACT_ROOT}" not in content
        ), "The docker-compose.yml still contains local artifacts dir."
    else:
        assert (
            "MINIO_ROOT_USER" not in content
        ), "The docker-compose.yml should not contain MINIO_ROOT_USER when minio is not expected."
        assert (
            "MINIO_ROOT_PASSWORD" not in content
        ), "The docker-compose.yml should not contain MINIO_ROOT_PASSWORD when minio is not expected."

        assert (
            "AWS_ACCESS_KEY_ID" not in content
        ), "The docker-compose.yml does not contain AWS_ACCESS_KEY_ID"
        assert (
            "AWS_SECRET_ACCESS_KEY" not in content
        ), "The docker-compose.yml does not contain AWS_SECRET_ACCESS_KEY"
        assert (
            "MLFLOW_S3_ENDPOINT_URL" not in content
        ), "The docker-compose.yml does not contain MLFLOW_S3_ENDPOINT_URL"

        expected_default_artifact = "--default-artifact-root s3://${MLFLOW_BUCKET_NAME} --artifacts-destination s3://${MLFLOW_BUCKET_NAME}"
        assert expected_default_artifact not in content, (
            "The docker-compose.yml does not contain default-artifact root as " "s3"
        )
        assert (
            "- ./${DEFAULT_ARTIFACT_ROOT}:/${DEFAULT_ARTIFACT_ROOT}" in content
        ), "The docker-compose.yml still contains local artifacts dir."


@pytest.mark.parametrize(
    "extra_context, expected_project_slug, expect_dag_factory",
    [
        (
            {
                "project_name": "My ML Project",
                "use_minio": "yes",
                "show_airflow_dag_examples": "false",
                "use_dag_factory": "yes",
            },
            "my_ml_project",
            True,
        ),
        (
            {
                "project_name": "My ML Project",
                "use_minio": "no",
                "show_airflow_dag_examples": "false",
                "use_dag_factory": "no",
            },
            "my_ml_project",
            False,
        ),
    ],
)
def test_full_directory_tree(
    temp_dir, extra_context, expected_project_slug, expect_dag_factory
):
    template_dir = str(pathlib.Path(__file__).parent.parent)

    cookiecutter(
        template=template_dir,
        no_input=True,
        extra_context=extra_context,
        output_dir=temp_dir,
    )

    project_dir = pathlib.Path(temp_dir) / expected_project_slug

    expected_files = {
        "README.md",
        "docker-compose.yml",
        "environment.yml",
        "src/__init__.py",
        "dockerfiles/airflow/Dockerfile",
        "dockerfiles/mlflow/Dockerfile",
        "dockerfiles/mlflow/requirements.txt",
        "notebooks/examples/mlflow_2_steps.ipynb",
        "notebooks/examples/mlflow_docker_inference.ipynb",
        "notebooks/examples/mlflow_inference.ipynb",
        "src/preprocess/examples/__init__.py",
        "src/preprocess/examples/mnist_run.py",
        "src/preprocess/__init__.py",
        "src/postprocess/run.py",
        "src/postprocess/run.py",
        "src/train/examples/mnist_run.py",
        "src/train/examples/mnist_autolog_run.py",
        "src/train/examples/example_bash.py",
        "src/train/examples/run.py",
        "src/train/examples/__init__.py",
        "src/train/__init__.py",
        "src/__init__.py",
        "src/utils/utils.py",
        ".gitignore",
        "local_inference.py",
        "mlops_run.sh",
    }

    if expect_dag_factory:
        expected_files.add("dags/examples/dag_factory/generate_dags.py")
        expected_files.add("dags/examples/dag_factory/pipeline-config.yml")
    else:
        expected_files.add("dags/examples/manual_dags/example_dag.py")
        expected_files.add("dags/examples/manual_dags/example_ml_mnist_autolog_dag.py")
        expected_files.add("dags/examples/manual_dags/example_ml_mnist_dag.py")
        expected_files.add("dags/examples/manual_dags/example_ml_single_step_dag.py")

    actual_files = {
        str(path.relative_to(project_dir))
        for path in project_dir.glob("**/*")
        if path.is_file()
    }
    for expected in expected_files:
        assert (
            expected in actual_files
        ), f"Expected file '{expected}' not found in the project tree."


def test_post_gen_hook_executed(temp_dir):
    template_dir = str(pathlib.Path(__file__).parent.parent)
    extra_context = {
        "project_name": "My ML Project",
        "use_minio": "yes",
        "show_airflow_dag_examples": "false",
        "use_dag_factory": "no",
    }
    cookiecutter(
        template=template_dir,
        no_input=True,
        extra_context=extra_context,
        output_dir=temp_dir,
    )

    project_dir = pathlib.Path(temp_dir) / "my_ml_project"

    env_file = project_dir / "environment.yml"
    assert env_file.exists(), "environment.yml file is missing."

    with env_file.open("r", encoding="utf-8") as f:
        env_data = yaml.safe_load(f)

    dependencies = env_data.get("dependencies", [])
    assert (
        "dag_factory" in dependencies
    ), "dag_factory should be in dependencies when use_dag_factory is 'yes'."

    dag_factory_dir = project_dir / "dags/examples/dag_factory"
    manual_dags_dir = project_dir / "dags/examples/manual_dags"

    if "{{ cookiecutter.use_dag_factory }}".strip().lower() == "yes":
        assert dag_factory_dir.exists(), "dag_factory directory should exist."
        assert not manual_dags_dir.exists(), "manual_dags directory should be removed."
    else:
        assert not dag_factory_dir.exists(), "dag_factory directory should be removed."
        assert manual_dags_dir.exists(), "manual_dags directory should exist."
