# constraint-snap

Geometric constraint snapping. Define ranges, snap values to satisfy all constraints, detect conflicts. Like snapping to a grid, but for behavior spaces.

## Usage

```python
from constraint_snap import ConstraintSnap, Constraint

cs = ConstraintSnap()
cs.add(Constraint("max_speed", 0, 100))
cs.add(Constraint("safe_speed", 0, 60))

result = cs.snap(75)
# snapped=60, violations=["safe_speed"], feasible=False (was clamped)

lo, hi = cs.feasible_range()  # (0, 60) — intersection
conflicts = cs.conflicts()    # [] — no impossible pairs
```

Zero deps. `pip install constraint-snap`
