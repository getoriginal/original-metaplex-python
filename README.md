# original-metaplex-python
Python port of Metaplex JS SDK - https://github.com/metaplex-foundation/js

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management and packaging

### Setting Up the Development Environment

1. **Clone the repository**

```bash
git clone https://github.com/getoriginal/original-metaplex-python.git
cd original-metaplex-python
```

2. **Install dependencies**

Run the following command to install the project dependencies:

```bash
poetry install --no-root
```


This command reads the `pyproject.toml` file and installs all necessary dependencies, including development dependencies, into a new virtual environment managed by Poetry.

3. **Activate the virtual environment**

To activate the Poetry-managed virtual environment, use:

```bash
poetry shell
```


Alternatively, you can run commands within the virtual environment using `poetry run <command>` without activating it.

4. **Set up pre-commit hooks**

Install the pre-commit hooks with:

```bash
pre-commit install
```

This step ensures that the code linters and formatters run on every commit to maintain code quality and consistency.

### Running the Application

Create a new wallet using 
    
```bash
solana-keygen new
```

This will generate a new wallet and give you the path, the seed phrase and public key in the terminal. Copy the file generated into the root of the project and rename it to `wallet_secret.json`.

For security reasons, do not commit this file to the repository.

Ensure the wallet that it refers to is topped up with DevNet SOL. You can get devnet SOL here: https://faucet.solana.com/ and pass the public key of the wallet.

## Test flow

`src/tests/e2e/test_create_update_transfer_burn_flow.py` will be the file of most interest. 
It is where the full creation of a collection, minting an NFT, updating it, transferring it and burning is tested.
If you use pycharm, you should be able to run the tests from the IDE.


### Running Tests

To run the unit tests, use the following command:

```bash
poetry run pytest -m unit
```

And for the e2e test flow, use the following command:

```bash
poetry run pytest -m e2e
```

You can also just run this if you want to experiment with the flow outside the tests:
    
```bash
python -m original_metaplex_python.app
```

## Tools & IDE

### black: code formatter

https://black.readthedocs.io/  
config: pyproject.toml  
pre-commit & pre-push: enabled

```bash
black .
pre-commit run black --all-files
```


### flake8: linter

https://flake8.pycqa.org/  
config: .flake8  
pre-commit & pre-push: enabled  

```bash
flake8 .
pre-commit run flake8 --all-files
```

### isort: import sorting

https://pycqa.github.io/isort/  
config: pyproject.toml  
pre-commit & pre-push: enabled

```bash
isort .
pre-commit run isort --all-files
```

### mypy: type checking

https://mypy.readthedocs.io/  
config: mypy.ini  
pre-commit & pre-push: enabled

```bash
mypy .
pre-commit run mypy --all-files
```