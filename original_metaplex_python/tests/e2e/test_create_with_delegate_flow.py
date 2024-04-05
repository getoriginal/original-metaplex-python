from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.transaction_status import TransactionConfirmationStatus

from original_metaplex_python.metaplex import Metaplex
from original_metaplex_python.metaplex.keypair_identity.plugin import keypair_identity
from original_metaplex_python.metaplex.nft_module.delegate_input import (
    MetadataDelegateInputWithData,
)
from original_metaplex_python.metaplex.nft_module.operations.approve_nft_delegate import (
    ApproveNftDelegateBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.create_nft import (
    CreateNftBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.transfer_nft import (
    NftOrSft,
)
from original_metaplex_python.metaplex.types.creator import CreatorInput
from original_metaplex_python.metaplex.utils.transaction_builder import (
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    ProgrammableNonFungible,
)


def test_create_with_delegate_flow(project_root):
    try:
        with open(f"{project_root}/wallet_secret.txt") as f:
            secret = f.read()
            wallet = Keypair.from_base58_string(secret)
    except FileNotFoundError:
        raise Exception("Please provide a valid wallet secret file with a private key")

    try:
        with open(f"{project_root}/wallet_secret_friend.txt") as f:
            friend_secret = f.read()
            friend_key_pair = Keypair.from_base58_string(friend_secret)
    except FileNotFoundError:
        print(
            "Please provide a wallet secret file to test transferring NFT to a friend."
        )
        return

    # Metaplex Client
    rpc_url = "https://api.devnet.solana.com"

    ### .use(keypair_identity(wallet) is needed to grab the collection_update_authority later.
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
                mint_authority=wallet,
                symbol="ORIG",
                token_owner=wallet.pubkey(),
            ),
            options=TransactionBuilderOptions(payer=wallet),
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

    #### APPROVE FRIEND TO VERIFY NFT ####
    #### NOT applicable for ProgrammableNonFungible ####
    # approve_transaction_builder = (
    #     metaplex.nfts()
    #     .builders()
    #     .approve_collection_authority(
    #         input=ApproveNftCollectionAuthorityBuilderParams(
    #             mint_address=collection_mint_address,
    #             update_authority=wallet,
    #             collection_authority=friend_key_pair.pubkey(),
    #         ),
    #         options=TransactionBuilderOptions(
    #             payer=wallet,
    #         ),
    #     )
    # )

    # We must use the new delegate builder instead
    approve_delegate_builder = (
        metaplex.nfts()
        .builders()
        .delegate(
            input=ApproveNftDelegateBuilderParams(
                nft_or_sft=NftOrSft(
                    address=collection_mint_address,
                    token_standard=ProgrammableNonFungible,
                ),
                delegate=MetadataDelegateInputWithData(
                    type="CollectionV1",
                    delegate=friend_key_pair.pubkey(),
                    update_authority=wallet.pubkey(),
                ),
                authority=wallet,
            ),
            options=TransactionBuilderOptions(
                payer=wallet,
            ),
        )
    )

    response = metaplex.rpc().send_and_confirm_transaction(approve_delegate_builder)
    signature = response["signature"].value
    confirm_response = response["confirm_response"]
    blockhash = response["blockhash"]
    error = confirm_response.value[0].err
    confirmation_status = confirm_response.value[0].confirmation_status

    print(
        f"Approved Collection Delegate: https://explorer.solana.com/address/{collection_mint_address}?cluster=devnet"
    )
    print(f"Tx: https://explorer.solana.com/tx/{signature}?cluster=devnet")

    if error:
        raise Exception(f"Failed to confirm transaction: {error}")

    assert signature is not None
    assert error is None
    assert confirmation_status == TransactionConfirmationStatus.Finalized
    assert blockhash is not None

    #### CREATE NFT ####
    nft_params = {
        "name": "Original NFT",
        "symbol": "ORIG",
        "seller_fee_basis_points": 500,
        "creators": [CreatorInput(address=friend_key_pair.pubkey(), share=100)],
        "metadata": "https://arweave.net/yIgHNXiELgQqW8QIbFM9ibVV37jhvfyW3mFcZGRX-PA",
        "collection": collection_mint_address,
    }

    token_owner = Keypair()

    # NOTE - This only works with an approved delegate because we have .use(keypair_identity(wallet))) set above
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
                collection=collection_mint_address,
                collection_authority=friend_key_pair,
                collection_authority_is_delegated="metadata_delegate",
                token_standard=ProgrammableNonFungible,
                token_owner=token_owner.pubkey(),
                update_authority=friend_key_pair,
                mint_authority=friend_key_pair,
            ),
            options=TransactionBuilderOptions(
                payer=friend_key_pair,
            ),
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
