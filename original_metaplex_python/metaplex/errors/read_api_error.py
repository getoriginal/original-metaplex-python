from .metaplex_error import MetaplexError


class ReadApiError(MetaplexError):
    def __init__(self, message, cause=None):
        super().__init__(message, "rpc", None, cause)
        self.name = "ReadApiError"
