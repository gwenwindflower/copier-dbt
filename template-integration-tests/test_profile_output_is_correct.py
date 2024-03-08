import os
import shutil
from pathlib import Path
from typing import Dict

import copier
import pytest
import yaml
from deepdiff import DeepDiff

PROJECT_ROOT: Path = Path(__file__).parent.parent
TEST_EXPECT: Path = PROJECT_ROOT / "template-integration-tests" / "test-expectations"
TEST_BUILD_DIR: Path = PROJECT_ROOT / "template-integration-tests" / "test-build"


warehouse_answers: Dict[str, Dict[str, str | bool | int]] = {
    "duckdb": {
        "project_name": "Galadriel's Mirrors and More",
        "data_warehouse": "duckdb",
        "username": "galadriel",
        "database": "lothlorien",
        "schema": "mallorn_trees",
        "duckdb_file_path": "./lothlorien.db",
    },
    "snowflake": {
        "project_name": "Aragorn Inc.",
        "account_id": "minas_tirith.us-east-1",
        "data_warehouse": "snowflake",
        "username": "Strider",
        "warehouse": "Narsil",
        "role": "King",
        "database": "dunedain",
        "schema": "rangers",
    },
    "bigquery": {
        "project_name": "Legoalas Corp",
        "data_warehouse": "bigquery",
        "username": "legolas",
        "database": "mirkwood",
        "schema": "archers",
    },
    "redshift": {
        "project_name": "Gimli Mining",
        "data_warehouse": "redshift",
        "iam_profile": "default",
        "region": "us-east-1",
        "cluster_id": "legolas-bff-4eva",
        "host": "gimli-mining.us-east-1.redshift.amazonaws.com",
        "port": 5439,
        "username": "gimli_son_of_gloin",
        "database": "ores",
        "schema": "mithril",
    },
    "postgres": {
        "project_name": "Shieldmaiden Security",
        "data_warehouse": "postgres",
        "host": "localhost",
        "port": 5432,
        "username": "eowyn",
        "password": "",
        "database": "rohan",
        "schema": "nazgul_threat_assessments",
    },
    "databricks": {
        "project_name": "Faramir Landscaping",
        "using_unity_catalog": True,
        "catalog": "tower_of_ecthelion",
        "data_warehouse": "databricks",
        "host": "faramir-landscaping",
        "http_path": "ithilien.databricks.com",
        "database": "eowyn",
        "schema": "bridal_gifts",
    },
}

test_data = [(warehouse, options) for warehouse, options in warehouse_answers.items()]


def check_profiles(warehouse: str, options: Dict) -> None:

    copier.run_copy(
        str(PROJECT_ROOT),
        str(TEST_BUILD_DIR / warehouse),
        data=options,
        defaults=True,
        unsafe=True,
        vcs_ref="HEAD",
    )

    with open(TEST_EXPECT / f"{warehouse}_profile.yml", "r") as f:
        expected_output: yaml.YAMLObject = yaml.safe_load(f)
    with open(TEST_BUILD_DIR / warehouse / "profiles.yml", "r") as f:
        actual_output: yaml.YAMLObject = yaml.safe_load(f)

    diff: DeepDiff = DeepDiff(expected_output, actual_output)
    assert diff == {}, f"Differences: {diff}"


@pytest.mark.parametrize("warehouse, options", test_data)
def test_profile_output_is_correct(warehouse, options, request):
    # Clean up the test build directory before the first iteration
    current_warehouse = request.node.callspec.params["warehouse"]
    if current_warehouse == test_data[0]:
        if os.path.exists(TEST_BUILD_DIR):
            shutil.rmtree(TEST_BUILD_DIR)

    check_profiles(warehouse, options)
