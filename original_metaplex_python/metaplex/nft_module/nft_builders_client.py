from typing import Optional

from ..utils.transaction_builder import TransactionBuilderOptions
from .operations.approve_nft_collection_authority import (
    ApproveNftCollectionAuthorityBuilderParams,
    approve_nft_collection_authority_builder,
)
from .operations.approve_nft_delegate import (
    ApproveNftDelegateBuilderParams,
    approve_nft_delegate_builder,
)
from .operations.create_nft import CreateNftBuilderParams, create_nft_builder
from .operations.create_sft import CreateSftBuilderParams, create_sft_builder
from .operations.delete_nft import DeleteNftBuilderParams, delete_nft_builder
from .operations.mint_nft import MintNftBuilderParams, mint_nft_builder
from .operations.revoke_nft_collection_authority import (
    RevokeNftCollectionAuthorityBuilderParams,
    revoke_nft_collection_authority_builder,
)
from .operations.transfer_nft import TransferNftBuilderParams, transfer_nft_builder
from .operations.unverify_nft_collection import (
    UnverifyNftCollectionBuilderParams,
    unverify_nft_collection_builder,
)
from .operations.update_nft import UpdateNftBuilderParams, update_nft_builder
from .operations.verify_nft_collection import (
    VerifyNftCollectionBuilderParams,
    verify_nft_collection_builder,
)
from .operations.verify_nft_creator import (
    VerifyNftCreatorBuilderParams,
    verify_nft_creator_builder,
)


class NftBuildersClient:
    metaplex = None

    def __init__(self, metaplex):
        self.metaplex = metaplex

    def create(
        self,
        input: CreateNftBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return create_nft_builder(self.metaplex, input, options)

    def create_sft(
        self,
        input: CreateSftBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return create_sft_builder(self.metaplex, input, options)

    def mint(
        self,
        input: MintNftBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return mint_nft_builder(self.metaplex, input, options)

    def transfer(
        self,
        input: TransferNftBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return transfer_nft_builder(self.metaplex, input, options)

    def verify_collection(
        self,
        input: VerifyNftCollectionBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return verify_nft_collection_builder(self.metaplex, input, options)

    def verify_creator(
        self,
        input: VerifyNftCreatorBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return verify_nft_creator_builder(self.metaplex, input, options)

    def unverify_collection(
        self,
        input: UnverifyNftCollectionBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return unverify_nft_collection_builder(self.metaplex, input, options)

    def approve_collection_authority(
        self,
        input: ApproveNftCollectionAuthorityBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return approve_nft_collection_authority_builder(self.metaplex, input, options)

    def revoke_collection_authority(
        self,
        input: RevokeNftCollectionAuthorityBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return revoke_nft_collection_authority_builder(self.metaplex, input, options)

    def delete(
        self,
        input: DeleteNftBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return delete_nft_builder(self.metaplex, input, options)

    def update(
        self,
        input: UpdateNftBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return update_nft_builder(self.metaplex, input, options)

    def delegate(
        self,
        input: ApproveNftDelegateBuilderParams,
        options: Optional[TransactionBuilderOptions] = None,
    ):
        return approve_nft_delegate_builder(self.metaplex, input, options)

    # TODO_ORIGINAL: Not used yet
    # def revoke(
    #         self,
    #         input: RevokeNftDelegateBuilderParams,
    #         options: Optional[TransactionBuilderOptions] = None
    # ):
    #     return revokeNftDelegateBuilder(self.metaplex, input, options);
