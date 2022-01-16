"""

"""

from __future__ import annotations
import sys

from eagle_enums import Warnings


def print_results(results: list[tuple[Warnings, str]], level) -> None:
    """"""
    for (warn, msg) in filter(lambda r: r[0] <= level, results):
        print(f"{warn.name.title()}: {msg}")


def main(args: list[str]):
    """"""
    results = [
        (Warnings.CORRECTION, "This is a correction"),
        (Warnings.ERROR, "This is an error"),
        (Warnings.WARNING, "This is a warning"),
        (Warnings.SUGGESTION, "This is a suggestion"),
        (Warnings.MESSAGE, "This is a message"),
    ]
    print_results(results, Warnings.WARNING)


if (__name__ == "__main__"):
    main(sys.argv[1:])
