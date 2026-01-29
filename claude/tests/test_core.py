"""
Tests for the core module of field_calc.

This module tests:
- PointCharge class functionality
- ChargeSystem class functionality
- Electric field calculations
- Electric potential calculations
- Edge cases and error handling
"""

import pytest
import math
from field_calc.core import ChargeSystem, PointCharge, K, EPSILON_0,calculate_field,calculate_potential


class TestPointCharge:
    """Tests for the PointCharge class."""
    
    def test_create_point_charge(self):
        """Test creating a point charge with valid parameters."""
        charge = PointCharge(x=1.0, y=2.0, z=3.0, q=1e-9, charge_id=1)
        assert charge.x == 1.0
        assert charge.y == 2.0
        assert charge.z == 3.0
        assert charge.q == 1e-9
        assert charge.charge_id == 1
    
    def test_point_charge_position(self):
        """Test the position method returns correct tuple."""
        charge = PointCharge(x=1.0, y=2.0, z=3.0, q=1e-9, charge_id=1)
        assert charge.position() == (1.0, 2.0, 3.0)
    
    def test_point_charge_distance_to(self):
        """Test distance calculation from charge to a point."""
        charge = PointCharge(x=0, y=0, z=0, q=1e-9, charge_id=1)
        
        # Distance to (1, 0, 0) should be 1
        assert charge.distance_to(1, 0, 0) == pytest.approx(1.0)
        
        # Distance to (3, 4, 0) should be 5 (3-4-5 triangle)
        assert charge.distance_to(3, 4, 0) == pytest.approx(5.0)
        
        # Distance to (1, 1, 1) should be sqrt(3)
        assert charge.distance_to(1, 1, 1) == pytest.approx(math.sqrt(3))
    
    def test_point_charge_str(self):
        """Test string representation of point charge."""
        charge = PointCharge(x=1.0, y=2.0, z=0.0, q=1e-9, charge_id=1)
        str_repr = str(charge)
        assert "id=1" in str_repr
        assert "1.0" in str_repr
        assert "2.0" in str_repr
        assert "1.00e-09" in str_repr


class TestChargeSystemBasic:
    """Basic tests for ChargeSystem class."""
    
    def test_create_empty_system(self, empty_system):
        """Test creating an empty charge system."""
        assert empty_system.charge_count() == 0
        assert empty_system.list_charges() == []
    
    def test_add_single_charge(self, empty_system):
        """Test adding a single charge."""
        charge_id = empty_system.add_charge(1, 2, 3, 1e-9)
        assert charge_id == 1
        assert empty_system.charge_count() == 1
    
    def test_add_multiple_charges(self, empty_system):
        """Test adding multiple charges."""
        id1 = empty_system.add_charge(0, 0, 0, 1e-9)
        id2 = empty_system.add_charge(1, 0, 0, -1e-9)
        id3 = empty_system.add_charge(0, 1, 0, 2e-9)
        
        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        assert empty_system.charge_count() == 3
    
    def test_remove_charge(self, empty_system):
        """Test removing a charge."""
        id1 = empty_system.add_charge(0, 0, 0, 1e-9)
        id2 = empty_system.add_charge(1, 0, 0, -1e-9)
        
        assert empty_system.remove_charge(id1) == True
        assert empty_system.charge_count() == 1
        assert empty_system.get_charge(id1) is None
        assert empty_system.get_charge(id2) is not None
    
    def test_remove_nonexistent_charge(self, empty_system):
        """Test removing a charge that doesn't exist."""
        assert empty_system.remove_charge(999) == False
    
    def test_get_charge(self, empty_system):
        """Test getting a charge by ID."""
        id1 = empty_system.add_charge(1, 2, 3, 1e-9)
        charge = empty_system.get_charge(id1)
        
        assert charge is not None
        assert charge.x == 1
        assert charge.y == 2
        assert charge.z == 3
        assert charge.q == 1e-9
    
    def test_get_nonexistent_charge(self, empty_system):
        """Test getting a charge that doesn't exist."""
        assert empty_system.get_charge(999) is None
    
    def test_list_charges(self, empty_system):
        """Test listing all charges."""
        empty_system.add_charge(0, 0, 0, 1e-9)
        empty_system.add_charge(1, 0, 0, -1e-9)
        
        charges = empty_system.list_charges()
        assert len(charges) == 2
    
    def test_clear_all(self, empty_system):
        """Test clearing all charges."""
        empty_system.add_charge(0, 0, 0, 1e-9)
        empty_system.add_charge(1, 0, 0, -1e-9)
        empty_system.add_charge(0, 1, 0, 2e-9)
        
        count = empty_system.clear_all()
        assert count == 3
        assert empty_system.charge_count() == 0


