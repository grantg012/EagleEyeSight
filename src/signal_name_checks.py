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


def remove_middle_node(parent: ET, target_node: ET) -> list[ET]:
    """"""
    children = target_node.findall("./*")
    for c in children:
        target_node.remove(c)
    parent.remove(target_node)
    return children


def transfer_nets(nodes: list[ET], correct_name: str, voltage_names: set[str], parent: ET):
    """"""
    correct_node = None
    children = []
    for node in nodes:
        if (name := node.attrib["name"]) == correct_name:
            correct_node = node
        elif name in voltage_names:
            children.append(remove_middle_node(parent, node))
    assert correct_node is not None
    assert children
    for childrenList in children:
        correct_node.extend(childrenList)


def _check_signal_name(warnings: list[tuple[Warnings, str]], voltages: list, net_names: list[str],
                       net_nodes: list[ET], nets_node: ET, brdTree: ET, correct: bool) -> None:
    """"""
    signals_node = signal_nodes = None
    for voltage in voltages:
        voltage_names = level_dec_to_voltage_names(voltage)
        found_names = [n for n in net_names if n in voltage_names]
        if len(found_names) > 1:
            warnings.append((Warnings.ERROR,
                f"Voltage net for {voltage}V has multiple names ({found_names})."
            ))
            if correct:
                if not signals_node:
                    signal_nodes = brdTree.find("./drawing/board/signals").findall("signal")
                correct_name = next(iter(voltage_names))
                transfer_nets(net_nodes, correct_name, voltage_names, nets_node)
                transfer_nets(signal_nodes, correct_name, voltage_names, signals_node)
                # TODO: append to message that the correction happened


def check_signal_names(schTree: ET, brdTree: ET, correct: bool) -> list[tuple[Warnings, str]]:
    """"""
    # Get all the net names
    # net_nodes = next(brdTree.iter("signals"))  # Old version. Keep if compatibility breaks, but it's slower
    nets_node = schTree.find("drawing/schematic/sheets/sheet/nets")  # TODO: double check there's only ever one 'nets' node
    net_nodes = nets_node.findall("net")
    net_names = [n.attrib["name"] for n in net_nodes]

    # Check the voltages with and without a decimal
    warnings = []
    _check_signal_name(warnings, POWER_VOLTAGES_INTEGER, net_names, net_nodes, nets_node, brdTree, correct)
    _check_signal_name(warnings, POWER_VOLTAGES_DECIMAL, net_names, net_nodes, nets_node, brdTree, correct)

    return warnings or [(Warnings.HIGH_PRIORITY_MESSAGE, "All voltage names appear consistent without duplicates.")]


def main(args: list[str]):
    """Just for testing"""
    args.append("../eagle-files/CAN-Test-Board")
    names = (args[0] + ".sch", (args[0] + ".brd"))
    schTree = ET.parse(names[0])
    brdTree = ET.parse(names[1])
    correct = True
    print_results(check_signal_names(schTree, brdTree, correct), Warnings.all())
    if correct:
        schTree.write("../eagle-files/test.sch")
        brdTree.write("../eagle-files/test.brd")


if(__name__ == "__main__"):
    main(sys.argv[1:])
