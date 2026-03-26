from __future__ import annotations


def test_running_config_contains_hostname(running_config: str, hostname: str) -> None:
    assert f"hostname {hostname}" in running_config


def test_has_at_least_one_ntp_server(running_config: str) -> None:
    assert "ntp server " in running_config


def test_vty_uses_ssh_only(running_config: str) -> None:
    assert "line vty 0" in running_config
    assert "transport input ssh" in running_config
