
class ANSIColors:
    """
    Classe com `sequências de scape` ANSI que formatam a saída no terminal.
    """    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def header(cls, string: str) -> str:
        return f'{cls.HEADER}{string}{cls.ENDC}'

    @classmethod
    def okblue(cls, string: str) -> str:
        return f'{cls.OKBLUE}{string}{cls.ENDC}'

    @classmethod
    def okcyan(cls, string: str) -> str:
        return f'{cls.OKCYAN}{string}{cls.ENDC}'

    @classmethod
    def okgreen(cls, string: str) -> str:
        return f'{cls.OKGREEN}{string}{cls.ENDC}'

    @classmethod
    def warning(cls, string: str) -> str:
        return f'{cls.WARNING}{string}{cls.ENDC}'

    @classmethod
    def fail(cls, string: str) -> str:
        return f'{cls.FAIL}{string}{cls.ENDC}'

    @classmethod
    def bold(cls, string: str) -> str:
        return f'{cls.BOLD}{string}{cls.ENDC}'

    @classmethod
    def underline(cls, string: str) -> str:
        return f'{cls.UNDERLINE}{string}{cls.ENDC}'
