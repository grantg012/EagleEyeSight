"""

"""

from __future__ import annotations
from typing import Iterable


def thou_to_mm(thou: float) -> float:
    """"""
    return thou * 0.0254


def mm_to_thou(mm: float) -> float:
    """"""
    return mm / 0.0254


def mm_to_in(mm: float) -> float:
    """"""
    return mm / 25.4


def in_to_mm(in_: float) -> float:
    """"""
    return in_ * 25.4


def thou_to_mm_it(thou: Iterable[float]) -> list[float]:
    """"""
    return [e * 0.0254 for e in thou]


def mm_to_thou_it(mm: Iterable[float]) -> list[float]:
    """"""
    return [e / 0.0254 for e in mm]


def mm_to_in_it(mm: Iterable[float]) -> list[float]:
    """"""
    return [e / 25.4 for e in mm]


def in_to_mm_it(ins: Iterable[float]) -> list[float]:
    """"""
    return [e * 25.4 for e in ins]
