from enum import IntEnum, auto


class Verbosity(IntEnum):
    error = auto()
    warning = auto()
    info = auto()
    debug = auto()

    def at_level(self, level):
        return self >= level
