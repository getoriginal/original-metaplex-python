from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class RevokeCollectionAuthorityAccounts(typing.TypedDict):
    collection_authority_record: Pubkey
    delegate_authority: Pubkey
    revoke_authority: Pubkey
    metadata: Pubkey
    mint: Pubkey


def revoke_collection_authority(
    accounts: RevokeCollectionAuthorityAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["collection_authority_record"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["delegate_authority"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["revoke_authority"], is_signer=True, is_writable=True
        ),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts

    # DON 4-Apr-2024 - TODO_ORIGINAL The original code uses this byte string as the identifier, however it doesn't work
    # and raises an error - "Transaction simulation failed: Error processing Instruction 0: invalid instruction data"
    #
    # We use the below descriminator of 24 instead which is taken from the javascript SDK.
    # identifier = b"\x1f\x8b\x87\xc6\x1d0\xa0\x9a"
    identifier = bytes([24])
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
