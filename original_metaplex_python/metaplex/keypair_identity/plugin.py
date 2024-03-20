from .keypair_identity_driver import KeypairIdentityDriver


def keypair_identity(keypair):
    def install(metaplex):
        metaplex.identity().set_driver(KeypairIdentityDriver(keypair))

    return install