class TestElectricField:
    """Tests for electric field calculations."""
    
    def test_field_empty_system(self, empty_system):
        """Test field calculation with no charges."""
        Ex, Ey, Ez = empty_system.electric_field_at(1, 0, 0)
        assert Ex == 0.0
        assert Ey == 0.0
        assert Ez == 0.0
    
    def test_field_single_positive_charge(self, single_charge_system):
        """Test field from a single positive charge at origin."""
        # Field at (1, 0, 0) from 1 nC at origin
        # E = k * q / r^2 = 8.99e9 * 1e-9 / 1 = 8.99 N/C
        Ex, Ey, Ez = single_charge_system.electric_field_at(1, 0, 0)
        
        expected_E = K * 1e-9 / 1.0  # ~8.99 N/C
        assert Ex == pytest.approx(expected_E, rel=1e-6)
        assert Ey == pytest.approx(0.0, abs=1e-10)
        assert Ez == pytest.approx(0.0, abs=1e-10)
    
    def test_field_single_negative_charge(self, empty_system):
        """Test field from a single negative charge."""
        empty_system.add_charge(0, 0, 0, -1e-9)
        
        Ex, Ey, Ez = empty_system.electric_field_at(1, 0, 0)
        
        expected_E = -K * 1e-9 / 1.0  # Negative, pointing toward charge
        assert Ex == pytest.approx(expected_E, rel=1e-6)
    
    def test_field_direction(self, single_charge_system):
        """Test that field points radially outward from positive charge."""
        # Test at different positions
        Ex, Ey, Ez = single_charge_system.electric_field_at(0, 1, 0)
        assert Ex == pytest.approx(0.0, abs=1e-10)
        assert Ey > 0  # Points in +y direction
        
        Ex, Ey, Ez = single_charge_system.electric_field_at(0, 0, 1)
        assert Ex == pytest.approx(0.0, abs=1e-10)
        assert Ey == pytest.approx(0.0, abs=1e-10)
        assert Ez > 0  # Points in +z direction
    
    def test_field_inverse_square_law(self, single_charge_system):
        """Test that field follows inverse square law."""
        E1 = single_charge_system.electric_field_magnitude_at(1, 0, 0)
        E2 = single_charge_system.electric_field_magnitude_at(2, 0, 0)
        
        # E at r=2 should be 1/4 of E at r=1
        assert E2 == pytest.approx(E1 / 4, rel=1e-6)
    
    def test_field_superposition_dipole(self, dipole_system):
        """Test superposition principle with a dipole."""
        # At the midpoint (0, 0, 0), fields from both charges point in -x direction
        Ex, Ey, Ez = dipole_system.electric_field_at(0, 0, 0)
        
        # Both charges contribute field in -x direction at origin
        # From +q at (-0.5, 0, 0): E points in +x (away from charge)
        # From -q at (0.5, 0, 0): E points in +x (toward charge)
        # Total field should be in +x direction
        assert Ex > 0
        assert Ey == pytest.approx(0.0, abs=1e-10)
        assert Ez == pytest.approx(0.0, abs=1e-10)
    
    def test_field_symmetric_cancellation(self, symmetric_system):
        """Test that symmetric charge configuration cancels at center."""
        # Four equal charges at corners of a square
        # Field at center should be zero due to symmetry
        Ex, Ey, Ez = symmetric_system.electric_field_at(0.5, 0.5, 0)
        
        assert Ex == pytest.approx(0.0, abs=1e-6)
        assert Ey == pytest.approx(0.0, abs=1e-6)
        assert Ez == pytest.approx(0.0, abs=1e-6)
    
    def test_field_at_charge_position_raises_error(self, single_charge_system):
        """Test that calculating field at charge position raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            single_charge_system.electric_field_at(0, 0, 0)
        assert "coincides with charge" in str(excinfo.value)
    
    def test_field_magnitude(self, single_charge_system):
        """Test field magnitude calculation."""
        E_mag = single_charge_system.electric_field_magnitude_at(1, 0, 0)
        Ex, Ey, Ez = single_charge_system.electric_field_at(1, 0, 0)
        
        expected_mag = math.sqrt(Ex**2 + Ey**2 + Ez**2)
        assert E_mag == pytest.approx(expected_mag, rel=1e-10)


class TestElectricPotential:
    """Tests for electric potential calculations."""
    
    def test_potential_empty_system(self, empty_system):
        """Test potential calculation with no charges."""
        V = empty_system.potential_at(1, 0, 0)
        assert V == 0.0
    
    def test_potential_single_positive_charge(self, single_charge_system):
        """Test potential from a single positive charge."""
        # V = k * q / r = 8.99e9 * 1e-9 / 1 = 8.99 V
        V = single_charge_system.potential_at(1, 0, 0)
        
        expected_V = K * 1e-9 / 1.0
        assert V == pytest.approx(expected_V, rel=1e-6)
    
    def test_potential_single_negative_charge(self, empty_system):
        """Test potential from a single negative charge."""
        empty_system.add_charge(0, 0, 0, -1e-9)
        
        V = empty_system.potential_at(1, 0, 0)
        
        expected_V = K * (-1e-9) / 1.0  # Negative potential
        assert V == pytest.approx(expected_V, rel=1e-6)
    
    def test_potential_inverse_distance(self, single_charge_system):
        """Test that potential follows 1/r law."""
        V1 = single_charge_system.potential_at(1, 0, 0)
        V2 = single_charge_system.potential_at(2, 0, 0)
        
        # V at r=2 should be 1/2 of V at r=1
        assert V2 == pytest.approx(V1 / 2, rel=1e-6)
    
    def test_potential_superposition_dipole(self, dipole_system):
        """Test potential superposition with a dipole."""
        # At the midpoint (0, 0, 0), potentials should cancel
        # V from +q at distance 0.5: V1 = k * q / 0.5
        # V from -q at distance 0.5: V2 = k * (-q) / 0.5
        # Total: V1 + V2 = 0
        V = dipole_system.potential_at(0, 0, 0)
        assert V == pytest.approx(0.0, abs=1e-6)
    
    def test_potential_at_charge_position_raises_error(self, single_charge_system):
        """Test that calculating potential at charge position raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            single_charge_system.potential_at(0, 0, 0)
        assert "coincides with charge" in str(excinfo.value)
    
    def test_potential_is_scalar(self, empty_system):
        """Test that potential is a scalar (same at equidistant points)."""
        empty_system.add_charge(0, 0, 0, 1e-9)
        
        # All points at distance 1 should have same potential
        V1 = empty_system.potential_at(1, 0, 0)
        V2 = empty_system.potential_at(0, 1, 0)
        V3 = empty_system.potential_at(0, 0, 1)
        V4 = empty_system.potential_at(-1, 0, 0)
        
        assert V1 == pytest.approx(V2, rel=1e-10)
        assert V2 == pytest.approx(V3, rel=1e-10)
        assert V3 == pytest.approx(V4, rel=1e-10)


