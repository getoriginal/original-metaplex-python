from original_metaplex_python.metaplex.storage_module.storage_client import (
    StorageClient,
)


def storage_module():
    def install(metaplex):
        storage_client = StorageClient()
        metaplex.storage = lambda: storage_client

    return install
