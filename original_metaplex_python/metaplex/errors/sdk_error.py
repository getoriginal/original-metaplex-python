from original_metaplex_python.metaplex.errors.metaplex_error import MetaplexError


class SdkError(MetaplexError):
    def __init__(self, message, cause=None):
        super().__init__(message, "sdk", None, cause)
        self.name = "SdkError"


class OperationHandlerMissingError(SdkError):
    def __init__(self, operation_key):
        message = (
            f"No operation handler was registered for the [{operation_key}] operation. "
            "Did you forget to register it? You may do this by using: "
            '"metaplex.operations().register(operation, operationHandler)".'
        )
        super().__init__(message)
        self.name = "OperationHandlerMissingError"


class DriverNotProvidedError(SdkError):
    def __init__(self, driver):
        message = (
            f"The SDK tried to access the driver [{driver}] but was not provided. "
            'Make sure the driver is registered by using the "setDriver(myDriver)" method.'
        )
        super().__init__(message)
        self.name = "DriverNotProvidedError"


class UnexpectedCurrencyError(SdkError):
    def __init__(self, actual, expected):
        message = (
            f"Expected currency [{expected}] but got [{actual}]. "
            "Ensure the provided Amount or Currency is of the expected type."
        )
        super().__init__(message)
        self.actual = actual
        self.expected = expected
        self.name = "UnexpectedCurrencyError"


class CurrencyMismatchError(SdkError):
    def __init__(self, left, right, operation=None):
        wrapped_operation = f" [{operation}]" if operation else ""
        message = (
            f"The SDK tried to execute an operation{wrapped_operation} on two different currencies: "
            f"{left.symbol} and {right.symbol}. "
            "Provide both amounts in the same currency to perform this operation."
        )
        super().__init__(message)
        self.left = left
        self.right = right
        self.operation = operation
        self.name = "CurrencyMismatchError"


class InvalidJsonVariableError(SdkError):
    def __init__(self, cause=None):
        super().__init__(
            "The provided JSON variable could not be parsed into a string.", cause
        )
        self.name = "InvalidJsonVariableError"


class InvalidJsonStringError(SdkError):
    def __init__(self, cause=None):
        super().__init__(
            "The provided string could not be parsed into a JSON variable.", cause
        )
        self.name = "InvalidJsonStringError"


class OperationUnauthorizedForGuestsError(SdkError):
    def __init__(self, operation):
        message = (
            f"Trying to access the [{operation}] operation as a guest. "
            "Ensure your wallet is connected using the identity driver. "
            'For instance, by using "metaplex.use(walletAdapterIdentity(wallet))" or '
            '"metaplex.use(keypairIdentity(keypair))".'
        )
        super().__init__(message)
        self.name = "OperationUnauthorizedForGuestsError"


class UninitializedWalletAdapterError(SdkError):
    def __init__(self):
        message = (
            "The current wallet adapter is not initialized. "
            "You likely have selected a wallet adapter but forgot to initialize it. "
            'You may do this by running the following asynchronous method: "wallet.connect();".'
        )
        super().__init__(message)
        self.name = "UninitializedWalletAdapterError"


class OperationNotSupportedByWalletAdapterError(SdkError):
    def __init__(self, operation):
        message = (
            f"The current wallet adapter does not support the following operation: [{operation}]. "
            "Ensure your wallet is connected using a compatible wallet adapter."
        )
        super().__init__(message)
        self.name = "OperationNotSupportedByWalletAdapterError"


class TaskIsAlreadyRunningError(SdkError):
    def __init__(self):
        message = (
            "Trying to re-run a task that hasn't completed yet. "
            'Ensure the task has completed using "await" before trying to run it again.'
        )
        super().__init__(message)
        self.name = "TaskIsAlreadyRunningError"


class AssetNotFoundError(SdkError):
    def __init__(self, location):
        super().__init__(f"The asset at [{location}] could not be found.")
        self.name = "AssetNotFoundError"


class AccountNotFoundError(SdkError):
    def __init__(self, address, account_type=None, solution=None):
        message = (
            (
                f"The account of type [{account_type}] was not found"
                if account_type
                else "No account was found"
            )
            + f" at the provided address [{address}]."
            + (f" {solution}" if solution else "")
        )
        super().__init__(message)
        self.name = "AccountNotFoundError"


class UnexpectedAccountError(SdkError):
    def __init__(self, address, expected_type, cause=None):
        message = (
            f"The account at the provided address [{address}] "
            f"is not of the expected type [{expected_type}]."
        )
        super().__init__(message, cause)
        self.name = "UnexpectedAccountError"


class UnexpectedTypeError(SdkError):
    def __init__(self, variable, actual_type, expected_type):
        message = (
            f"Expected variable [{variable}] to be "
            f"of type [{expected_type}] but got [{actual_type}]."
        )
        super().__init__(message)
        self.name = "UnexpectedTypeError"


class ExpectedSignerError(SdkError):
    def __init__(self, variable, actual_type, solution=None):
        solution_text = (
            solution
            if solution
            else "Please check that you are providing the variable as a signer. "
            "Note that, it may be allowed to provide a non-signer variable for certain use cases but not this one."
        )
        message = (
            f"Expected variable [{variable}] to be of type [Signer] but got [{actual_type}]. "
            f"{solution_text}"
        )
        super().__init__(message)
        self.name = "ExpectedSignerError"


class ProgramNotRecognizedError(SdkError):
    def __init__(self, name_or_address, cluster):
        is_name = isinstance(name_or_address, str)
        toString = name_or_address if is_name else str(name_or_address)
        message = (
            f"The provided program {'name' if is_name else 'address'} [{toString}] "
            f"is not recognized in the [{cluster}] cluster. "
            "Did you forget to register this program? "
            'If so, you may use "metaplex.programs().register(myProgram)" to fix this.'
        )
        super().__init__(message)
        self.nameOrAddress = name_or_address
        self.cluster = cluster
        self.name = "ProgramNotRecognizedError"


class NoInstructionsToSendError(SdkError):
    def __init__(self, operation, solution=None):
        message = (
            f"The input provided to the [{operation}] resulted in a Transaction containing no Instructions. "
            f"{solution or 'Ensure that the provided input has an effect on the operation. This typically happens when trying to update an account with the same data it already contains.'}"
        )
        super().__init__(message)
        self.name = "NoInstructionsToSendError"


class FailedToSerializeDataError(SdkError):
    def __init__(self, data_description, cause=None):
        message = (
            f"The received data could not be serialized as a [{data_description}]."
        )
        super().__init__(message, cause)
        self.name = "FailedToSerializeDataError"


class FailedToDeserializeDataError(SdkError):
    def __init__(self, data_description, cause=None):
        message = f"The received serialized data could not be deserialized to a [{data_description}]."
        super().__init__(message, cause)
        self.name = "FailedToDeserializeDataError"


class MissingInputDataError(SdkError):
    def __init__(self, missing_parameters, solution=None):
        message = (
            f"Some parameters are missing from the provided input object. "
            f"Please provide the following missing parameters [{', '.join(missing_parameters)}]."
            f"{f' {solution}' if solution else ''}"
        )
        super().__init__(message)
        self.name = "MissingInputDataError"


class NotYetImplementedError(SdkError):
    def __init__(self):
        message = "This feature is not yet implemented. Please check back later."
        super().__init__(message)
        self.name = "NotYetImplementedError"


class UnreachableCaseError(SdkError):
    def __init__(self, value):
        message = f"A switch statement is not handling the provided case [{value}]. Check your inputs or raise an issue to have ensure all cases are handled properly."
        super().__init__(message)
        self.name = "UnreachableCaseError"
