from dataclasses import dataclass

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.types.amount import SplTokenAmount


@dataclass
class NftOriginalEdition:
    model: str
    is_original: bool
    address: Pubkey
    supply: SplTokenAmount
    max_supply: SplTokenAmount


def to_nft_original_edition(account, public_key):
    return NftOriginalEdition(
        model="nftEdition",
        is_original=True,
        address=public_key,
        supply=account.supply,
        max_supply=account.max_supply,
    )


@dataclass
class NftPrintEdition:
    model: str
    is_original: bool
    address: Pubkey
    parent: Pubkey
    number: SplTokenAmount


def to_nft_print_edition(account, public_key):
    return NftPrintEdition(
        model="nftEdition",
        is_original=False,
        address=public_key,
        parent=account.parent,
        number=account.edition,
    )


def is_original_edition(account):
    return account.max_supply is not None


def is_print_edition_account(account):
    return not is_original_edition(account)


def to_nft_edition(account, public_key):
    if is_original_edition(account):
        return to_nft_original_edition(account, public_key)
    else:
        return to_nft_print_edition(account, public_key)
