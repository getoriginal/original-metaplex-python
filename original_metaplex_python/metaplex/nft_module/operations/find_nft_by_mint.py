from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey
from solders.token.state import TokenAccount

from original_metaplex_python.metaplex.nft_module.models.metadata import to_metadata
from original_metaplex_python.metaplex.nft_module.models.nft import (
    to_nft,
    to_nft_with_token,
)
from original_metaplex_python.metaplex.nft_module.models.nft_edition import (
    to_nft_edition,
)
from original_metaplex_python.metaplex.nft_module.models.sft import (
    to_sft,
    to_sft_with_token,
)
from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.token_module.models.mint import (
    to_mint,
    to_mint_account,
)
from original_metaplex_python.metaplex.token_module.models.token import to_token
from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    AssociatedTokenAccountOptions,
)
from original_metaplex_python.metaplex.types.operation import use_operation
from original_metaplex_python.metaplex.types.signer import get_public_key
from original_metaplex_python.token_metadata.generated.accounts import (
    Edition,
    MasterEditionV1,
    MasterEditionV2,
    Metadata,
)
from original_metaplex_python.token_metadata.generated.types.key import (
    MasterEditionV1 as MasterEditionV1Key,
)
from original_metaplex_python.token_metadata.generated.types.key import (
    MasterEditionV2 as MasterEditionV2Key,
)

Key = "FindNftByMintOperation"


@dataclass
class FindNftByMintInput:
    mint_address: Pubkey
    token_address: Optional[Pubkey] = None
    token_owner: Optional[Pubkey] = None
    load_json_metadata: bool = True


find_nft_by_mint_operation = use_operation(Key)


@dataclass
class FindNftByMintOperation:
    def __init__(self, input: FindNftByMintInput):
        self.input = input


def to_metadata_account(client, account):
    metadata_account = Metadata.fetch_sync(conn=client, address=get_public_key(account))
    return metadata_account


def parse_original_or_print_edition_account(client, account):
    if account is None:
        return None

    edition = Edition.fetch_sync(conn=client, address=get_public_key(account))
    if edition.key == MasterEditionV1Key():
        edition = MasterEditionV1.decode(account.data)
    elif edition.key == MasterEditionV2Key():
        edition = MasterEditionV2.decode(account.data)

    return edition


def to_token_account(client, account):
    token_account = TokenAccount.from_bytes(account.data)
    return token_account


class FindNftByMintOperationHandler:
    def handle(self, operation: FindNftByMintOperation, metaplex, scope):
        programs = scope.programs
        commitment = scope.commitment
        mint_address = operation.input.mint_address
        token_address = operation.input.token_address
        token_owner = operation.input.token_owner
        load_json_metadata = operation.input.load_json_metadata or True

        associated_token_address = (
            metaplex.tokens()
            .pdas()
            .associated_token_account(
                AssociatedTokenAccountOptions(
                    mint=mint_address, owner=token_owner, programs=programs
                )
            )
            if token_owner
            else None
        )

        nft_pdas = metaplex.nfts().pdas()
        account_addresses = [
            address
            for address in [
                mint_address,
                nft_pdas.metadata(
                    MintAddressPdaInput(mint=mint_address, programs=programs)
                ),
                nft_pdas.master_edition(
                    MintAddressPdaInput(mint=mint_address, programs=programs)
                ),
                token_address or associated_token_address,
            ]
            if address is not None
        ]

        accounts = metaplex.rpc().get_multiple_accounts(account_addresses, commitment)
        # TODO_ORIGINAL: no scope
        # scope.throw_if_canceled()

        mint = to_mint(to_mint_account(accounts[0]), get_public_key(accounts[0]))
        metadata = to_metadata(
            to_metadata_account(metaplex.connection, accounts[1]),
            get_public_key(accounts[1]),
        )
        edition_account = parse_original_or_print_edition_account(
            metaplex.connection, accounts[2]
        )
        edition_public_key = get_public_key(accounts[2]) if accounts[2] else None
        if accounts[3]:
            token = to_token(
                to_token_account(metaplex.connection, accounts[3]),
                get_public_key(accounts[3]),
            )
        else:
            token = None

        if load_json_metadata:
            try:
                json = metaplex.storage().download_json(
                    metadata.uri
                )  # scope) # TODO_ORIGINAL: no scope
                metadata.json_loaded = True
                metadata.json = json
            except Exception:
                metadata.json_loaded = False
                metadata.json = None

        is_nft = (
            edition_account
            and mint.mint_authority_address
            and mint.mint_authority_address == edition_public_key
        )

        if is_nft:
            edition = to_nft_edition(edition_account, edition_public_key)
            return (
                to_nft_with_token(metadata, mint, edition, token)
                if token
                else to_nft(metadata, mint, edition)
            )

        return (
            to_sft_with_token(metadata, mint, token)
            if token
            else to_sft(metadata, mint)
        )
