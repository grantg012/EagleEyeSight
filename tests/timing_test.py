"""
"""

from __future__ import annotations
import sys
import timeit

import xml.etree.ElementTree as ET


def test1(args: list[str]):
    """"""
    args.append("../eagle-files/CAN-Test-Board")
    brdTree = ET.parse(args[0] + ".brd")
    print(timeit.timeit('next(brdTree.iter("signals"))', globals = locals(), number = 10_00))
    print(timeit.timeit('brdTree.find("./drawing/board/signals")', globals = locals(), number = 10_00))


def test2(args: list[str]):
    """"""
    args.append("../eagle-files/CAN-Test-Board")
    schTree = ET.parse(args[0] + ".sch")
    def opt1():
        return schTree.find(".//parts").find("./part[@name='R4']")
    def opt2():
        return next(p for p in schTree.find(".//parts").findall("./part") if p.attrib["name"] == "R4")
    print(timeit.timeit("opt1()", globals = locals(), number = 50_000))
    print(timeit.timeit("opt2()", globals = locals(), number = 50_000))


def main(args: list[str]):
    """"""
    # test1(args)
    test2(args)


if (__name__ == "__main__"):
    main(sys.argv[1:])
