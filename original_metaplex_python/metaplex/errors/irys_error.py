from .metaplex_error import MetaplexError, MetaplexErrorSource


class IrysError(MetaplexError):
    def __init__(self, message, cause=None):
        super().__init__(message, MetaplexErrorSource.PLUGIN, "Irys", cause)
        self.name = "IrysError"


class FailedToInitializeIrysError(IrysError):
    def __init__(self, cause):
        message = "Irys could not be initialized. Please check the underlying error below for more details."
        super().__init__(message, cause)
        self.name = "FailedToInitializeIrysError"


class FailedToConnectToIrysAddressError(IrysError):
    def __init__(self, address, cause):
        message = f'Irys could not connect to the provided address [{address}]. Please ensure the provided address is valid. Some valid addresses include: "https://node1.irys.xyz" for mainnet and "https://devnet.irys.xyz" for devnet'
        super().__init__(message, cause)
        self.name = "FailedToConnectToIrysAddressError"


class AssetUploadFailedError(IrysError):
    def __init__(self, status):
        message = f"The asset could not be uploaded to the Irys network and returned the following status code [{status}]."
        super().__init__(message)
        self.name = "AssetUploadFailedError"


class IrysWithdrawError(IrysError):
    def __init__(self, error):
        message = f"The balance could not be withdrawn from the Irys network and returned the following error: {error}."
        super().__init__(message)
        self.name = "IrysWithdrawError"
