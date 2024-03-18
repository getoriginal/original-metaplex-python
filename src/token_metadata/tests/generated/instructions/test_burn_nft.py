from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import burn_nft
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_burn_nft():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "master_edition_account": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "collection_metadata": Pubkey.new_unique(),
    }
    instruction = burn_nft(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 7
    assert isinstance(instruction.data, bytes)


def test_burn_nft_without_collection_metadata():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "master_edition_account": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "collection_metadata": None,
    }
    instruction = burn_nft(accounts)
    assert len(instruction.accounts) == 7


def test_burn_nft_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "master_edition_account": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "collection_metadata": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = burn_nft(accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 8
