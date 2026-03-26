from __future__ import annotations


def test_has_at_least_one_ntp_server(running_config: str) -> None:
    assert "ntp server " in running_config
