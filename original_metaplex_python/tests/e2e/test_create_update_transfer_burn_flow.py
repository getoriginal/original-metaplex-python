import json

from solana.rpc.api import Client
from solana.rpc.commitment import Finalized
from solana.rpc.types import TxOpts
from solders.keypair import Keypair
from solders.transaction_status import TransactionConfirmationStatus

from original_metaplex_python.metaplex import Metaplex
from original_metaplex_python.metaplex.keypair_identity.plugin import keypair_identity
from original_metaplex_python.metaplex.nft_module.operations.create_nft import (
    CreateNftBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.delete_nft import (
    DeleteNftBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.find_nft_by_mint import (
    FindNftByMintInput,
)
from original_metaplex_python.metaplex.nft_module.operations.transfer_nft import (
    NftOrSft,
    TransferNftBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.update_nft import (
    UpdateNftBuilderParams,
)
from original_metaplex_python.metaplex.types.creator import CreatorInput
from original_metaplex_python.metaplex.utils.transaction_builder import (
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    ProgrammableNonFungible,
)


def test_create_update_transfer_burn_asset_flow(project_root):
    with open(f"{project_root}/wallet_secret.json") as f:
        secret = json.load(f)

    # Wallet with Devnet SOL
    wallet = Keypair.from_bytes(secret)

    # Wallet with no SOL, but used to transfer NFT to and burn NFT. The wallet above will pay for the transactions.
    friend_key_pair = Keypair.from_base58_string(
        "37S1gcn9jCb8We2faHUCpjZKtpN4MWJswxF6UGHMQar8YEqB5sMyVVua3TkwjMepNc2sYpkJb8v8QR1TEVwzmdgi"
    )

    # Metaplex Client
    rpc_url = "https://api.devnet.solana.com"
    metaplex = Metaplex.make(Client(rpc_url)).use(keypair_identity(wallet))

    #### CREATE COLLECTION NFT ####
    collection_nft_builder = (
        metaplex.nfts()
        .builders()
        .create(
            CreateNftBuilderParams(
                name="Original NFT Collection",
                uri="https://mfp2m2qzszjbowdjl2vofmto5aq6rtlfilkcqdtx2nskls2gnnsa.arweave.net/YV-mahmWUhdYaV6q4rJu6CHozWVC1CgOd9NkpctGa2Q",
                seller_fee_basis_points=0,
                is_collection=True,
                update_authority=wallet,
                symbol="ORIG",
            )
        )
    )

    response = metaplex.rpc().send_and_confirm_transaction(collection_nft_builder)
    signature = response["signature"].value
    confirm_response = response["confirm_response"]
    blockhash = response["blockhash"]
    error = confirm_response.value[0].err
    confirmation_status = confirm_response.value[0].confirmation_status

    assert signature is not None
    assert error is None
    assert confirmation_status == TransactionConfirmationStatus.Finalized
    assert blockhash is not None

    context = collection_nft_builder.get_context()
    collection_mint_address = context["mintAddress"]
    collection_metadata_address = context["metadataAddress"]
    collection_master_edition_address = context["masterEditionAddress"]
    collection_token_address = context["tokenAddress"]

    assert collection_mint_address is not None
    assert collection_metadata_address is not None
    assert collection_master_edition_address is not None
    assert collection_token_address is not None

    if error is not None:
        raise Exception(f"Failed to confirm transaction: {error}")

    print(
        f"Minted Collection NFT: https://explorer.solana.com/address/{collection_mint_address}?cluster=devnet"
    )
    print(f"Tx: https://explorer.solana.com/tx/{signature}?cluster=devnet")

    #### CREATE NFT ####
    nft_params = {
        "name": "Original NFT",
        "symbol": "ORIG",
        "seller_fee_basis_points": 500,
        "creators": [CreatorInput(address=wallet.pubkey(), share=100)],
        "metadata": "https://arweave.net/yIgHNXiELgQqW8QIbFM9ibVV37jhvfyW3mFcZGRX-PA",
        "collection": collection_mint_address,
    }

    mint_nft_transaction_builder = (
        metaplex.nfts()
        .builders()
        .create(
            CreateNftBuilderParams(
                uri=nft_params["metadata"],
                name=nft_params["name"],
                seller_fee_basis_points=nft_params["seller_fee_basis_points"],
                symbol=nft_params["symbol"],
                creators=nft_params["creators"],
                is_mutable=True,
                is_collection=True,
                collection=collection_mint_address,
                collection_authority=wallet.pubkey(),
                token_standard=ProgrammableNonFungible,
                rule_set=None,
            )
        )
    )

    response = metaplex.rpc().send_and_confirm_transaction(mint_nft_transaction_builder)
    signature = response["signature"].value
    confirm_response = response["confirm_response"]
    blockhash = response["blockhash"]
    error = confirm_response.value[0].err
    confirmation_status = confirm_response.value[0].confirmation_status

    assert signature is not None
    assert error is None
    assert confirmation_status == TransactionConfirmationStatus.Finalized
    assert blockhash is not None

    context = mint_nft_transaction_builder.get_context()
    nft_mint_address = context["mintAddress"]
    nft_metadata_address = context["metadataAddress"]
    nft_master_edition_address = context["masterEditionAddress"]
    nft_token_address = context["tokenAddress"]

    assert nft_mint_address is not None
    assert nft_metadata_address is not None
    assert nft_master_edition_address is not None
    assert nft_token_address is not None

    if error is not None:
        raise Exception(f"Failed to confirm transaction: {error}")

    print(
        f"Minted NFT at Mint Address: https://explorer.solana.com/address/{nft_mint_address}?cluster=devnet"
    )
    print(
        f"Token Address: https://explorer.solana.com/address/{nft_token_address}?cluster=devnet"
    )
    print(f"Tx: https://explorer.solana.com/tx/{signature}?cluster=devnet")

    if error:
        raise Exception(f"Failed to confirm transaction: {error}")

    #### UPDATE NFT ####
    nft_to_update = metaplex.nfts().find_by_mint(
        FindNftByMintInput(
            mint_address=nft_mint_address,
            token_address=nft_token_address,
            # token_owner=wallet.pubkey(),
        )
    )

    uri = "https://arweave.net/O27ikLNE5nSWNd-oDvpmZW46VYiwnsD96JYi_v89Uss"
    update_transaction_builder = (
        metaplex.nfts()
        .builders()
        .update(
            UpdateNftBuilderParams(
                name="newName",
                nft_or_sft=nft_to_update,
                uri=uri,
            ),
        )
    )

    response = metaplex.rpc().send_and_confirm_transaction(
        update_transaction_builder, TxOpts(preflight_commitment=Finalized)
    )
    signature = response["signature"].value
    confirm_response = response["confirm_response"]
    blockhash = response["blockhash"]
    error = confirm_response.value[0].err
    confirmation_status = confirm_response.value[0].confirmation_status

    assert signature is not None
    assert error is None
    assert confirmation_status == TransactionConfirmationStatus.Finalized
    assert blockhash is not None

    # TODO_ORIGINAL - update_transaction_builder should set context
    context = update_transaction_builder.get_context()
    updated_nft_mint_address = nft_mint_address
    updated_nft_metadata_address = nft_metadata_address
    updated_nft_master_edition_address = nft_master_edition_address
    updated_nft_token_address = nft_token_address

    assert updated_nft_mint_address is not None
    assert updated_nft_metadata_address is not None
    assert updated_nft_master_edition_address is not None
    assert updated_nft_token_address is not None

    if error is not None:
        raise Exception(f"Failed to update: {error}")

    print("Success!🎉")
    print(
        f"Updated NFT: https://explorer.solana.com/address/{nft_mint_address}?cluster=devnet"
    )
    print(f"Tx: https://explorer.solana.com/tx/{signature}?cluster=devnet")

    #### TRANSFER NFT ####
    # In reality, we would just have the public key, but we want to burn it later
    # friend_pubkey = Pubkey.from_string("4AN2ePiudKWheFBL7e7GFa1w7HhkUPRv4qfF5WAkvH1C")
    transfer_transaction_builder = (
        metaplex.nfts()
        .builders()
        .transfer(
            TransferNftBuilderParams(
                nft_or_sft=NftOrSft(
                    address=nft_mint_address,
                    token_standard=ProgrammableNonFungible,
                ),
                authority=wallet,
                from_owner=wallet.pubkey(),
                to_owner=friend_key_pair.pubkey(),
            )
        )
    )

    response = metaplex.rpc().send_and_confirm_transaction(
        transfer_transaction_builder, TxOpts(preflight_commitment=Finalized)
    )

    signature = response["signature"].value
    confirm_response = response["confirm_response"]
    blockhash = response["blockhash"]
    error = confirm_response.value[0].err
    confirmation_status = confirm_response.value[0].confirmation_status

    assert signature is not None
    assert error is None
    assert confirmation_status == TransactionConfirmationStatus.Finalized
    assert blockhash is not None

    if error is not None:
        raise Exception(f"Failed to confirm transfer transaction {error}")

    print("Success!🎉")
    print(
        f"Transferred NFT: https://explorer.solana.com/address/{nft_mint_address}?cluster=devnet"
    )
    print(f"Tx: https://explorer.solana.com/tx/{signature}?cluster=devnet")

    #### BURN NFT ####

    delete_transaction_builder = (
        metaplex.nfts()
        .builders()
        .delete(
            input=DeleteNftBuilderParams(
                mint_address=nft_mint_address,
                owner_token_account=None,
                collection=collection_mint_address,
                parent_edition_mint=None,
                parent_edition_token=None,
                edition_marker=None,
                amount=None,
                authority=friend_key_pair,
            ),
            options=TransactionBuilderOptions(
                payer=wallet,
            ),
        )
    )

    response = metaplex.rpc().send_and_confirm_transaction(
        delete_transaction_builder, TxOpts(preflight_commitment=Finalized)
    )

    signature = response["signature"].value
    confirm_response = response["confirm_response"]
    blockhash = response["blockhash"]
    error = confirm_response.value[0].err
    confirmation_status = confirm_response.value[0].confirmation_status

    assert signature is not None
    assert error is None
    assert confirmation_status == TransactionConfirmationStatus.Finalized
    assert blockhash is not None

    # TODO_ORIGINAL - delete_transaction_builder should set context
    context = delete_transaction_builder.get_context()
    deleted_nft_mint_address = nft_mint_address
    deleted_nft_metadata_address = nft_metadata_address
    deleted_nft_master_edition_address = nft_master_edition_address
    deleted_nft_token_address = nft_token_address

    assert deleted_nft_mint_address is not None
    assert deleted_nft_metadata_address is not None
    assert deleted_nft_master_edition_address is not None
    assert deleted_nft_token_address is not None

    if error is not None:
        raise Exception(f"Failed to burn: {error}")

    print("Success!🎉")
    print(
        f"Burned NFT: https://explorer.solana.com/address/{nft_mint_address}?cluster=devnet"
    )
    print(f"Tx: https://explorer.solana.com/tx/{signature}?cluster=devnet")
