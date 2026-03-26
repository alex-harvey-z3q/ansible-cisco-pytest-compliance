# Cisco Config Compliance with Ansible + pytest

This repository uses:

- **Ansible** to connect to Cisco IOS/IOS-XE devices and fetch `show running-config`
- **pytest** to evaluate compliance rules against the fetched config artifacts

The design is intentionally simple:

- no custom Ansible role is required
- Ansible handles collection and orchestration
- pytest contains the compliance logic

## Prerequisites

- macOS or Linux
- Python 3.11+
- Working SSH access to the Cisco DevNet Sandbox device
- (macOS only) Homebrew + `libssh` if you want `ansible-pylibssh`

---

## Initial setup

Create the virtual environment and install collection dependencies:

```bash
make install
```

---

## Configure LibSSH (macOS only)

On macOS, `ansible-pylibssh` needs Homebrew `libssh` headers:

```bash
export LIBSSH_PREFIX="$(brew --prefix libssh)"
export CPPFLAGS="-I${LIBSSH_PREFIX}/include"
export LDFLAGS="-L${LIBSSH_PREFIX}/lib"
export PKG_CONFIG_PATH="${LIBSSH_PREFIX}/lib/pkgconfig"
```

---

## Create a Sandbox in Cisco DevNet

1. Log in to the Cisco DevNet Sandbox portal.
    https://developer.cisco.com/site/sandbox/
2. Launch the **Catalyst 8000 Always-on** Sandbox.
3. Once ready, note the hostname, username, and password.

Export these:

```bash
export CISCO_HOST=devnetsandboxiosxec8k.cisco.com
export CISCO_USER=alexharv074
export CISCO_PASS=xxxxxxxxxxxx
```

---

## Inventory

Copy the example inventory and fill in real values:

```bash
cp inventories/devnet/hosts.yml.example inventories/devnet/hosts.yml
```

Example inventory:

```yaml
---
all:
  children:
    sandbox:
      hosts:
        sandbox:
          ansible_host: devnetsandboxiosxec8k.cisco.com
          ansible_user: your_username_here
          ansible_password: your_password_here
          ansible_network_os: cisco.ios.ios
          ansible_connection: ansible.netcommon.network_cli
          ansible_network_cli_ssh_type: paramiko
          device_type: branch_router
```

The `sandbox` group matters because the playbook targets:

```yaml
hosts: sandbox
```

---

## Main playbook

Run the workflow with:

```bash
ansible-playbook -i inventories/devnet/hosts.yml playbooks/compliance.yml
```

This will:

- fetch configs from the Cisco devices
- write JSON artifacts into `artifacts/configs/`
- run pytest against those artifacts

---

## Artifacts

Each fetched config is written as JSON, for example:

```json
{
  "hostname": "sandbox",
  "device_type": "branch_router",
  "running_config": "..."
}
```

The tests consume these artifacts rather than connecting to devices directly.

---

## Tests

The pytest suite lives in `tests/`.

Typical command:

```bash
pytest tests --artifact-dir artifacts/configs
```

Current tests are simple string-based checks over the running config.

Example assertions:
- hostname is present
- at least one NTP server is configured
- VTY configuration includes SSH access

---

## Licence

MIT
