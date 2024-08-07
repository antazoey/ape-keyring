#!/usr/bin/env python
from setuptools import find_packages, setup

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=6.0",  # Core testing package
        "pytest-xdist",  # multi-process runner
        "pytest-cov",  # Coverage analyzer plugin
        "hypothesis>=6.2.0,<7.0",  # Strategy-based fuzzer
    ],
    "lint": [
        "black>=24.4.2",  # auto-formatter and linter
        "mypy>=1.10.1,<2",  # Static type analyzer
        "types-setuptools",  # Needed for mypy typeshed
        "flake8>=7.1.0",  # Style linter
        "isort>=5.10.1",  # Import sorting linter
        "mdformat>=0.7.17",  # Auto-formatter for markdown
        "mdformat-gfm>=0.3.5",  # Needed for formatting GitHub-flavored markdown
        "mdformat-frontmatter>=0.4.1",  # Needed for frontmatters-style headers in issue templates
        "mdformat-pyproject>=0.0.1",  # Allows configuring in pyproject.toml
    ],
    "release": [  # `release` GitHub Action job uses this
        "setuptools",  # Installation tool
        "wheel",  # Packaging tool
        "twine",  # Package upload tool
    ],
    "dev": [
        "commitizen",  # Manage commits and publishing releases
        "pre-commit",  # Ensure that linters are run prior to committing
        "pytest-watch",  # `ptw` test watcher/runner
        "IPython",  # Console for interacting
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
    ],
}

extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["release"]
    + extras_require["dev"]
)

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="ape-keyring",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="""ape-keyring: Store secrets for ape using Keyring.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="antazoey",
    author_email="antyzoa@gmail.com",
    url="https://github.com/antazoey/ape-keyring",
    include_package_data=True,
    install_requires=[
        "click",  # Use same version as eth-ape
        "eth-ape>=0.8.8,<0.9",
        "eth-account",  # Use same version as eth-ape
        "eth-utils",  # Use same version as eth-ape
        "eip712",  # Use same version as eth-ape
        "keyring>=24.3.0,<25",
    ],
    entry_points={"ape_cli_subcommands": ["ape_keyring=ape_keyring._cli:cli"]},
    python_requires=">=3.8,<4",
    extras_require=extras_require,
    py_modules=["ape_keyring"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"ape_keyring": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
