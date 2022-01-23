"""
"""

from __future__ import annotations
from typing import Final

from unit_conversions import *
from eagle_enums import BoardTypes, Checks

# All units are listed in thou(mil) and converted to mm

RULES: Final = {
    BoardTypes.POWER: {
        Checks.POLYGON_WIDTH: thou_to_mm(30),
        Checks.POLYGON_ISOLATE: thou_to_mm(30),
        Checks.TRACE_THICKNESS: thou_to_mm(10),
    },
    BoardTypes.MIXED: {
        Checks.POLYGON_WIDTH: thou_to_mm(30),
        Checks.POLYGON_ISOLATE: thou_to_mm(30),
        Checks.TRACE_THICKNESS: thou_to_mm(10),
    },
    BoardTypes.LOGIC: {
        Checks.POLYGON_WIDTH: thou_to_mm(16),
        Checks.POLYGON_ISOLATE: thou_to_mm(16),
        Checks.TRACE_THICKNESS: thou_to_mm(8),
    }
}