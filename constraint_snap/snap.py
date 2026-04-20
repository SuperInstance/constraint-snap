"""Geometric constraint snapping engine."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Constraint:
    """A constraint on a value: must be within [lo, hi]."""
    name: str
    lo: float
    hi: float
    weight: float = 1.0
    hard: bool = True  # hard constraints can't be violated
    
    def contains(self, value: float) -> bool:
        return self.lo <= value <= self.hi
    
    def distance(self, value: float) -> float:
        if self.contains(value):
            return 0.0
        if value < self.lo:
            return self.lo - value
        return value - self.hi
    
    def snap(self, value: float) -> float:
        if value < self.lo:
            return self.lo
        if value > self.hi:
            return self.hi
        return value


@dataclass
class SnapResult:
    """Result of a snap operation."""
    original: float
    snapped: float
    violations: List[str] = field(default_factory=list)
    total_distance: float = 0.0
    feasible: bool = True


class ConstraintSnap:
    """Resolve overlapping constraints and snap to feasible points.
    
    Usage:
        cs = ConstraintSnap()
        cs.add(Constraint("speed", 0.0, 100.0))
        cs.add(Constraint("safe_speed", 0.0, 60.0))
        result = cs.snap(75.0)  # snaps to 60.0 (safe_speed violated)
    """
    
    def __init__(self):
        self.constraints: List[Constraint] = []
    
    def add(self, constraint: Constraint) -> "ConstraintSnap":
        self.constraints.append(constraint)
        return self
    
    def remove(self, name: str) -> bool:
        before = len(self.constraints)
        self.constraints = [c for c in self.constraints if c.name != name]
        return len(self.constraints) < before
    
    def snap(self, value: float) -> SnapResult:
        """Snap a single value to satisfy all constraints."""
        violations = []
        current = value
        total_dist = 0.0
        
        # Sort by weight (highest priority first)
        sorted_c = sorted(self.constraints, key=lambda c: -c.weight)
        
        for c in sorted_c:
            if not c.contains(current):
                dist = c.distance(current)
                total_dist += dist
                snapped = c.snap(current)
                
                if c.hard:
                    violations.append(c.name)
                    current = snapped
        
        return SnapResult(
            original=value,
            snapped=current,
            violations=violations,
            total_distance=round(total_dist, 6),
            feasible=len(violations) == 0,
        )
    
    def snap_multi(self, values: Dict[str, float]) -> Dict[str, SnapResult]:
        """Snap multiple named values."""
        return {name: self.snap(val) for name, val in values.items()}
    
    def feasible_range(self) -> Tuple[float, float]:
        """Find the intersection of all hard constraints."""
        if not self.constraints:
            return (float('-inf'), float('inf'))
        
        hard = [c for c in self.constraints if c.hard]
        if not hard:
            return (float('-inf'), float('inf'))
        
        lo = max(c.lo for c in hard)
        hi = min(c.hi for c in hard)
        
        return (lo, hi) if lo <= hi else (0.0, 0.0)  # infeasible
    
    def is_feasible(self) -> bool:
        lo, hi = self.feasible_range()
        return lo <= hi
    
    def conflicts(self) -> List[Tuple[str, str]]:
        """Find conflicting constraint pairs."""
        conflicts = []
        for i, a in enumerate(self.constraints):
            for b in self.constraints[i+1:]:
                if a.hard and b.hard:
                    lo = max(a.lo, b.lo)
                    hi = min(a.hi, b.hi)
                    if lo > hi:
                        conflicts.append((a.name, b.name))
        return conflicts
