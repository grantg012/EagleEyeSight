"""
Check that footprints in a library part file either have the stop property turned
on for pads & smds or have a polygon on that area
"""

from __future__ import annotations
from itertools import chain
import sys
from typing import Final

import xml.etree.ElementTree as ET

from eagle_enums import Warnings
from results_printer import print_results


def check_stop_present_board(brdTree: ET) -> list[tuple[Warnings, str]]:
    """"""
    libraries_node = brdTree.find("./drawing/board/libraries")
    library_nodes = libraries_node.findall("library")

    # Find all the pads on the library that have the stop layer turned off
    no_stop_nodes: dict["Package", list[tuple["Pad", str]]] = {}
    for lib_node in library_nodes:
        for package_node in lib_node.findall(".//package"):
            for pad_node in chain(package_node.findall("pad[@stop='no']"), package_node.findall("smd[@stop='no']")):
                if package_node not in no_stop_nodes:
                    no_stop_nodes[package_node] = []
                no_stop_nodes[package_node].append((pad_node, lib_node.attrib["name"]))

    # See if there's a manual circle present for the stop layer and warn accordingly.
    warnings = []
    for (package_node, no_stop_list) in no_stop_nodes.items():
        nMissingFull = nUsingPoly = nOnlyOnePoly = 0
        lib_name_scope = ''
        for (no_stop_node, lib_name) in no_stop_list:
            lib_name_scope = lib_name
            x = no_stop_node.attrib['x']; y = no_stop_node.attrib['y']
            circles_top = package_node.findall(f"circle[@layer='29'][@x='{x}'][@y='{y}']")
            circles_bottom = package_node.findall(f"circle[@layer='30'][@x='{x}'][@y='{y}']")
            if circles_top:
                if circles_bottom:
                    nUsingPoly += 1
                else:
                    nOnlyOnePoly += 1
            else:
                if circles_bottom:
                    nOnlyOnePoly += 1
                else:
                    nMissingFull += 1
        warnings.append((Warnings.ERROR,
                         f"Library {lib_name_scope} package {package_node.attrib['name']} has "
                         f"{nMissingFull} pad/smd(s) with stop turned off (soldermask over the copper), "
                         f"{nOnlyOnePoly} pad/smd(s) with stop off but one polygon on a stop layer (29 and 30), "
                         f"and {nUsingPoly} pad/smd(s) with stop off but polygons on both stop layers"))
    return warnings or [(Warnings.HIGH_PRIORITY_MESSAGE, "All libraries have footprints with stop set or polygons present.")]


def main(args: list[str]):
    """Just for testing"""
    args.append("../eagle-files/CAN-Test-Board")
    brdTree = ET.parse(args[0] + ".brd")
    print_results(check_stop_present_board(brdTree), Warnings.all())
    with open("../eagle-files/test.brd", 'wb') as brdFile:
        brdFile.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE eagle SYSTEM "eagle.dtd">\n'.encode('utf8'))
        brdTree.write(brdFile, "utf-8")


if (__name__ == "__main__"):
    sys.exit(main(sys.argv[1:]))
