from typing import Optional

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.errors.metaplex_error import (
    MetaplexError,
    MetaplexErrorSource,
)


class NftError(MetaplexError):
    name: str = "NftError"

    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(
            message=message,
            source=MetaplexErrorSource.PLUGIN,
            source_details="NFT",
            cause=cause,
        )


class ParentCollectionMissingError(NftError):
    name: str = "ParentCollectionMissingError"

    def __init__(self, mint: Pubkey, operation: str):
        message = (
            f"You are trying to send the operation [${operation}] which requires the NFT to have a parent "
            f"collection but that is not the case for the NFT at address [${mint}]. Ensure the NFT you are "
            f"interacting with has a parent collection."
        )
        super().__init__(message)


class DelegateRoleRequiredDataError(NftError):
    name: str = "DelegateRoleRequiredDataError"

    def __init__(self, type):
        message = (
            f"You are trying to approve a delegate of type [${type}] but did not provide any data for that "
            f"role. Please provide the data attribute as the SDK cannot provide a default value for that role."
        )
        super().__init__(message)
