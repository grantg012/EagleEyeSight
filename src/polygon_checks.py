"""
"""

from __future__ import annotations
import sys

import xml.etree.ElementTree as ET

from unit_conversions import *
from eagle_enums import Warnings, BoardTypes, Checks
from default_rules import RULES
from results_printer import print_results


def check_polgyons(brdTree: ET, boardType: BoardTypes, correct: bool) -> list[tuple[Warnings, str]]:
    """"""
    # Get all the polygons
    # signals_node = next(brdTree.iter("signals"))  # Old version. Keep if compatibility breaks, but it's slower
    signals_node = brdTree.find("./drawing/board/signals")
    signal_nodes = signals_node.findall("signal")
    polygons = {node.attrib["name"]: node.findall("polygon") for node in signal_nodes}

    # Check their widths and isolates
    widthMin = RULES[boardType][Checks.POLYGON_WIDTH]
    widthMinThou = mm_to_thou(widthMin)
    isolateMin = RULES[boardType][Checks.POLYGON_ISOLATE]
    isolateMinThou = mm_to_thou(isolateMin)
    warnings = []
    for (signal, polys) in polygons.items():
        # Find the polygons with too small of a width, then create a message for them and correct the issue if doing so.
        width_fails = [(poly, w) for poly in polys if (w := float(poly.attrib["width"])) < widthMin]
        warnings.extend((
            Warnings.ERROR,
            f"Polygon {signal} (l{poly.attrib['layer']}) width is {mm_to_thou(w)} which is too small"
            f"for {boardType.name.title()} width ({widthMinThou} thou)."
            ) for (poly, w) in width_fails)
        if correct:
            widthMinStr = str(widthMin)
            for (poly, _) in width_fails:
                poly.attrib["width"] = widthMinStr

        # Same deal with the isolates
        isolate_fails = [(poly, i) for poly in polys if (i := float(poly.attrib["isolate"])) < isolateMin]
        warnings.extend((
            Warnings.ERROR,
            f"Polygon {signal} (l{poly.attrib['layer']}) isolate is {mm_to_thou(i)} which is too small"
            f"for {boardType.name.title()} width ({isolateMinThou} thou)."
        ) for (poly, i) in isolate_fails)
        if correct:
            isolateMinStr = str(isolateMin)
            for (poly, _) in isolate_fails:
                poly.attrib["isolate"] = isolateMinStr

    return warnings or [(Warnings.HIGH_PRIORITY_MESSAGE,
        f"All polygons have sufficient widths ({widthMinThou} thou) and isolates ({isolateMinThou} thou).")]


def main(args: list[str]):
    """Just for testing"""
    args.append("../eagle-files/CAN-Test-Board")
    brdTree = ET.parse(args[0] + ".brd")
    print_results(check_polgyons(brdTree, BoardTypes.POWER, False), Warnings.highest())


if(__name__ == "__main__"):
    main(sys.argv[1:])
