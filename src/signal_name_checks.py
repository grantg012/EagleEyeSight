"""
"""

from __future__ import annotations
import sys
from typing import Final

import xml.etree.ElementTree as ET

from eagle_enums import Warnings
from results_printer import print_results

POWER_VOLTAGES_DECIMAL: Final = [1.8, 3.3]
POWER_VOLTAGES_INTEGER: Final = [5, 12, 18, 24, 48]


def level_dec_to_voltage_names(level: float) -> set[str]:
    """"""
    results = [f"{level}".replace('.', 'V'), f"+{level}".replace('.', 'V'), f"{level}V", f"+{level}V"]
    return set(results + [s.lower() for s in results])


def level_int_to_voltage_names(level: int) -> set[str]:
    """"""
    return {f"{level}V", f"+{level}V", f"{level}v", f"+{level}v"}


def _check_signal_name(warnings: list[tuple[Warnings, str]], voltages: list, net_names: list[str], net_nodes: list[ET], correct: bool) -> None:
    """"""
    for voltage in voltages:
        voltage_names = level_dec_to_voltage_names(voltage)
        found_names = [n for n in net_names if n in voltage_names]
        if len(found_names) > 1:
            warnings.append((Warnings.ERROR,
                f"Voltage net for {voltage}V has multiple names ({found_names})."
            ))
            if correct:
                correct_name = next(iter(set(voltage_names)))
                for node in net_nodes:
                    if (name := node.attrib["name"]) in voltage_names and name != correct_name:
                        node.attrib["name"] = correct_name


def check_signal_names(schTree: ET, brdTree: ET, correct: bool) -> list[tuple[Warnings, str]]:
    """"""
    # Get all the net names
    # net_nodes = next(brdTree.iter("signals"))  # Old version. Keep if compatibility breaks, but it's slower
    nets_node = schTree.find("drawing/schematic/sheets/sheet/nets")  # TODO: double check there's only ever one 'nets' node
    net_nodes = nets_node.findall("net")
    net_names = [n.attrib["name"] for n in net_nodes]

    # Check the voltages with and without a decimal
    warnings = []
    _check_signal_name(warnings, POWER_VOLTAGES_INTEGER, net_names, net_nodes, correct)
    _check_signal_name(warnings, POWER_VOLTAGES_DECIMAL, net_names, net_nodes, correct)

    return warnings or [(Warnings.HIGH_PRIORITY_MESSAGE, "All voltage names appear consistent without duplicates.")]


def main(args: list[str]):
    """Just for testing"""
    args.append("../eagle-files/CAN-Test-Board")
    schTree = ET.parse(args[0] + ".sch")
    brdTree = ET.parse(args[0] + ".brd")
    print_results(check_signal_names(schTree, brdTree, True), Warnings.highest())


if(__name__ == "__main__"):
    main(sys.argv[1:])
