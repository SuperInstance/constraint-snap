"""constraint-snap — Geometric constraint snapping.

Snap values to valid ranges, resolve overlapping constraints,
find the nearest feasible point. Like snapping to a grid, but for behavior.
"""
__version__ = "0.1.0"
from .snap import ConstraintSnap, Constraint, SnapResult
__all__ = ["ConstraintSnap", "Constraint", "SnapResult"]
