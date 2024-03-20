import json

from .metaplex_error import MetaplexError


class RpcError(MetaplexError):
    def __init__(self, message, cause=None):
        super().__init__(message, "rpc", None, cause)
        self.name = "RpcError"


class FailedToSendTransactionError(RpcError):
    def __init__(self, cause):
        message = (
            "The transaction could not be sent successfully to the network. "
            "Please check the underlying error below for more details."
        )
        super().__init__(message, cause)
        self.name = "FailedToSendTransactionError"

        if self.error_logs:
            log_str = "\n".join(f"| {log}" for log in self.error_logs)
            self.message += f"\nProgram Logs:\n{log_str}\n"

    @property
    def as_send_transaction_error(self):
        # Assuming cause is an instance of SendTransactionError or has similar attributes
        return self.cause

    @property
    def error(self):
        return self.as_send_transaction_error.message

    @property
    def error_logs(self):
        return getattr(self.as_send_transaction_error, "logs", [])


class FailedToConfirmTransactionError(RpcError):
    def __init__(self, cause):
        message = (
            "The transaction could not be confirmed. "
            "Please check the underlying error below for more details."
        )
        super().__init__(message, cause)
        self.name = "FailedToConfirmTransactionError"


class FailedToConfirmTransactionWithResponseError(FailedToConfirmTransactionError):
    def __init__(self, response):
        def get_message(error):
            if not error:
                return "Unknown error"
            if isinstance(error, str):
                return error
            try:
                return json.dumps(error)
            except Exception:
                return "Unknown error"

        message = get_message(response.value.err)
        super().__init__(message)
        self.name = "FailedToConfirmTransactionWithResponseError"
        self.response = response

    @property
    def error(self):
        return getattr(self.response.value, "err", "Unknown error")
