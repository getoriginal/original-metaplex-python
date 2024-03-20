from typing import Generic, Optional, TypeVar

from solders.pubkey import Pubkey


class AccountNotFoundError(Exception):
    pass


T = TypeVar("T")


class AccountInfo:
    def __init__(
        self,
        executable: bool,
        owner: Pubkey,
        lamports: int,
        rent_epoch: Optional[int] = None,
    ):
        self.executable = executable
        self.owner = owner
        self.lamports = lamports
        self.rent_epoch = rent_epoch


class Account(AccountInfo, Generic[T]):
    def __init__(
        self,
        executable: bool,
        owner: Pubkey,
        lamports: int,
        public_key: Pubkey,
        data: T,
        rent_epoch: Optional[int] = None,
    ):
        super().__init__(executable, owner, lamports, rent_epoch)
        self.public_key = public_key
        self.data = data


class MintAccount(Account):
    pass


class MaybeAccount:
    def __init__(
        self,
        public_key,
        exists,
        data=None,
        executable=None,
        owner=None,
        lamports=None,
        rent_epoch=None,
    ):
        self.public_key = public_key
        self.exists = exists
        self.data = data
        self.executable = executable
        self.owner = owner
        self.lamports = lamports
        self.rent_epoch = rent_epoch


class UnparsedAccount(Account):
    pass


class UnparsedMaybeAccount(MaybeAccount):
    pass


def account_parsing_function(unparsed_account):
    raise NotImplementedError("account_parsing_function")


def account_parsing_and_asserting_function(unparsed_account, solution=None):
    raise NotImplementedError("account_parsing_and_asserting_function")
