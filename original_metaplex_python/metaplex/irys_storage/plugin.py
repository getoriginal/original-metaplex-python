from .irys_storage_driver import IrysStorageDriver


def irys_storage(options={}):
    def install(metaplex):
        storage_client = IrysStorageDriver(metaplex, options)
        metaplex.storage().set_driver(storage_client)

    return install
