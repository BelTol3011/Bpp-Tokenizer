class CompilationWarning(Warning):
    def __init__(self, message: str, command: str):
        super().__init__(f"{message}: {command}")


class CompilationError(Exception):
    ...


def issue_warning(warning: Warning):
    warnings.warn(warning)
    sys.stderr.write("".join(traceback.format_stack()[:-1]) + "\n")


def compile_assert(unless: bool, message: str):
    if not unless:
        raise CompilationError(message)


from .classes import *
