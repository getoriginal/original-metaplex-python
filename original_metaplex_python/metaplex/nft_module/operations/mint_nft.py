from dataclasses import asdict, dataclass
from typing import Optional

from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.authorization import (
    ParsedTokenMetadataAuthorization,
    TokenMetadataAuthorityMetadata,
    TokenMetadataAuthorization,
    TokenMetadataAuthorizationDetails,
    parse_token_metadata_authorization,
)
from original_metaplex_python.metaplex.nft_module.models.metadata import is_non_fungible
from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MintAddressPdaInput,
    TokenRecordPdaInput,
)
from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    AssociatedTokenAccountOptions,
)
from original_metaplex_python.metaplex.types.amount import SplTokenAmount, token
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    MintAccounts,
    MintArgs,
    mint,
)
from original_metaplex_python.token_metadata.generated.types import TokenStandardKind
from original_metaplex_python.token_metadata.generated.types.mint_args import (
    from_decoded,
)

TOKEN_AUTH_RULES_ID = Pubkey.from_string("auth9SigNpDKz4sJJ1DfCTuZrZNSAgh9sFD3rboVmgg")


@dataclass
class NftOrSft:
    address: Pubkey
    token_standard: Optional[TokenStandardKind] = None


@dataclass
class MintNftBuilderParams:
    nft_or_sft: NftOrSft
    authority: Optional[Signer] = None
    authorization_details: Optional[TokenMetadataAuthorizationDetails] = None
    to_owner: Optional[Pubkey] = None
    to_token: Optional[Pubkey] = None
    amount: Optional[SplTokenAmount] = None
    instruction_key: Optional[str] = None


def mint_nft_builder(
    metaplex,
    params: MintNftBuilderParams,
    options: Optional[TransactionBuilderOptions | None] = None,
):
    programs = options.programs if options else None
    payer = (
        options.payer
        if (options and options.payer)
        else metaplex.rpc().get_default_fee_payer()
    )

    nft_or_sft = params.nft_or_sft
    authority = params.authority or metaplex.identity()
    authorization_details = params.authorization_details
    to_owner = params.to_owner or metaplex.identity().public_key
    amount = params.amount or token(1)

    authority = (
        authority
        if isinstance(authority, TokenMetadataAuthorityMetadata)
        else TokenMetadataAuthorityMetadata(update_authority=authority)
    )

    # Auth
    auth: ParsedTokenMetadataAuthorization = parse_token_metadata_authorization(
        metaplex,
        TokenMetadataAuthorization(
            mint=nft_or_sft.address,
            authority=authority,
            authorization_details=authorization_details,
            programs=programs,
        ),
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
    master_edition = (
        metaplex.nfts()
        .pdas()
        .master_edition(MintAddressPdaInput(mint=nft_or_sft.address, programs=programs))
    )

    # Destination token account
    to_token = params.to_token or (
        metaplex.tokens()
        .pdas()
        .associated_token_account(
            AssociatedTokenAccountOptions(
                mint=nft_or_sft.address, owner=to_owner, programs=programs
            )
        )
    )

    assert to_token is not None, "to_token must be a Pubkey"

    authority_pub_key = get_public_key(auth.accounts.authority)
    payer_pub_key = get_public_key(payer)

    return (
        TransactionBuilder.make()
        .set_fee_payer(payer)
        .add(
            InstructionWithSigners(
                instruction=mint(
                    accounts=MintAccounts(
                        token=to_token,
                        token_owner=to_owner,
                        metadata=metadata,
                        master_edition=(
                            master_edition if is_non_fungible(nft_or_sft) else None
                        ),
                        token_record=metaplex.nfts()
                        .pdas()
                        .token_record(
                            TokenRecordPdaInput(
                                mint=nft_or_sft.address,
                                token=to_token,
                                programs=programs,
                            )
                        ),
                        mint=nft_or_sft.address,
                        authority=authority_pub_key,
                        delegate_record=None,
                        payer=payer_pub_key,
                        sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                        spl_token_program=token_program.address,
                        spl_ata_program=ata_program.address,
                        authorization_rules_program=auth.accounts.authorization_rules,
                        authorization_rules=TOKEN_AUTH_RULES_ID,
                    ),
                    args=MintArgs(
                        mint_args=from_decoded(
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
                key=params.instruction_key or "mint_nft",
            )
        )
    )
