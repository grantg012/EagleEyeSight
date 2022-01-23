"""
"""

from __future__ import annotations
import sys

import xml.etree.ElementTree as ET

from unit_conversions import *
from eagle_enums import Warnings, BoardTypes, Checks
from default_rules import RULES
from results_printer import print_results


def check_trace_widths(brdTree: ET, schTree: ET, boardType: BoardTypes, correct: bool) -> list[tuple[Warnings, str]]:
    """"""
    warnings = []
    boardName = boardType.name.title()
    minThick = RULES[boardType][Checks.TRACE_THICKNESS]  # mm
    minThickStr = str(round(minThick, 4))
    minThickThou = mm_to_thou(minThick)

    # First check all net classes (esp the default) have a thick enough width
    classes = brdTree.find(".//classes").findall("class")
    schClasses = None
    for c in classes:
        class_width = float(c.attrib["width"])
        if class_width < minThick:
            warnings.append((Warnings.ERROR,
                f"Net class {c.attrib['name']} has a trace width of {mm_to_thou(class_width)} thou which is too this for a {boardName} ({minThickThou} thou)."
            ))
            if correct:
                if not schClasses:
                    schClasses = schTree.find(".//classes")
                c.attrib["width"] = minThickStr
                schClasses.find(f"class[@name='{c.attrib['name']}']").attrib["width"] = minThickStr

    # Then check all traces
    msg_template = f"Trace for {'{}'} is {'{}'} thou which is too thin for a {boardName} board's minimum {minThickThou} thou."
    for signal in brdTree.findall("./drawing/board/signals/signal"):
        for wire in signal.findall("wire"):
            if 1 <= int(wire.attrib["layer"]) <= 16:
                if (width := float(wire.attrib["width"])) < minThick:
                    warnings.append((Warnings.ERROR,
                        msg_template.format(signal.attrib['name'], mm_to_thou(width))
                    ))
                    if correct:
                        wire.attrib["width"] = minThickStr
                    else:
                        break  # Only need one message per trace

    return warnings or [(Warnings.ERROR,
        f"All traces on this {boardName} board have sufficient minimum thickness ({mm_to_thou(minThick)} thou).")
    ]


def main(args: list[str]):
    """Just for testing"""
    # args.append("../eagle-files/test")
    args.append("../eagle-files/CAN-Test-Board")
    names = (args[0] + ".sch", (args[0] + ".brd"))
    schTree = ET.parse(names[0])
    brdTree = ET.parse(names[1])
    correct = True
    print_results(check_trace_widths(brdTree, schTree, BoardTypes.POWER, correct), Warnings.all())
    if correct:
        # schTree.write("../eagle-files/test.sch", xml_declaration = True, encoding = "utf-8")
        # brdTree.write("../eagle-files/test.brd", xml_declaration = True, encoding = "utf-8")

        with open("../eagle-files/test.sch", 'w', encoding = "utf-8") as schFile:
            schFile.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE eagle SYSTEM "eagle.dtd">\n')
            schTree.write(schFile, encoding = "unicode")
        with open("../eagle-files/test.brd", 'w', encoding = "utf-8") as brdFile:
            brdFile.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE eagle SYSTEM "eagle.dtd">\n')
            brdTree.write(brdFile, encoding = "unicode")


if __name__ == "__main__":
    main(sys.argv[1:])
