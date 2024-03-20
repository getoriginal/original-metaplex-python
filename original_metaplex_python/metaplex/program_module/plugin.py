from original_metaplex_python.metaplex.program_module.program_client import (
    ProgramClient,
)


def program_module():
    def install(metaplex):
        program_client = ProgramClient(metaplex)
        metaplex.programs = lambda: program_client

    return install
