from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions.collect import collect
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_collect():
    accounts = {
        "authority": Pubkey.new_unique(),
        "recipient": Pubkey.new_unique(),
    }
    instruction = collect(accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 2
    assert instruction.accounts[0].pubkey == accounts["authority"]
    assert instruction.accounts[0].is_signer
    assert not instruction.accounts[0].is_writable
    assert instruction.accounts[1].pubkey == accounts["recipient"]
    assert not instruction.accounts[1].is_signer
    assert not instruction.accounts[1].is_writable
    assert instruction.data == b"\xd0/\xc2\x9b\x11bR\xec"


def test_collect_with_remaining_accounts():
    accounts = {
        "authority": Pubkey.new_unique(),
        "recipient": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(Pubkey.new_unique(), is_signer=False, is_writable=True),
    ]
    instruction = collect(accounts, remaining_accounts=remaining_accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 2 + len(remaining_accounts)
    assert instruction.accounts[0].pubkey == accounts["authority"]
    assert instruction.accounts[1].pubkey == accounts["recipient"]
    assert instruction.accounts[2].pubkey == remaining_accounts[0].pubkey
    assert not instruction.accounts[2].is_signer
    assert instruction.accounts[2].is_writable
    assert instruction.data == b"\xd0/\xc2\x9b\x11bR\xec"
