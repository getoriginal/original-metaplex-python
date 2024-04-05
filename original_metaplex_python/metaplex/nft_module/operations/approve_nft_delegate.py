from dataclasses import dataclass
from typing import Optional, Union, cast

from solders.pubkey import Pubkey
from solders.sysvar import INSTRUCTIONS as SYSVAR_INSTRUCTIONS_PUBKEY

from original_metaplex_python.metaplex.nft_module.authorization import (
    TokenMetadataAuthority,
    TokenMetadataAuthorityHolder,
    TokenMetadataAuthorityMetadata,
    TokenMetadataAuthorization,
    TokenMetadataAuthorizationDetails,
    parse_token_metadata_authorization,
)
from original_metaplex_python.metaplex.nft_module.delegate_input import (
    DelegateInputWithData,
    parse_token_metadata_delegate_input,
)
from original_metaplex_python.metaplex.nft_module.delegate_type import (
    get_default_delegate_args,
)
from original_metaplex_python.metaplex.nft_module.models.metadata import is_non_fungible
from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MintAddressPdaInput,
)
from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    AssociatedTokenAccountOptions,
)
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.metaplex.utils.transaction_builder import (
    InstructionWithSigners,
    TransactionBuilder,
    TransactionBuilderOptions,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    DelegateAccounts,
    DelegateArgs,
)
from original_metaplex_python.token_metadata.generated.instructions import (
    delegate as delegate_instruction,
)
from original_metaplex_python.token_metadata.generated.types import TokenStandardKind
from original_metaplex_python.token_metadata.generated.types.delegate_args import (
    CollectionV1,
    CollectionV1Value,
)

TOKEN_AUTH_RULES_ID = Pubkey.from_string("auth9SigNpDKz4sJJ1DfCTuZrZNSAgh9sFD3rboVmgg")


@dataclass
class NftOrSft:
    address: Pubkey
    token_standard: TokenStandardKind


@dataclass
class ApproveNftDelegateInput:
    nft_or_sft: NftOrSft
    delegate: DelegateInputWithData
    authority: Optional[
        Union[Signer, TokenMetadataAuthorityMetadata, TokenMetadataAuthorityHolder]
    ] = None
    authorization_details: Optional[TokenMetadataAuthorizationDetails] = None


@dataclass
class ApproveNftDelegateBuilderParams(ApproveNftDelegateInput):
    instruction_key: Optional[str] = None


def approve_nft_delegate_builder(
    metaplex,
    params: ApproveNftDelegateBuilderParams,
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

    # Programs
    token_metadata_program = metaplex.programs().get_token_metadata(programs)
    token_program = metaplex.programs().get_token(programs)
    # system_program = metaplex.programs().get_system(programs)

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

    # New Delegate
    delegate_output = parse_token_metadata_delegate_input(
        metaplex=metaplex,
        mint=nft_or_sft.address,
        input=params.delegate,
        programs=programs,
    )
    delegate_record = delegate_output.delegate_record
    delegate = delegate_output.delegate
    is_token_delegate = delegate_output.is_token_delegate

    # Auth.
    if hasattr(authority, "__kind"):
        token_metadata_authority = authority
    elif hasattr(params.delegate, "owner"):
        token_metadata_authority = {
            "__kind": "holder",
            "owner": authority,
            "token": metaplex.tokens()
            .pdas()
            .associated_token_account(
                AssociatedTokenAccountOptions(
                    mint=nft_or_sft.address,
                    owner=get_public_key(authority),
                    programs=programs,
                )
            ),
        }
    else:
        token_metadata_authority = TokenMetadataAuthorityMetadata(
            update_authority=cast(Signer, authority),
        )

    auth = parse_token_metadata_authorization(
        metaplex,
        TokenMetadataAuthorization(
            mint=nft_or_sft.address,
            authority=cast(TokenMetadataAuthority, token_metadata_authority),
            authorization_details=authorization_details,
            programs=programs,
        ),
    )

    # TODO_ORIGINAL - We only implement CollectionV1 for our needs:
    # Original JS code -
    # const delegateArgsWithoutAuthData: Omit < DelegateArgs, 'authorizationData' > =
    # params.delegate.data == = undefined
    # ? getDefaultDelegateArgs(params.delegate.type)
    # : {
    #     __kind: params.delegate.type,
    #     ...params.delegate.data,
    # };

    delegate_type = (
        get_default_delegate_args(params.delegate.type)
        if params.delegate.data is None
        else {"__kind": params.delegate.type}
    )
    match delegate_type["__kind"]:
        case "CollectionV1":
            delegate_args_without_auth_data = CollectionV1(
                value=CollectionV1Value(authorization_data=params.delegate.data)
            )
        case _:
            raise Exception(f"Unsupported delegate type: {params.delegate.type}")

    # Building the transaction
    transaction_builder = TransactionBuilder.make().set_fee_payer(payer)

    instruction_key = params.instruction_key or "approve_nft_delegate"
    transaction_builder.add(
        InstructionWithSigners(
            instruction=delegate_instruction(
                accounts=DelegateAccounts(
                    delegate_record=delegate_record,
                    delegate=delegate,
                    metadata=metadata,
                    master_edition=(
                        master_edition if is_non_fungible(nft_or_sft) else None
                    ),
                    token_record=delegate_record if is_token_delegate else None,
                    mint=nft_or_sft.address,
                    token=auth.accounts.token,
                    authority=auth.accounts.authority,
                    payer=get_public_key(payer),
                    sysvar_instructions=SYSVAR_INSTRUCTIONS_PUBKEY,
                    spl_token_program=token_program.address,
                    authorization_rules_program=TOKEN_AUTH_RULES_ID,
                    authorization_rules=auth.accounts.authorization_rules,
                ),
                args=DelegateArgs(delegate_args=delegate_args_without_auth_data),
                program_id=token_metadata_program.address,
            ),
            signers=[payer] + auth.signers,
            key=instruction_key,
        )
    )

    return transaction_builder
