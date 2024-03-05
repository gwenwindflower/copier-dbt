import os
import shutil
from pathlib import Path
from typing import Dict

import copier
import yaml
from deepdiff import DeepDiff

PROJECT_ROOT = Path(__file__).parent.parent
TEST_EXPECT = PROJECT_ROOT / "template-integration-tests" / "test-expectations"
TEST_BUILD_DIR = PROJECT_ROOT / "template-integration-tests" / "test-build"


warehouse_answers: Dict[str, Dict[str, str]] = {
    "duckdb": {
        "project_name": "Lothlorien Enterprises",
        "data_warehouse": "duckdb",
        "username": "galadriel",
        "database": "mallorn",
        "schema": "flets",
        "duckdb_file_path": "./lothlorien.db",
    },
    "snowflake": {
        "project_name": "Aragorn Inc.",
        "account_id": "minas_tirith.us-east-1",
        "data_warehouse": "snowflake",
        "username": "Strider",
        "warehouse": "Narsil",
        "role": "King",
        "database": "gondor",
        "schema": "rangers",
    },
    "bigquery": {
        "project_name": "Legoalas Corp",
        "data_warehouse": "bigquery",
        "username": "legolas",
        "database": "mirkwood",
        "schema": "archers",
    },
}


def _check_profiles(warehouse):
    data = warehouse_answers[warehouse]

    copier.run_copy(
        str(PROJECT_ROOT),
        str(TEST_BUILD_DIR / warehouse),
        data=data,
        defaults=True,
        unsafe=True,
        vcs_ref="HEAD",
    )

    with open(TEST_EXPECT / f"{warehouse}_profile.yml", "r") as f:
        expected_output = yaml.safe_load(f)
    with open(TEST_BUILD_DIR / warehouse / "profiles.yml", "r") as f:
        actual_output = yaml.safe_load(f)

    diff = DeepDiff(expected_output, actual_output)
    assert diff == {}, f"Differences: {diff}"


def test_profile_output_is_correct():
    if os.path.exists(TEST_BUILD_DIR):
        shutil.rmtree(TEST_BUILD_DIR)

    for warehouse in warehouse_answers:
        _check_profiles(warehouse)
