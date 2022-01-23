"""
"""

from enum import Enum, unique, auto


class EnumIntHash(Enum):
    def __hash__(self):
        return self.value


@unique
class Warnings(EnumIntHash):
    """"""
    CORRECTION = auto()
    HIGH_PRIORITY_MESSAGE = auto()
    ERROR = auto()
    WARNING = auto()
    SUGGESTION = auto()
    MESSAGE = auto()

    def __le__(self, other):
        if isinstance(other, Warnings):
            return self.value <= other.value
        else:
            raise TypeError(f"Can't compare Warnings and {type(other)}.")

    @classmethod
    def all(cls):
        """Return the enum member that results in the most (all) messages being printed."""
        return Warnings.MESSAGE


@unique
class BoardTypes(EnumIntHash):
    """"""
    POWER = auto()
    MIXED = auto()
    LOGIC = auto()


@unique
class Checks(EnumIntHash):
    """"""
    POLYGON_WIDTH = auto()
    POLYGON_ISOLATE = auto()
    TRACE_THICKNESS = auto()
