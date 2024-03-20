from solders import system_program as lib_system_program

from original_metaplex_python.metaplex.system_module.system_client import SystemClient
from original_metaplex_python.metaplex.types.program import Program

system_program: Program = Program()
system_program.name = "SystemProgram"
system_program.address = lib_system_program.ID


def system_module():
    def install(metaplex):
        metaplex.programs().register(system_program)
        metaplex.programs().get_system = lambda programs: metaplex.programs().get(
            system_program.name, programs
        )
        system_client = SystemClient(metaplex)
        metaplex.system = lambda: system_client

    return install
