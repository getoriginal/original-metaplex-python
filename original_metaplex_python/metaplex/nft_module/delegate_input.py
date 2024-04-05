from dataclasses import dataclass
from typing import Any, Optional, Union, cast

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.nft_module.nft_pdas_client import (
    MetadataDelegateRecordPdaInput,
    TokenRecordPdaInput,
)
from original_metaplex_python.metaplex.token_module.token_pdas_client import (
    AssociatedTokenAccountOptions,
)
from original_metaplex_python.metaplex.types.program import Program
from original_metaplex_python.metaplex.types.signer import Signer, is_signer


@dataclass
class TokenMetadataDelegateInput:
    delegate: Signer
    type: str
    update_authority: Optional[Pubkey]
    owner: Optional[Pubkey]
    token: Optional[Pubkey]


@dataclass
class TokenMetadataDelegateOutput:
    is_token_delegate: bool
    delegate: Signer
    approver: Pubkey
    delegate_record: Pubkey
    token_account: Optional[Pubkey] = None


@dataclass
class MetadataDelegateInputWithData:
    delegate: Signer
    update_authority: Pubkey
    type: str
    data: Optional[Any] = None
    __kind: Optional[Any] = None


@dataclass
class TokenDelegateInputWithData:
    delegate: Signer
    owner: Pubkey
    type: str
    data: Any
    __kind: Any
    token: Optional[Pubkey] = None


DelegateInputWithData = Union[MetadataDelegateInputWithData, TokenDelegateInputWithData]


def parse_token_metadata_delegate_input(
    metaplex,
    mint: Pubkey,
    input: DelegateInputWithData,
    programs: Optional[list[Program]] = None,
):
    if hasattr(input, "update_authority"):
        return TokenMetadataDelegateOutput(
            is_token_delegate=False,
            delegate=input.delegate,
            approver=cast(Pubkey, input.update_authority),
            delegate_record=metaplex.nfts()
            .pdas()
            .metadata_delegate_record(
                MetadataDelegateRecordPdaInput(
                    mint=mint,
                    type=input.type,
                    update_authority=cast(Pubkey, input.update_authority),
                    delegate=cast(
                        Pubkey,
                        (
                            input.delegate.public_key
                            if is_signer(input.delegate)
                            else input.delegate
                        ),
                    ),
                    programs=programs,
                )
            ),
        )

    token_account = (
        input.token
        if input.token
        else metaplex.tokens()
        .pdas()
        .associated_token_account(
            AssociatedTokenAccountOptions(
                mint=mint,
                owner=cast(Pubkey, input.owner),
                programs=programs,
            )
        )
    )

    return TokenMetadataDelegateOutput(
        is_token_delegate=True,
        delegate=input.delegate,
        approver=cast(Pubkey, input.owner),
        delegate_record=metaplex.nfts()
        .pdas()
        .token_record(
            TokenRecordPdaInput(
                mint=mint,
                token=token_account,
                programs=programs,
            )
        ),
        token_account=token_account,
    )
