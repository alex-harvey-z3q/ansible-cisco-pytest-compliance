from __future__ import annotations


def test_running_config_contains_hostname(running_config: str, hostname: str) -> None:
    assert f"hostname {hostname}" in running_config
