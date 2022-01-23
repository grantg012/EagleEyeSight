"""
"""

from __future__ import annotations
import math
import sys
from typing import Final

import xml.etree.ElementTree as ET

from eagle_enums import Warnings
from results_printer import print_results
from unit_conversions import *


GRID_BASE: Final = 0.1


def is_grid_multiple(number: float) -> bool:
    """"""
    return math.isclose(multiplied := number / GRID_BASE, round(multiplied))


def almost_eq_coords(x1: float, y1: float, x2: float, y2: float) -> bool:
    """"""
    return math.isclose(x1, x2, abs_tol = 0.001) and math.isclose(y1, y2, abs_tol = 0.001)


def check_schematic_alignment(schTree: ET, correct: bool) -> list[tuple[Warnings, str]]:
    """"""
    warnings = []
    # First, check what the grid is configured to.
    gridNode = schTree.find(".//grid")
    gridSize = float(gridNode.attrib["distance"])
    goodGrid = (math.isclose(gridSize, GRID_BASE) or is_grid_multiple(gridSize)) and \
        gridNode.attrib["unitdist"] == gridNode.attrib["unit"] == "inch"
    if not goodGrid:
        warnings.append((Warnings.WARNING, "Grid alignment is not 0.1 inches or a multiple of it."))
        if correct:
            gridNode.attrib["distance"] = str(GRID_BASE)
            gridNode.attrib["unitdist"] = gridNode.attrib["unit"] = "inch"

    # Second, check all the symbols in the schematic
    instance_nodes = schTree.findall(".//instances/instance")
    segment_nodes = libraries_node = parts_node = None
    for inst in instance_nodes:
        x = mm_to_in(x_mm := float(inst.attrib['x']))
        y = mm_to_in(y_mm := float(inst.attrib['y']))
        if not (is_grid_multiple(x) and is_grid_multiple(y)):
            instName = inst.attrib["part"]
            warnings.append((Warnings.SUGGESTION, f"Component {instName} is not aligned to a {GRID_BASE} in grid ({x:.2f}, {y:.2f})."))
            if correct:
                # Move the symbol itself
                newX_mm = round(in_to_mm(round(x, 1)), 4); newY_mm = round(in_to_mm(round(y, 1)), 4)
                xMov_mm = newX_mm - x_mm; yMov_mm = newY_mm - y_mm
                inst.attrib['x'] = str(newX_mm)
                inst.attrib['y'] = str(newY_mm)

                # Move all the net segments it's connected to
                # First get the nodes we need if we haven't already
                if not segment_nodes:
                    segment_nodes = schTree.findall(".//nets//segment")
                    libraries_node = schTree.find(".//libraries")
                    parts_node = schTree.find(".//parts")
                # Next find the symbol that was used and the coordinates of its pins
                gate_name = inst.attrib["gate"]
                part = parts_node.find(f"./part[@name='{instName}']")
                library = libraries_node.find(f"./library[@name='{part.attrib['library']}']")
                deviceset = library.find(f".//deviceset[@name='{part.attrib['deviceset']}']")
                gate_symbol = deviceset.find(f"./gates/gate[@name='{gate_name}']").attrib["symbol"]
                symbol = library.find(f".//symbol[@name='{gate_symbol}']")
                symbol_pins = symbol.findall("./pin")
                pin_coords = {p.attrib["name"]: (x_mm + float(p.attrib['x']), y_mm + float(p.attrib['y'])) for p in symbol_pins}
                # Lastly, check all segments that use this pin to see if any of the segments wires connect to that pin
                for (seg, pr) in [(s, pr) for s in segment_nodes if (pr := s.findall(f"./pinref[@part='{instName}'][@gate='{gate_name}']"))]:
                    ref_pin_coords = [pin_coords[p.attrib["pin"]] for p in pr]
                    for (x_pin, y_pin) in ref_pin_coords:
                        for wire in seg.findall("wire"):
                            # If a wire end matches the pin, move it like the pin was moved.
                            if almost_eq_coords(x1 := float(wire.attrib['x1']), y1 := float(wire.attrib['y1']), x_pin, y_pin):
                                wire.attrib['x1'] = str(round(x1 + xMov_mm, 3))
                                wire.attrib['y1'] = str(round(y1 + yMov_mm, 3))
                            elif almost_eq_coords(x2 := float(wire.attrib['x2']), y2 := float(wire.attrib['y2']), x_pin, y_pin):
                                wire.attrib['x2'] = str(round(x2 + xMov_mm, 3))
                                wire.attrib['y2'] = str(round(y2 + yMov_mm, 3))

    return warnings or [(Warnings.SUGGESTION, f"All schematic items are aligned on a {GRID_BASE} inch grid.")]


def main(args: list[str]):
    """Just for testing"""
    # args.append("../eagle-files/test")
    args.append("../eagle-files/CAN-Test-Board")
    names = (args[0] + ".sch", (args[0] + ".brd"))
    schTree = ET.parse(names[0])
    brdTree = ET.parse(names[1])
    correct = False
    print_results(check_schematic_alignment(schTree, correct), Warnings.all())
    if correct:
        schTree.write("../eagle-files/test.sch")
        brdTree.write("../eagle-files/test.brd")


if (__name__ == "__main__"):
    main(sys.argv[1:])
