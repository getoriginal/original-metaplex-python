from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, cast

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.delegate_input import (
    MetadataDelegateInputWithData,
    TokenDelegateInputWithData,
    TokenMetadataDelegateInput,
    parse_token_metadata_delegate_input,
)
from original_metaplex_python.metaplex.types.program import Program
from original_metaplex_python.metaplex.types.signer import Signer, get_public_key
from original_metaplex_python.token_metadata.generated.types import AuthorizationData

# /**
#  * Defines an authority that can handle a digital asset (NFT, SFT, etc.).
#  *
#  * An authority can be one of the following:
#  * - Metadata: the update authority of the metadata account.
#  * - Holder: the owner of the token account, i.e. the owner of the asset.
#  * - Metadata Delegate: an approved delegate authority of the metadata account for a given action.
#  * - Token Delegate: an approved delegate authority of the token account for a given action.
#  */


# The update authority of the metadata account.
@dataclass
class TokenMetadataAuthorityMetadata:
    update_authority: Signer
    token: Optional[Pubkey] = None
    kind: str = "metadata"


# The owner of the token account, i.e. the owner of the asset.
@dataclass
class TokenMetadataAuthorityHolder:
    owner: Signer
    token: Pubkey
    kind: str = "holder"


# An approved delegate authority of the metadata account for a given action.
@dataclass
class TokenMetadataAuthorityMetadataDelegate:
    delegate: Signer
    update_authority: Pubkey
    type: str
    kind: str = "metadata_delegate"


# An approved delegate authority of the token account for a given action.
@dataclass
class TokenMetadataAuthorityTokenDelegate:
    delegate: Signer
    type: str
    owner: Pubkey
    token: Optional[Pubkey] = None
    kind: str = "token_delegate"


TokenMetadataAuthority = Union[
    TokenMetadataAuthorityMetadata,
    TokenMetadataAuthorityHolder,
    TokenMetadataAuthorityMetadataDelegate,
    TokenMetadataAuthorityTokenDelegate,
]


class AuthorityType(Enum):
    None_ = 0
    Metadata = 1
    Holder = 2
    MetadataDelegate = 3
    TokenDelegate = 4


@dataclass
class TokenMetadataAuthorizationDetails:
    rules: Pubkey
    data: Optional[AuthorizationData] = None


@dataclass
class TokenMetadataAuthorizationAccount:
    authority: Pubkey
    token: Optional[Pubkey] = None
    approver: Optional[Pubkey] = None
    delegate_record: Optional[Pubkey] = None
    authorization_rules: Optional[Pubkey] = None


@dataclass
class TokenMetadataAuthorizationData:
    authority_type: Union[AuthorityType | None]
    authorization_data: Optional[AuthorizationData] = None


@dataclass
class ParsedTokenMetadataAuthorization:
    accounts: TokenMetadataAuthorizationAccount
    signers: list[Signer]
    data: TokenMetadataAuthorizationData


@dataclass
class TokenMetadataAuthorization:
    mint: Pubkey
    authority: TokenMetadataAuthority
    authorization_details: Optional[TokenMetadataAuthorizationDetails] = None
    programs: Optional[list[Program]] = None


def parse_token_metadata_authorization(
    metaplex, input: TokenMetadataAuthorization
) -> ParsedTokenMetadataAuthorization:
    auth = ParsedTokenMetadataAuthorization(
        accounts=TokenMetadataAuthorizationAccount(
            authority=cast(
                Pubkey, None
            ),  # TODO_ORIGINAL: This is not set in original JS code, but don't want to make it optional
            authorization_rules=(
                input.authorization_details.rules
                if input.authorization_details
                else None
            ),
        ),
        signers=[],
        data=TokenMetadataAuthorizationData(
            authority_type=None,
            authorization_data=(
                input.authorization_details.data
                if input.authorization_details
                else None
            ),
        ),
    )

    if isinstance(input.authority, TokenMetadataAuthorityMetadata):
        auth.accounts.authority = get_public_key(input.authority.update_authority)
        auth.accounts.token = input.authority.token
        auth.signers.append(input.authority.update_authority)
        auth.data.authority_type = AuthorityType.Metadata
    elif isinstance(input.authority, TokenMetadataAuthorityMetadataDelegate):
        delegate_input = TokenMetadataDelegateInput(
            owner=input.authority.update_authority,
            delegate=input.authority.delegate,
            token=None,
            update_authority=input.authority.update_authority,
            type=input.authority.type,
        )
        delegate_output = parse_token_metadata_delegate_input(
            metaplex=metaplex,
            mint=input.mint,
            input=cast(MetadataDelegateInputWithData, delegate_input),
            programs=input.programs,
        )
        delegate_record = delegate_output.delegate_record
        approver = delegate_output.approver

        auth.accounts.authority = get_public_key(input.authority.delegate)
        auth.accounts.delegate_record = delegate_record
        auth.accounts.approver = approver
        auth.signers.append(input.authority.delegate)
        auth.data.authority_type = AuthorityType.MetadataDelegate
    elif isinstance(input.authority, TokenMetadataAuthorityTokenDelegate):
        delegate_input = TokenMetadataDelegateInput(
            owner=input.authority.owner,
            delegate=input.authority.delegate,
            token=input.authority.token,
            update_authority=None,
            type=input.authority.type,
        )

        delegate_output = parse_token_metadata_delegate_input(
            metaplex=metaplex,
            mint=input.mint,
            input=cast(TokenDelegateInputWithData, delegate_input),
            programs=input.programs,
        )

        delegate_record = delegate_output.delegate_record
        approver = delegate_output.approver
        token_account = delegate_output.token_account

        auth.accounts.authority = get_public_key(input.authority.delegate)
        auth.accounts.token = token_account
        auth.accounts.delegate_record = delegate_record
        auth.accounts.approver = approver
        auth.signers.append(input.authority.delegate)
        auth.data.authority_type = AuthorityType.TokenDelegate
    elif isinstance(input.authority, TokenMetadataAuthorityHolder):
        auth.accounts.authority = get_public_key(input.authority.owner)
        auth.accounts.token = input.authority.token
        auth.signers.append(input.authority.owner)
        auth.data.authority_type = AuthorityType.Holder
    else:
        raise ValueError("Unreachable case: " + input.authority.kind)

    return auth


def get_signer_from_token_metadata_authority(
    authority: TokenMetadataAuthority | Signer,
):
    if (
        not isinstance(authority, TokenMetadataAuthorityMetadata)
        and not isinstance(authority, TokenMetadataAuthorityHolder)
        and not isinstance(authority, TokenMetadataAuthorityMetadataDelegate)
        and not isinstance(authority, TokenMetadataAuthorityTokenDelegate)
    ):
        return authority

    if isinstance(authority, TokenMetadataAuthorityMetadata):
        return authority.update_authority
    elif isinstance(authority, TokenMetadataAuthorityMetadataDelegate) or isinstance(
        authority, TokenMetadataAuthorityTokenDelegate
    ):
        return authority.delegate
    elif isinstance(authority, TokenMetadataAuthorityHolder):
        return authority.owner
    else:
        raise ValueError(f"Unreachable case: {authority}")
