from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT

from ..program_id import PROGRAM_ID


class ApproveCollectionAuthorityAccounts(typing.TypedDict):
    collection_authority_record: Pubkey
    new_collection_authority: Pubkey
    update_authority: Pubkey
    payer: Pubkey
    metadata: Pubkey
    mint: Pubkey


def approve_collection_authority(
    accounts: ApproveCollectionAuthorityAccounts,
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
            pubkey=accounts["new_collection_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["update_authority"], is_signer=True, is_writable=True
        ),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        (
            AccountMeta(pubkey=RENT, is_signer=False, is_writable=False)
            if RENT
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts

    # DON 4-Apr-2024 - TODO_ORIGINAL The original code uses this byte string as the identifier, however it doesn't work
    # and raises an error - "Transaction simulation failed: Error processing Instruction 0: invalid instruction data"
    #
    # We use the below descriminator of 23 instead which is taken from the javascript SDK.
    # identifier = b"\xfe\x88\xd0'AB\x1bo"
    identifier = bytes([23])
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
