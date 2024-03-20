from original_metaplex_python.metaplex.errors.sdk_error import ProgramNotRecognizedError


class ProgramClient:
    """
    Group: Modules
    """

    def __init__(self, metaplex):
        self.metaplex = metaplex
        self.programs = []

    def register(self, program):
        self.programs.insert(0, program)

    def all(self, overrides=None):
        overrides = overrides if overrides is not None else []
        return overrides + self.programs

    def all_for_cluster(self, cluster, overrides=None):
        overrides = overrides if overrides is not None else []
        all_programs = self.all(overrides)

        for i in range(len(all_programs) - 1, -1, -1):
            program = all_programs[i]
            if callable(
                getattr(program, "cluster_filter", None)
            ) and not program.cluster_filter(cluster):
                all_programs.pop(i)

        return all_programs

    def all_for_current_cluster(self, overrides=None):
        overrides = overrides if overrides is not None else []
        return self.all_for_cluster(self.metaplex.cluster, overrides)

    def get(self, name_or_address, overrides=None):
        overrides = overrides if overrides is not None else []
        programs = self.all_for_current_cluster(overrides)

        program = next(
            (
                program
                for program in programs
                if (
                    program.name == name_or_address
                    if isinstance(name_or_address, str)
                    else program.address.equals(name_or_address)
                )
            ),
            None,
        )

        if program is None:
            raise ProgramNotRecognizedError(name_or_address, self.metaplex.cluster)

        return program
