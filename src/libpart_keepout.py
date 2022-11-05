"""
Check that footprints in a library part file have keepout polygons
"""

from __future__ import annotations
from itertools import chain
import sys

import xml.etree.ElementTree as ET

from eagle_enums import Warnings
from results_printer import print_results


def check_keepout_present_board(brdTree: ET) -> list[tuple[Warnings, str]]:
    """"""
    libraries_node = brdTree.find("./drawing/board/libraries")
    library_nodes = libraries_node.findall("library")
    warnings = []

    # Find all the pads on the library that have nothing on the keepout layer
    for lib_node in library_nodes:
        for package_node in lib_node.findall(".//package"):
            if not (package_node.findall("wire[@layer='39']") or package_node.findall("smd[@layer='40']")):
                warnings.append((Warnings.WARNING, f"Library {lib_node.attrib['name']} package {package_node.attrib['name']} is missing a keepout polygon (layers 39 and 40)."))
    return warnings or [(Warnings.HIGH_PRIORITY_MESSAGE, "All libraries have footprints with keepout polygons.")]


def main(args: list[str]):
    """Just for testing"""
    args.append("../eagle-files/CAN-Test-Board")
    brdTree = ET.parse(args[0] + ".brd")
    print_results(check_keepout_present_board(brdTree), Warnings.all())
    with open("../eagle-files/test.brd", 'wb') as brdFile:
        brdFile.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE eagle SYSTEM "eagle.dtd">\n'.encode('utf8'))
        brdTree.write(brdFile, "utf-8")


if(__name__ == "__main__"):
    sys.exit(main(sys.argv[1:]))
