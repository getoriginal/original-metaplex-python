from .metaplex_error import MetaplexError


class ProgramError(MetaplexError):
    def __init__(self, message, program, cause=None, logs=None):
        super().__init__(
            message, "program", f"{program.name} [{program.address}]", cause
        )
        self.name = "ProgramError"
        self.program = program
        self.logs = logs
        if logs:
            log_str = "\n".join(f"| {log}" for log in logs)
            self.message += f"\nProgram Logs:\n{log_str}\n"


class ParsedProgramError(ProgramError):
    def __init__(self, program, cause, logs):
        of_code = f" of code [{cause.code}]" if cause.code else ""
        message = (
            f"The program [{program.name}] at address [{program.address}] "
            f'raised an error{of_code} that translates to "{cause.message}".'
        )
        super().__init__(message, program, cause, logs)
        self.name = "ParsedProgramError"


class UnknownProgramError(ProgramError):
    def __init__(self, program, cause):
        of_code = f" of code [{cause.code}]" if cause.code else ""
        message = (
            f"The program [{program.name}] at address [{program.address}] "
            f"raised an error{of_code} that is not recognized by the programs registered on the SDK. "
            "Please check the underlying program error below for more details."
        )
        super().__init__(message, program, cause, cause.logs)
        self.name = "UnknownProgramError"
