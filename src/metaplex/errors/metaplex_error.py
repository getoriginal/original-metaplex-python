from enum import Enum


class MetaplexErrorSource(Enum):
    SDK = "sdk"
    NETWORK = "network"
    RPC = "rpc"
    PLUGIN = "plugin"
    PROGRAM = "program"


class MetaplexError(Exception):
    def __init__(
        self, message, source: MetaplexErrorSource, source_details=None, cause=None
    ):
        super().__init__(message)
        self.name = "MetaplexError"
        self.source = source
        self.source_details = source_details
        self.cause = cause
        self.message = (
            f"{message}\n\nSource: {self.get_full_source()}"
            + (f"\n\nCaused By: {cause}" if cause else "")
            + "\n"
        )

    def get_capitalized_source(self):
        if self.source in [MetaplexErrorSource.SDK, MetaplexErrorSource.RPC]:
            return self.source.upper()

        return self.source[0].upper() + self.source[1:]

    def get_full_source(self):
        capitalized_source = self.get_capitalized_source()
        source_details = f" > {self.source_details}" if self.source_details else ""

        return capitalized_source + source_details

    def __str__(self):
        return f"[{self.name}] {self.message}"
