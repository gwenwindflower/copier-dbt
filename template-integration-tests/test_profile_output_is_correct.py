import pytest
from typing import Dict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


@pytest.fixture
def duckdb_answers() -> Dict[str, str]:
    return {
        "project_name": "Lothlorien Enterprises",
        "data_warehouse": "duckdb",
        "username": "galadriel",
        "database": "mallorn",
        "schema": "flets",
        "duckdb_file_path": "./lothlorien.db",
    }


@pytest.fixture
def snowflake_answers() -> Dict[str, str]:
    return {
        "project_name": "Aragorn Inc",
        "data_warehouse": "snowflake",
        "username": "Strider",
        "warehouse": "Narsil",
        "role": "King",
        "database": "gondor",
        "schema": "minas_tirith",
    }

@pytest.fixture
def bigquery_answers() -> Dict[str, str]:
    return {
        "project_name": "Legoalas Corp",
        "data_warehouse": "bigquery",
        "username": "legolas",
        "database": "mirkwood",
        "schema": "archers",
    }

