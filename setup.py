#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup  # type: ignore

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=6.0,<7.0",  # Core testing package
        "pytest-xdist",  # multi-process runner
        "pytest-cov",  # Coverage analyzer plugin
        "hypothesis>=6.2.0,<7.0",  # Strategy-based fuzzer
    ],
    "lint": [
        "black>=21.10b0,<22.0",  # auto-formatter and linter
        "mypy>=0.910,<1.0",  # Static type analyzer
        "flake8>=3.8.3,<4.0",  # Style linter
        "isort>=5.9.3,<6.0",  # Import sorting linter
    ],
    "release": [  # `release` GitHub Action job uses this
        "setuptools",  # Installation tool
        "wheel",  # Packaging tool
        "twine",  # Package upload tool
    ],
    "dev": [
        "commitizen",  # Manage commits and publishing releases
        "pre-commit",  # Ensure that linters are run prior to commiting
        "pytest-watch",  # `ptw` test watcher/runner
        "IPython",  # Console for interacting
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
    ],
}

# NOTE: `pip install -e .[dev]` to install package
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
    author="Juliya Smith",
    author_email="juliya@juliyasmith.com",
    url="https://github.com/unparalleled-js/ape-keyring",
    include_package_data=True,
    install_requires=[
        "click>=8.0.3",
        "eth-ape>=0.1.0b5",
        "eth-account>=0.5.6,<0.6.0",
        "eth-utils>=1.10.0,<1.11",
        "keyring>=23.5.0,<24.0",
        "importlib-metadata ; python_version<'3.8'",
    ],  # NOTE: Add 3rd party libraries here
    entry_points={"ape_cli_subcommands": ["ape_keyring=ape_keyring._cli:cli"]},
    python_requires=">=3.7.2,<4",
    extras_require=extras_require,
    py_modules=["ape_keyring"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"ape_keyring": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
