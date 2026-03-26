from __future__ import annotations


def test_vty_uses_ssh_only(running_config: str) -> None:
    assert "line vty 0" in running_config
    assert "transport input ssh" in running_config
