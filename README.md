# Molecule additions for playbook-based testing

This archive contains the extra files needed to test the playbook-oriented
Ansible + pytest design with Molecule.

## Scenarios

- `molecule/default`: happy path
  - `prepare.yml` configures the device to satisfy the pytest checks
  - `converge.yml` runs the real `playbooks/compliance.yml` and expects success

- `molecule/fail`: expected-failure path
  - `prepare.yml` introduces deliberate VTY drift
  - `converge.yml` runs the real `playbooks/compliance.yml` and asserts that it fails

## Usage

From the project root:

```bash
make molecule-default
make molecule-fail
```

Both scenarios assume you already have a real inventory file at:

`inventories/devnet/hosts.yml`
