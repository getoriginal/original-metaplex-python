from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import deprecated_mint_printing_tokens
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_deprecated_mint_printing_tokens():
    accounts = {
        "destination": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
    }
    instruction = deprecated_mint_printing_tokens(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 7
    assert isinstance(instruction.data, bytes)


def test_deprecated_mint_printing_tokens_with_remaining_accounts():
    accounts = {
        "destination": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = deprecated_mint_printing_tokens(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 8
