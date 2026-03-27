from __future__ import annotations


def test_running_config_contains_hostname(running_config: str) -> None:
    assert "hostname " in running_config


def test_vty_uses_ssh_only(running_config: str) -> None:
    assert "line vty 0" in running_config
    assert "transport input ssh" in running_config


def test_has_no_telnet_transport(running_config: str) -> None:
    assert "transport input telnet" not in running_config
