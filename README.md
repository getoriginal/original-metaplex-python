# -------- THIS IS NO LONGER SUPPORTED -------- #
If you're looking for a Python version of Metaplex's libraries, this was our attempt to create one, but in the end, we decided that it was a lot to maintain on top of the actual client work we need to do. This is also based on the Token Metadata library, and Metaplex now recommend using Core - https://developers.metaplex.com/core. To help, what we can suggest is the following:

If you're using metaplex core, start by generating the instructions using anchor and the idl found here with:

`pip install "anchorpy[cli]"`

`anchorpy client-gen ./idl/mpl_core.json ./src --program-id CoREENxT6tW1HoK8ypY1SxRMZTcVPm7R94rH4PZNhX7d`

You'll need to change the discriminators to the ones found in the mpl core source code. For example, the discriminator for create_v1 0, and is found here.

We use this constant:
`CREATE_V1_INSTRUCTION_DISCRIMINATOR = bytes([0])`

Assuming you put the generated code inside a folder called metaplex/python you can do something like this in your code:
```
from .metaplex.python.types import CreateV1Args as CreateV1TypeArgs
from .metaplex.python.instructions import CreateV1Accounts
from .metaplex.python.instructions import (
    CreateV1Args as CreateV1InstructionArgs,
)
from .metaplex.python.types.data_state import AccountState

    def get_latest_blockhash_and_height(client):
          response = client.get_latest_blockhash()
          value = response.value
          return str(value.blockhash), value.last_valid_block_height

    def test_create_v1(self) -> None:
        latest_blockhash, last_valid_block_height = get_latest_blockhash_and_height(
            self.client
        )

        payer_keypair = ..."your payer keypair"
        asset_keypair = Keypair()

        try:
            instruction = create_v1(
                args=CreateV1InstructionArgs(
                    create_v1_args=CreateV1TypeArgs(
                        data_state=AccountState(),
                        name="your_asset_name",
                        uri="your_asset_uri",
                        plugins=[],
                    )
                ),
                accounts=CreateV1Accounts(
                    asset=asset_keypair.pubkey(),
                    collection=None,
                    authority=None,
                    payer=payer_keypair.pubkey(),
                    owner=owner_pubkey,
                    update_authority=None,
                    log_wrapper=None,
                ),
            )
        except Exception as e:
            raise Exception(f"Failed to create asset {e}")

        message = MessageV0.try_compile(
            payer=payer_keypair.pubkey(),
            instructions=[instruction],
            address_lookup_table_accounts=[],
            recent_blockhash=Hash.from_string(latest_blockhash),
        )

        transaction = VersionedTransaction(
            message=message, 
            keypairs=[payer_keypair, asset_keypair]
        )

        signature = self.client.send_raw_transaction(bytes(transaction)).value
        signature_status_response = self.client.confirm_transaction(
            tx_sig=signature,
            commitment=Finalized,
            sleep_seconds=0.5,
            last_valid_block_height=last_valid_block_height,
        )

        confirmed_tx = self.client.get_transaction(
            signature,
            encoding="json",
            commitment=Finalized,
            max_supported_transaction_version=0,
        )
```

# ------- Old documentation below -------- #

# original-metaplex-python
Python port of Metaplex JS SDK - https://github.com/metaplex-foundation/js

## Installing this package
If you simply want to use this package, first clone this repository on your machine, then install it from your file system using pip:

```bash
pip install -e /path/to/your/directory/original-metaplex-python
```

or poetry:

```bash
poetry add -e /path/to/your/directory/original-metaplex-python
```
Note -e adds it in editable mode.


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

First we need to create some wallets.

Use the Phantom wallet browser extension to create two new accounts. Then grab the private keys and put one in each of the files:
```
wallet_secret.txt // Used to mint NFTs
wallet_secret_friend.txt // The friend's wallet to test transferring.
```

Both files should be placed at the root of your project.

Ensure that the wallet_secret.txt account is topped up with DevNet SOL. You can get devnet SOL here: https://faucet.solana.com/ and pass the public key of the wallet.

## Test flow

`src/tests/e2e/test_create_update_flow.py` and `src/tests/e2e/test_create_update_transfer_burn_flow.py` will be the files of most interest. 
It is where the full creation of a collection, minting an NFT, updating it, transferring it and burning is tested.

The burn and transfer is separated in case you want to inspect the NFT before it is either transferred or burned.

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
