"""
"""

from __future__ import annotations
import sys
import timeit

import xml.etree.ElementTree as ET


def main(args: list[str]):
    """"""
    args.append("../eagle-files/CAN-Test-Board")
    brdTree = ET.parse(args[0] + ".brd")
    print(timeit.timeit('next(brdTree.iter("signals"))', globals = locals(), number = 10_00))
    print(timeit.timeit('brdTree.find("./drawing/board/signals")', globals = locals(), number = 10_00))


if (__name__ == "__main__"):
    main(sys.argv[1:])