class TestSingleChargeCalculations:
    """Tests for single charge field and potential calculations."""
    
    def test_field_from_single_charge(self, empty_system):
        """Test calculating field from a specific charge."""
        id1 = empty_system.add_charge(0, 0, 0, 1e-9)
        id2 = empty_system.add_charge(2, 0, 0, 1e-9)
        
        # Field from charge 1 only at (1, 0, 0)
        Ex, Ey, Ez = empty_system.field_from_single_charge(id1, 1, 0, 0)
        
        expected_E = K * 1e-9 / 1.0
        assert Ex == pytest.approx(expected_E, rel=1e-6)
    
    def test_field_from_nonexistent_charge(self, empty_system):
        """Test that field from nonexistent charge raises KeyError."""
        with pytest.raises(KeyError):
            empty_system.field_from_single_charge(999, 1, 0, 0)
    
    def test_potential_from_single_charge(self, empty_system):
        """Test calculating potential from a specific charge."""
        id1 = empty_system.add_charge(0, 0, 0, 1e-9)
        id2 = empty_system.add_charge(2, 0, 0, 1e-9)
        
        # Potential from charge 1 only at (1, 0, 0)
        V = empty_system.potential_from_single_charge(id1, 1, 0, 0)
        
        expected_V = K * 1e-9 / 1.0
        assert V == pytest.approx(expected_V, rel=1e-6)
    
    def test_potential_from_nonexistent_charge(self, empty_system):
        """Test that potential from nonexistent charge raises KeyError."""
        with pytest.raises(KeyError):
            empty_system.potential_from_single_charge(999, 1, 0, 0)


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_calculate_field_function(self):
        """Test the calculate_field convenience function."""
        charges = [(0, 0, 0, 1e-9)]
        Ex, Ey, Ez = calculate_field(charges, (1, 0, 0))
        
        expected_E = K * 1e-9 / 1.0
        assert Ex == pytest.approx(expected_E, rel=1e-6)
    
    def test_calculate_potential_function(self):
        """Test the calculate_potential convenience function."""
        charges = [(0, 0, 0, 1e-9)]
        V = calculate_potential(charges, (1, 0, 0))
        
        expected_V = K * 1e-9 / 1.0
        assert V == pytest.approx(expected_V, rel=1e-6)
    
    def test_calculate_field_multiple_charges(self):
        """Test calculate_field with multiple charges."""
        charges = [
            (0, 0, 0, 1e-9),
            (2, 0, 0, 1e-9)
        ]
        Ex, Ey, Ez = calculate_field(charges, (1, 0, 0))
        
        # At midpoint, fields from both charges point in opposite directions
        # and should cancel
        assert Ex == pytest.approx(0.0, abs=1e-6)


