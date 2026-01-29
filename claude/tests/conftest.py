"""
Pytest fixtures for field_calc tests.
"""

import pytest
from field_calc.core import ChargeSystem, PointCharge


@pytest.fixture
def empty_system():
    """Create an empty charge system."""
    return ChargeSystem()


@pytest.fixture
def single_charge_system():
    """Create a system with a single positive charge at the origin."""
    system = ChargeSystem()
    system.add_charge(0, 0, 0, 1e-9)  # 1 nC at origin
    return system


@pytest.fixture
def dipole_system():
    """Create a system with an electric dipole along the x-axis."""
    system = ChargeSystem()
    system.add_charge(-0.5, 0, 0, 1e-9)   # +1 nC at (-0.5, 0, 0)
    system.add_charge(0.5, 0, 0, -1e-9)   # -1 nC at (0.5, 0, 0)
    return system


@pytest.fixture
def symmetric_system():
    """Create a system with four equal charges at corners of a square."""
    system = ChargeSystem()
    system.add_charge(0, 0, 0, 1e-9)
    system.add_charge(1, 0, 0, 1e-9)
    system.add_charge(0, 1, 0, 1e-9)
    system.add_charge(1, 1, 0, 1e-9)
    return system
