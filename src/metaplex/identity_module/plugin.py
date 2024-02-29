from .identity_client import IdentityClient


def identity_module():
    def install(metaplex):
        identity_client = IdentityClient()
        metaplex.identity = lambda: identity_client

    return install