class TestPhysicalConstants:
    """Tests for physical constants."""
    
    def test_epsilon_0_value(self):
        """Test that epsilon_0 has correct value."""
        assert EPSILON_0 == pytest.approx(8.8541878128e-12, rel=1e-10)
    
    def test_coulomb_constant_value(self):
        """Test that Coulomb's constant has correct value."""
        expected_K = 1 / (4 * math.pi * EPSILON_0)
        assert K == pytest.approx(expected_K, rel=1e-10)
        assert K == pytest.approx(8.9875517923e9, rel=1e-6)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_very_small_charge(self, empty_system):
        """Test with very small charge value."""
        empty_system.add_charge(0, 0, 0, 1e-20)
        
        V = empty_system.potential_at(1, 0, 0)
        expected_V = K * 1e-20 / 1.0
        assert V == pytest.approx(expected_V, rel=1e-6)
    
    def test_very_large_charge(self, empty_system):
        """Test with very large charge value."""
        empty_system.add_charge(0, 0, 0, 1e6)
        
        V = empty_system.potential_at(1, 0, 0)
        expected_V = K * 1e6 / 1.0
        assert V == pytest.approx(expected_V, rel=1e-6)
    
    def test_very_close_to_charge(self, single_charge_system):
        """Test field calculation very close to charge."""
        # At r = 0.001 m
        E_mag = single_charge_system.electric_field_magnitude_at(0.001, 0, 0)
        
        expected_E = K * 1e-9 / (0.001**2)
        assert E_mag == pytest.approx(expected_E, rel=1e-6)
    
    def test_very_far_from_charge(self, single_charge_system):
        """Test field calculation very far from charge."""
        # At r = 1000 m
        E_mag = single_charge_system.electric_field_magnitude_at(1000, 0, 0)
        
        expected_E = K * 1e-9 / (1000**2)
        assert E_mag == pytest.approx(expected_E, rel=1e-6)
    
    def test_negative_coordinates(self, empty_system):
        """Test with negative coordinates."""
        empty_system.add_charge(-1, -2, -3, 1e-9)
        
        # Field at origin
        Ex, Ey, Ez = empty_system.electric_field_at(0, 0, 0)
        
        # Field should point toward positive coordinates (away from charge)
        assert Ex > 0
        assert Ey > 0
        assert Ez > 0
    
    def test_zero_charge(self, empty_system):
        """Test with zero charge value."""
        empty_system.add_charge(0, 0, 0, 0)
        
        Ex, Ey, Ez = empty_system.electric_field_at(1, 0, 0)
        V = empty_system.potential_at(1, 0, 0)
        
        assert Ex == pytest.approx(0.0, abs=1e-20)
        assert Ey == pytest.approx(0.0, abs=1e-20)
        assert Ez == pytest.approx(0.0, abs=1e-20)
        assert V == pytest.approx(0.0, abs=1e-20)


class TestChargeManagement:
    """Tests for charge management operations."""
    
    def test_add_remove_add_sequence(self, empty_system):
        """Test adding, removing, and adding charges in sequence."""
        id1 = empty_system.add_charge(0, 0, 0, 1e-9)
        id2 = empty_system.add_charge(1, 0, 0, 1e-9)
        
        empty_system.remove_charge(id1)
        
        id3 = empty_system.add_charge(2, 0, 0, 1e-9)
        
        # id3 should be 3, not 1 (IDs are not reused)
        assert id3 == 3
        assert empty_system.charge_count() == 2
    
    def test_clear_and_add(self, empty_system):
        """Test clearing all charges and adding new ones."""
        empty_system.add_charge(0, 0, 0, 1e-9)
        empty_system.add_charge(1, 0, 0, 1e-9)
        
        empty_system.clear_all()
        
        # IDs continue from where they left off
        id_new = empty_system.add_charge(0, 0, 0, 1e-9)
        assert id_new == 3
    
    def test_multiple_removes(self, empty_system):
        """Test removing multiple charges."""
        id1 = empty_system.add_charge(0, 0, 0, 1e-9)
        id2 = empty_system.add_charge(1, 0, 0, 1e-9)
        id3 = empty_system.add_charge(2, 0, 0, 1e-9)
        
        empty_system.remove_charge(id2)
        empty_system.remove_charge(id1)
        
        assert empty_system.charge_count() == 1
        assert empty_system.get_charge(id3) is not None
