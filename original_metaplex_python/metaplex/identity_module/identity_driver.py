from original_metaplex_python.metaplex.types.signer import IdentitySigner


class IdentityDriver(IdentitySigner):
    secret_key: bytes | None = None
