from __future__ import annotations

import json
from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--artifact-dir", action="store", required=True)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "device_artifact" not in metafunc.fixturenames:
        return

    artifact_dir = Path(metafunc.config.getoption("--artifact-dir"))
    files = sorted(artifact_dir.glob("*.json"))
    metafunc.parametrize("device_artifact", files, ids=[f.stem for f in files])


@pytest.fixture
def device_data(device_artifact: Path) -> dict:
    return json.loads(device_artifact.read_text())


@pytest.fixture
def running_config(device_data: dict) -> str:
    return device_data["running_config"]


@pytest.fixture
def hostname(device_data: dict) -> str:
    return device_data["hostname"]


@pytest.fixture
def device_type(device_data: dict) -> str:
    return device_data.get("device_type", "")
