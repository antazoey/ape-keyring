# Quickstart

Avoid hard-coding secrets in your projects using `ape-keyring`.
`ape-keyring` is built on top of [keyring](https://pypi.org/project/keyring/) and is an account plugin and secret manager.
By default, `keyring` uses your OS's secure storage and prompts for authorization upon request.
Thus, `keyring` is useful for securely managing local developer environments.

This guide demonstrates how to use `ape-keyring` as an account plugin and secret manager.

## Dependencies

* [python3](https://www.python.org/downloads) version 3.8 or greater, python3-dev

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-keyring
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-keyring.git
cd ape_keyring
python3 setup.py install
```

## Quick Usage

### Accounts

Use `ape-keyring` as an account plugin.
You can add existing accounts to keyring to use in your scripts, console, or tests:

```bash
ape keyring import keyring_dev_0
```

It then securely prompts you for your private key.

**NOTE**: You can only add existing accounts to keyring and generate new ones.

You can delete accounts by doing:

```bash
ape keyring accounts delete <alias>
```

This only deletes the account from keyring and not the blockchain.

To remove all your keyring accounts, run the command:

```bash
ape keyring accounts delete-all
```

Finally, list your accounts by doing:

```bash
ape keyring accounts list
```

### Secrets

Use `ape-keyring` as a secrets managers, such as Infura project IDs, Etherscan API keys, your mother's maiden name.
To add secrets to keyring, do:

```bash
ape keyring set WEB3_API_KEY
```

and then when it prompts you, input the value to your secret.

Optionally, scope your secrets to the active project.

```bah
ape keyring set DEPLOYMENT_SECRET --scope project 
```

To enable your secrets to become environment variables at runtime,
use the `ape-config.yaml` option `set_env_vars`:

```yaml
keyring:
  set_env_vars: true
```
