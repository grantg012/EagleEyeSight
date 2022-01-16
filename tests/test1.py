"""

"""

from __future__ import annotations
import sys

import xml.etree.ElementTree as ET

# iter - any depth
# find - just direct children


def main(args: list[str]):
    """"""
    path = "eagle-files/CAN-Test-Board"
    schPath = path + ".sch"
    brdPath = path + "brd"
    print(brdPath)


if(__name__ == "__main__"):
    main(sys.argv[1:])
