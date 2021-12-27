# ape-keyring

Store secrets and manage accounts for `ape` using [keyring](https://pypi.org/project/keyring/).

## Dependencies

* [python3](https://www.python.org/downloads) version 3.7 or greater, python3-dev

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

Add accounts to keyring:

```bash
ape keyring import keyring_dev_0
```

To add secrets to keyring:

```bash
ape keyring set WEB3_INFURA_PROJECT_ID
```

and then when it prompts you, input the value to your secret.

To enable your secrets to become environment variables, use the `ape-config.yaml` option `set_env_vars`:

```yaml
keyring:
  set_env_vars: true
```

## Development

This project is in early development and should be considered an alpha.
Things might not work, breaking changes are likely.
Comments, questions, criticisms and pull requests are welcomed.

## License

This project is licensed under the [Apache 2.0](LICENSE).
