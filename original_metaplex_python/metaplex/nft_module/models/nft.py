from original_metaplex_python.metaplex.nft_module.models.sft import (
    is_sft_with_token,
    to_sft,
    to_sft_with_token,
)


class Nft:
    def __init__(self, metadata, mint, edition):
        for key, value in metadata.__dict__.items():
            if key not in ["model", "address", "mint"]:
                setattr(self, key, value)

        self.model = "nft"
        self.address = metadata.mint.address
        self.metadata_address = metadata.metadata_address
        self.mint = mint
        self.edition = edition


def is_nft(value):
    return isinstance(value, dict) and value.get("model") == "nft"


def assert_nft(value):
    assert is_nft(value), "Expected Nft model"


def to_nft(metadata, mint, edition):
    sft = to_sft(metadata, mint)
    return Nft(sft, mint, edition)


class NftWithToken(Nft):
    def __init__(self, metadata, mint, edition, token):
        super().__init__(metadata, mint, edition)
        self.token = token


def is_nft_with_token(value):
    return is_nft(value) and hasattr(value, "token")


def assert_nft_with_token(value):
    assert is_nft_with_token(value), "Expected Nft model with token"


def assert_nft_or_sft_with_token(value):
    assert is_nft_with_token(value) or is_sft_with_token(
        value
    ), "Expected Nft or Sft model with token"


def to_nft_with_token(metadata, mint, edition, token):
    sft_with_token = to_sft_with_token(metadata, mint, token)
    return NftWithToken(sft_with_token, mint, edition, token)
