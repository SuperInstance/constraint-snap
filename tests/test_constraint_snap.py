"""Tests for constraint-snap."""
import pytest
from constraint_snap import ConstraintSnap, Constraint


def test_snap_within_range():
    cs = ConstraintSnap()
    cs.add(Constraint("speed", 0, 100))
    result = cs.snap(50)
    assert result.snapped == 50
    assert result.feasible


def test_snap_clamps_high():
    cs = ConstraintSnap()
    cs.add(Constraint("speed", 0, 60))
    result = cs.snap(75)
    assert result.snapped == 60


def test_snap_clamps_low():
    cs = ConstraintSnap()
    cs.add(Constraint("temp", 32, 212))
    result = cs.snap(20)
    assert result.snapped == 32


def test_overlapping_constraints():
    cs = ConstraintSnap()
    cs.add(Constraint("max_speed", 0, 100))
    cs.add(Constraint("safe_speed", 0, 60))
    result = cs.snap(75)
    assert result.snapped == 60  # tighter constraint wins


def test_feasible_range():
    cs = ConstraintSnap()
    cs.add(Constraint("a", 0, 100))
    cs.add(Constraint("b", 20, 80))
    lo, hi = cs.feasible_range()
    assert lo == 20 and hi == 80


def test_conflicts_detected():
    cs = ConstraintSnap()
    cs.add(Constraint("x", 0, 10))
    cs.add(Constraint("y", 20, 30))
    conflicts = cs.conflicts()
    assert len(conflicts) == 1


def test_no_violation():
    c = Constraint("ok", 0, 10)
    assert c.contains(5)
    assert c.distance(5) == 0.0
