from dataclasses import asdict, dataclass
from typing import Optional

from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.authorization import (
    ParsedTokenMetadataAuthorization,
    TokenMetadataAuthorityHolder,
    TokenMetadataAuthorization,
    TokenMetadataAuthorizationDetails,
    get_signer_from_token_metadata_authority,
    parse_token_metadata_authorization,
)
from original_metaplex_python.metaplex.nft_module.models.metadata import (
    is_non_fungible,
    is_programmable,
)
from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MintAddressPdaInput,
    TokenRecordPdaInput,
)
from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    AssociatedTokenAccountOptions,
)
from original_metaplex_python.metaplex.types.amount import SplTokenAmount, token
from original_metaplex_python.metaplex.types.read_api import TransferNftCompressionParam
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    TransferAccounts,
    TransferArgs,
    transfer,
)
from original_metaplex_python.token_metadata.generated.types.transfer_args import (
    from_decoded,
)

TOKEN_AUTH_RULES_ID = Pubkey.from_string("auth9SigNpDKz4sJJ1DfCTuZrZNSAgh9sFD3rboVmgg")


@dataclass
class NftOrSft:
    address: Pubkey
    token_standard: int


@dataclass
class TransferNftInput:
    nft_or_sft: NftOrSft
    to_owner: Pubkey
    authority: Optional[Signer] = None
    authorization_details: Optional[TokenMetadataAuthorizationDetails] = None
    from_owner: Optional[Pubkey] = None
    from_token: Optional[Pubkey] = None
    to_token: Optional[Pubkey] = None
    amount: Optional[SplTokenAmount] = None
    compression: Optional[TransferNftCompressionParam] = None


@dataclass
class TransferNftBuilderParams:
    nft_or_sft: NftOrSft
    to_owner: Pubkey
    authority: Optional[Signer] = None
    authorization_details: Optional[TokenMetadataAuthorizationDetails] = None
    from_owner: Optional[Pubkey] = None
    from_token: Optional[Pubkey] = None
    to_token: Optional[Pubkey] = None
    amount: Optional[SplTokenAmount] = None
    compression: Optional[TransferNftCompressionParam] = None
    instruction_key: Optional[str] = None


def transfer_nft_builder(
    metaplex,
    params: TransferNftBuilderParams,
    options: Optional[TransactionBuilderOptions | None] = None,
):
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )
    programs = options.programs if options else None

    nft_or_sft = params.nft_or_sft
    authority = params.authority or metaplex.identity()
    to_owner = params.to_owner
    amount = params.amount or token(1)
    authorization_details = params.authorization_details

    # From owner
    from_owner = params.from_owner or get_public_key(
        get_signer_from_token_metadata_authority(authority)
    )

    # Programs
    token_metadata_program = metaplex.programs().get_token_metadata(programs)
    ata_program = metaplex.programs().get_associated_token(programs)
    token_program = metaplex.programs().get_token(programs)

    # PDAs
    metadata = (
        metaplex.nfts()
        .pdas()
        .metadata(MintAddressPdaInput(mint=nft_or_sft.address, programs=programs))
    )
    edition = (
        metaplex.nfts()
        .pdas()
        .master_edition(MintAddressPdaInput(mint=nft_or_sft.address, programs=programs))
    )

    from_token = params.from_token or metaplex.tokens().pdas().associated_token_account(
        AssociatedTokenAccountOptions(
            mint=nft_or_sft.address, owner=from_owner, programs=programs
        )
    )

    to_token = params.to_token or metaplex.tokens().pdas().associated_token_account(
        AssociatedTokenAccountOptions(
            mint=nft_or_sft.address, owner=to_owner, programs=programs
        )
    )

    owner_token_record = (
        metaplex.nfts()
        .pdas()
        .token_record(
            TokenRecordPdaInput(
                mint=nft_or_sft.address, token=from_token, programs=programs
            )
        )
    )

    destination_token_record = (
        metaplex.nfts()
        .pdas()
        .token_record(
            TokenRecordPdaInput(
                mint=nft_or_sft.address, token=to_token, programs=programs
            )
        )
    )

    authority = (
        authority
        if isinstance(authority, TokenMetadataAuthorityHolder)
        else TokenMetadataAuthorityHolder(owner=authority, token=from_token)
    )

    auth: ParsedTokenMetadataAuthorization = parse_token_metadata_authorization(
        metaplex,
        TokenMetadataAuthorization(
            mint=nft_or_sft.address,
            authority=authority,
            authorization_details=authorization_details,
            programs=programs,
        ),
    )

    transaction_builder = (
        TransactionBuilder.make().set_fee_payer(payer)
        # Update the metadata account
        .add(
            InstructionWithSigners(
                instruction=transfer(
                    accounts=TransferAccounts(
                        token=from_token,
                        token_owner=from_owner,
                        destination=to_token,
                        destination_owner=to_owner,
                        mint=nft_or_sft.address,
                        metadata=metadata,
                        edition=edition if is_non_fungible(nft_or_sft) else None,
                        owner_token_record=(
                            owner_token_record if is_programmable(nft_or_sft) else None
                        ),
                        destination_token_record=(
                            destination_token_record
                            if is_programmable(nft_or_sft)
                            else None
                        ),
                        authority=auth.accounts.authority,
                        payer=get_public_key(payer),
                        sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                        spl_token_program=token_program.address,
                        spl_ata_program=ata_program.address,
                        authorization_rules=auth.accounts.authorization_rules,
                        authorization_rules_program=TOKEN_AUTH_RULES_ID,
                    ),
                    args=TransferArgs(
                        transfer_args=from_decoded(
                            {
                                "V1": {
                                    "amount": int(amount.basis_points),
                                    **asdict(auth.data),
                                }
                            }
                        )
                    ),
                    program_id=token_metadata_program.address,
                ),
                signers=[payer, *auth.signers],
                key=params.instruction_key or "transfer_nft",
            )
        )
    )
    return transaction_builder
