import json

from solana.rpc.api import Client
from solana.rpc.commitment import Finalized
from solana.rpc.types import TxOpts
from solders.keypair import Keypair

from original_metaplex_python.metaplex import Metaplex
from original_metaplex_python.metaplex.keypair_identity.plugin import keypair_identity
from original_metaplex_python.metaplex.nft_module.operations.create_nft import (
    CreateNftBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.delete_nft import (
    DeleteNftBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.find_nft_by_mint import (
    FindNftByMintInput,
)
from original_metaplex_python.metaplex.nft_module.operations.transfer_nft import (
    NftOrSft,
    TransferNftBuilderParams,
)
from original_metaplex_python.metaplex.nft_module.operations.update_nft import (
    UpdateNftBuilderParams,
)
from original_metaplex_python.metaplex.types.creator import CreatorInput
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    ProgrammableNonFungible,
)


class AppContext:
    def __init__(self):

        self.RPC_URL = "https://blue-holy-theorem.solana-devnet.quiknode.pro/7f7ea777c1f7298cd5850c658c316f2e639bb31d/"
        with open("wallet_secret.json") as f:
            secret = json.load(f)
        self.wallet = Keypair.from_bytes(secret)

        self.metaplex = Metaplex.make(Client(self.RPC_URL)).use(
            keypair_identity(self.wallet)
        )
        self.collection_nft_mint = None
        self.mint_address = None
        self.token_address = None

    def collection_config(self):
        params = CreateNftBuilderParams(
            name="Original NFT Collection",
            uri="https://mfp2m2qzszjbowdjl2vofmto5aq6rtlfilkcqdtx2nskls2gnnsa.arweave.net/YV-mahmWUhdYaV6q4rJu6CHozWVC1CgOd9NkpctGa2Q",
            seller_fee_basis_points=0,
            is_collection=True,
            update_authority=self.wallet,
        )

        return params

    def set_collection_nft_mint(self, mint):
        self.collection_nft_mint = mint

    def nft_config(self):
        params = {
            "name": "Original NFT",
            "symbol": "ORIG",
            "seller_fee_basis_points": 500,
            "creators": [CreatorInput(address=self.wallet.pubkey(), share=100)],
            "metadata": "https://arweave.net/yIgHNXiELgQqW8QIbFM9ibVV37jhvfyW3mFcZGRX-PA",
            "collection": self.collection_nft_mint,
        }

        #
        # {"name": "QuickNode Pixel", "description": "Pixel infrastructure for everyone!",
        #  "image": "https://arweave.net/toDD51CZzdD_8LxJjrELwfXqGE0MlO_3P_GlUBu1Kpo",
        #  "attributes": [{"trait_type": "Speed", "value": "Quick"}, {"trait_type": "Type", "value": "Pixelated"},
        #                 {"trait_type": "Background", "value": "QuickNode Blue"}], "properties": {
        #     "files": [{"type": "image/png", "uri": "https://arweave.net/toDD51CZzdD_8LxJjrELwfXqGE0MlO_3P_GlUBu1Kpo"}]}}
        #
        #
        # {"name": "asset_name_5",
        #  "image_url": "https://fastly.picsum.photos/id/167/200/300.jpg?hmac=ZAuGlRPlSv0i_JnJr4FFW-OPsVz5bTx8mAI_qUYP_bM",
        #  "attributes": [{"value": "Starfish", "trait_type": "Base"}, {"value": "Big", "trait_type": "Eyes"},
        #                 {"value": "Surprised", "trait_type": "Mouth"}, {"value": "5", "trait_type": "Level"},
        #                 {"value": "1.4", "trait_type": "Stamina"}, {"value": "Happy", "trait_type": "Personality"}],
        #  "description": "Asset description",
        #  "external_url": "https://fastly.picsum.photos/id/167/200/300.jpg?hmac=ZAuGlRPlSv0i_JnJr4FFW-OPsVz5bTx8mAI_qUYP_bM",
        #  "org_image_url": "https://fastly.picsum.photos/id/167/200/300.jpg?hmac=ZAuGlRPlSv0i_JnJr4FFW-OPsVz5bTx8mAI_qUYP_bM",
        #  "original_id": "034149180226"}
        return params

    def create_collection_nft(self):
        collection_nft_builder = (
            self.metaplex.nfts().builders().create(self.collection_config())
        )

        resp = self.metaplex.rpc().send_and_confirm_transaction(collection_nft_builder)

        mint_address = collection_nft_builder.get_context()["mintAddress"]
        self.set_collection_nft_mint(mint_address)

        sig = resp["signature"]
        confirm_resp = resp["confirm_response"]
        err = confirm_resp.value[0].err
        if err:
            raise Exception(f"Failed to confirm transaction: {err}")

        print("Success!🎉")
        print(
            f"Minted Collection NFT: https://explorer.solana.com/address/{mint_address}?cluster=devnet"
        )
        print(f"Tx: https://explorer.solana.com/tx/{sig}?cluster=devnet")

    def mint_nft(self):
        nft_config = self.nft_config()
        transaction_builder = (
            self.metaplex.nfts()
            .builders()
            .create(
                CreateNftBuilderParams(
                    uri=nft_config["metadata"],
                    name=nft_config["name"],
                    seller_fee_basis_points=nft_config["seller_fee_basis_points"],
                    symbol=nft_config["symbol"],
                    creators=nft_config["creators"],
                    is_mutable=True,
                    is_collection=True,
                    collection=self.collection_nft_mint,
                    collection_authority=self.wallet.pubkey(),  # TODO: Our wallet that created the collection NFT
                    token_standard=ProgrammableNonFungible,
                    rule_set=None,
                )
            )
        )

        response = self.metaplex.rpc().send_and_confirm_transaction(transaction_builder)
        signature = response["signature"]
        confirm_response = response["confirm_response"]
        err = confirm_response.value[0].err
        if err:
            raise Exception(f"Failed to confirm transaction: {err}")

        mint_address = transaction_builder.get_context()["mintAddress"]
        token_address = transaction_builder.get_context()["tokenAddress"]
        self.mint_address = mint_address
        self.token_address = token_address

        print("Success!🎉")
        print(
            f"Minted NFT at Mint Address: https://explorer.solana.com/address/{mint_address}?cluster=devnet"
        )
        print(
            f"Token Address: https://explorer.solana.com/address/{token_address}?cluster=devnet"
        )

        print(f"Tx: https://explorer.solana.com/tx/{signature}?cluster=devnet")

    def transfer_nft(self, destination_pubkey):
        transfer_transaction_builder = (
            self.metaplex.nfts()
            .builders()
            .transfer(
                TransferNftBuilderParams(
                    nft_or_sft=NftOrSft(
                        address=self.mint_address,
                        token_standard=ProgrammableNonFungible,
                    ),
                    authority=self.wallet,
                    from_owner=self.wallet.pubkey(),
                    to_owner=destination_pubkey,
                )
            )
        )

        resp = self.metaplex.rpc().send_and_confirm_transaction(
            transfer_transaction_builder, TxOpts(preflight_commitment=Finalized)
        )

        sig = resp["signature"]
        confirm_resp = resp["confirm_response"]
        err = confirm_resp.value[0].err

        if err:
            raise Exception("Failed to confirm transfer transaction")

        print("Success!🎉")
        print(
            f"Transferred NFT: https://explorer.solana.com/address/{sig}?cluster=devnet"
        )
        print(f"To destination: {destination_pubkey}")

    def delete_nft(self):

        #########################################
        # We will need to find the account address that holds the tokens we want to burn. As a reminder, the user's wallet
        # does not hold the SPL tokens. The user's wallet owns a separate SPL token account that holds those tokens.
        # We must find that address (the Associated Token Address, ATA). SPL token accounts are Program Derived Addresses
        # (PDAs) seeded with the public key of the user's wallet and the token mint address. We can pass both into get_associated_token_address
        # to find our address

        delete_transaction_builder = (
            self.metaplex.nfts()
            .builders()
            .delete(
                DeleteNftBuilderParams(
                    mint_address=self.mint_address,
                    owner_token_account=None,
                    collection=self.collection_nft_mint,
                    parent_edition_mint=None,
                    parent_edition_token=None,
                    edition_marker=None,
                    amount=None,
                    authority=self.wallet,
                )
            )
        )

        resp = self.metaplex.rpc().send_and_confirm_transaction(
            delete_transaction_builder, TxOpts(preflight_commitment=Finalized)
        )

        sig = resp["signature"]
        confirm_resp = resp["confirm_response"]
        err = confirm_resp.value[0].err

        if err:
            raise Exception("Failed to confirm delete transaction")

        print("Success!🎉")
        print(
            f"Deleted NFT: https://explorer.solana.com/address/{self.mint_address}?cluster=devnet"
        )
        print(f"Deleted NFT: {self.mint_address}")
        print(f"Sig: {sig}")

    def find_nft(self):
        nft = self.metaplex.nfts().find_by_mint(
            FindNftByMintInput(
                mint_address=self.mint_address,
                token_address=self.token_address,
                token_owner=self.wallet.pubkey(),
            )
        )
        return nft

    def update_nft(self):

        # NEW_METADATA = {
        #     "imgType": 'image/png',
        #     "imgName": 'QuickPix New MetaName',
        #     "description": 'New description!',
        #     "attributes": [
        #         {"trait_type": 'Speed', "value": 'Quicker'},
        #         {"trait_type": 'Type', "value": 'Pixelated'},
        #         {"trait_type": 'Background', "value": 'QuickNode Blue 2'}
        #     ]
        # }

        uri = "https://arweave.net/O27ikLNE5nSWNd-oDvpmZW46VYiwnsD96JYi_v89Uss"

        # mint_address = Pubkey.from_string("9izQ6km5XfQgMYcHZmCmKYwbVv7RCpBkv1uyicbgqkBu")
        # token_address = Pubkey.from_string("mdxm6ic85bLEXqD8cq96DMhjvifiCyy9XrXmnw4nicU")

        nft = self.metaplex.nfts().find_by_mint(
            FindNftByMintInput(
                mint_address=self.mint_address,
                token_address=self.token_address,
            )
        )
        update_transaction_builder = (
            self.metaplex.nfts()
            .builders()
            .update(
                UpdateNftBuilderParams(
                    name="newName",
                    nft_or_sft=nft,
                    uri=uri,
                ),
            )
        )

        resp = self.metaplex.rpc().send_and_confirm_transaction(
            update_transaction_builder, TxOpts(preflight_commitment=Finalized)
        )

        sig = resp["signature"]
        confirm_resp = resp["confirm_response"]
        err = confirm_resp.value[0].err

        if err:
            raise Exception("Failed to confirm delete transaction")

        print("Success!🎉")
        print(f"Updated NFT: https://explorer.solana.com/address/{sig}?cluster=devnet")
        print(f"Updated NFT: {self.mint_address}")
