"""
Core module for multi-charge electric field and potential calculations.

This module provides classes and functions to:
- Create and manage multiple point charges in 3D Cartesian space
- Calculate electric field vectors at arbitrary points
- Calculate electric potential at arbitrary points
- Support adding and removing charges dynamically

Physical Constants:
    EPSILON_0: Vacuum permittivity (8.8541878128e-12 F/m)
    K: Coulomb's constant (1/(4*pi*epsilon_0) ≈ 8.9875517923e9 N·m²/C²)

Classes:
    PointCharge: Represents a single point charge with position and charge value
    ChargeSystem: Manages a collection of point charges and calculates fields

Example:
    >>> from field_calc.core import ChargeSystem
    >>> system = ChargeSystem()
    >>> system.add_charge(0, 0, 0, 1e-9)  # Add 1 nC at origin
    >>> system.add_charge(1, 0, 0, -1e-9)  # Add -1 nC at (1,0,0)
    >>> E = system.electric_field_at(0.5, 0, 0)  # Field at midpoint
    >>> V = system.potential_at(0.5, 0, 0)  # Potential at midpoint
"""

import math
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, field

# Physical constants
EPSILON_0 = 8.8541878128e-12  # Vacuum permittivity (F/m)
K = 1 / (4 * math.pi * EPSILON_0)  # Coulomb's constant (N·m²/C²)


@dataclass
class PointCharge:
    """
    Represents a point charge in 3D Cartesian space.
    
    Attributes:
        x (float): x-coordinate in meters
        y (float): y-coordinate in meters
        z (float): z-coordinate in meters
        q (float): charge value in Coulombs (positive or negative)
        charge_id (int): unique identifier for the charge
    
    Example:
        >>> charge = PointCharge(x=1.0, y=2.0, z=0.0, q=1e-9, charge_id=1)
        >>> print(charge)
        PointCharge(id=1, position=(1.0, 2.0, 0.0), q=1.00e-09 C)
    """
    x: float
    y: float
    z: float
    q: float
    charge_id: int
    
    def __str__(self) -> str:
        return f"PointCharge(id={self.charge_id}, position=({self.x}, {self.y}, {self.z}), q={self.q:.2e} C)"
    
    def position(self) -> Tuple[float, float, float]:
        """Return the position as a tuple (x, y, z)."""
        return (self.x, self.y, self.z)
    
    def distance_to(self, x: float, y: float, z: float) -> float:
        """
        Calculate the distance from this charge to a point.
        
        Args:
            x: x-coordinate of the point
            y: y-coordinate of the point
            z: z-coordinate of the point
            
        Returns:
            Distance in meters
        """
        return math.sqrt((x - self.x)**2 + (y - self.y)**2 + (z - self.z)**2)


class ChargeSystem:
    """
    A system of multiple point charges for calculating electric fields and potentials.
    
    This class manages a collection of point charges and provides methods to:
    - Add charges at specified Cartesian coordinates
    - Remove charges by their ID
    - Calculate the total electric field at any point
    - Calculate the total electric potential at any point
    - List all charges in the system
    
    The electric field is calculated using Coulomb's law:
        E = k * q / r² (magnitude)
        E_vec = k * q * r_hat / r² (vector form)
    
    The electric potential is calculated as:
        V = k * q / r
    
    For multiple charges, the principle of superposition applies:
        E_total = sum(E_i)
        V_total = sum(V_i)
    
    Attributes:
        charges (Dict[int, PointCharge]): Dictionary of charges indexed by ID
        _next_id (int): Counter for generating unique charge IDs
    
    Example:
        >>> system = ChargeSystem()
        >>> id1 = system.add_charge(0, 0, 0, 1e-9)
        >>> id2 = system.add_charge(1, 0, 0, -1e-9)
        >>> print(system.list_charges())
        >>> Ex, Ey, Ez = system.electric_field_at(0.5, 0.5, 0)
        >>> V = system.potential_at(0.5, 0.5, 0)
    """
    
    def __init__(self):
        """Initialize an empty charge system."""
        self.charges: Dict[int, PointCharge] = {}
        self._next_id: int = 1
    
    def add_charge(self, x: float, y: float, z: float, q: float) -> int:
        """
        Add a point charge to the system.
        
        Args:
            x: x-coordinate in meters
            y: y-coordinate in meters
            z: z-coordinate in meters
            q: charge value in Coulombs (can be positive or negative)
        
        Returns:
            int: The unique ID assigned to this charge
        
        Example:
            >>> system = ChargeSystem()
            >>> charge_id = system.add_charge(1.0, 2.0, 0.0, 1e-9)
            >>> print(f"Added charge with ID: {charge_id}")
            Added charge with ID: 1
        """
        charge = PointCharge(x=x, y=y, z=z, q=q, charge_id=self._next_id)
        self.charges[self._next_id] = charge
        assigned_id = self._next_id
        self._next_id += 1
        return assigned_id
    
    def remove_charge(self, charge_id: int) -> bool:
        """
        Remove a charge from the system by its ID.
        
        Args:
            charge_id: The unique ID of the charge to remove
        
        Returns:
            bool: True if the charge was removed, False if not found
        
        Example:
            >>> system = ChargeSystem()
            >>> id1 = system.add_charge(0, 0, 0, 1e-9)
            >>> system.remove_charge(id1)
            True
            >>> system.remove_charge(999)  # Non-existent ID
            False
        """
        if charge_id in self.charges:
            del self.charges[charge_id]
            return True
        return False
    
    def get_charge(self, charge_id: int) -> Optional[PointCharge]:
        """
        Get a charge by its ID.
        
        Args:
            charge_id: The unique ID of the charge
        
        Returns:
            PointCharge if found, None otherwise
        """
        return self.charges.get(charge_id)
    
    def list_charges(self) -> List[PointCharge]:
        """
        Get a list of all charges in the system.
        
        Returns:
            List of PointCharge objects
        
        Example:
            >>> system = ChargeSystem()
            >>> system.add_charge(0, 0, 0, 1e-9)
            >>> system.add_charge(1, 0, 0, -1e-9)
            >>> for charge in system.list_charges():
            ...     print(charge)
        """
        return list(self.charges.values())
    
    def clear_all(self) -> int:
        """
        Remove all charges from the system.
        
        Returns:
            int: Number of charges removed
        """
        count = len(self.charges)
        self.charges.clear()
        return count
    
    def charge_count(self) -> int:
        """Return the number of charges in the system."""
        return len(self.charges)
    
    def electric_field_at(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """
        Calculate the total electric field at a point due to all charges.
        
        The electric field from each charge is calculated using Coulomb's law:
            E = k * q * r_hat / r²
        
        where r_hat is the unit vector pointing from the charge to the field point.
        
        The total field is the vector sum of all individual fields (superposition).
        
        Args:
            x: x-coordinate of the field point in meters
            y: y-coordinate of the field point in meters
            z: z-coordinate of the field point in meters
        
        Returns:
            Tuple[float, float, float]: Electric field components (Ex, Ey, Ez) in N/C
        
        Raises:
            ValueError: If the field point coincides with any charge position
        
        Example:
            >>> system = ChargeSystem()
            >>> system.add_charge(0, 0, 0, 1e-9)  # 1 nC at origin
            >>> Ex, Ey, Ez = system.electric_field_at(1, 0, 0)
            >>> print(f"E = ({Ex:.2e}, {Ey:.2e}, {Ez:.2e}) N/C")
        """
        if not self.charges:
            return (0.0, 0.0, 0.0)
        
        Ex_total = 0.0
        Ey_total = 0.0
        Ez_total = 0.0
        
        for charge in self.charges.values():
            # Vector from charge to field point
            dx = x - charge.x
            dy = y - charge.y
            dz = z - charge.z
            
            # Distance
            r = math.sqrt(dx**2 + dy**2 + dz**2)
            
            if r < 1e-15:  # Essentially zero distance
                raise ValueError(
                    f"Field point ({x}, {y}, {z}) coincides with charge ID {charge.charge_id} "
                    f"at ({charge.x}, {charge.y}, {charge.z}). Electric field is undefined."
                )
            
            # Electric field magnitude from this charge
            E_mag = K * charge.q / (r**2)
            
            # Unit vector components
            rx_hat = dx / r
            ry_hat = dy / r
            rz_hat = dz / r
            
            # Add field components (field points away from positive charges)
            Ex_total += E_mag * rx_hat
            Ey_total += E_mag * ry_hat
            Ez_total += E_mag * rz_hat
        
        return (Ex_total, Ey_total, Ez_total)
    
    def electric_field_magnitude_at(self, x: float, y: float, z: float) -> float:
        """
        Calculate the magnitude of the total electric field at a point.
        
        Args:
            x: x-coordinate of the field point in meters
            y: y-coordinate of the field point in meters
            z: z-coordinate of the field point in meters
        
        Returns:
            float: Electric field magnitude in N/C
        
        Example:
            >>> system = ChargeSystem()
            >>> system.add_charge(0, 0, 0, 1e-9)
            >>> E_mag = system.electric_field_magnitude_at(1, 0, 0)
            >>> print(f"|E| = {E_mag:.2e} N/C")
        """
        Ex, Ey, Ez = self.electric_field_at(x, y, z)
        return math.sqrt(Ex**2 + Ey**2 + Ez**2)
    
    def potential_at(self, x: float, y: float, z: float) -> float:
        """
        Calculate the total electric potential at a point due to all charges.
        
        The electric potential from each charge is:
            V = k * q / r
        
        The total potential is the scalar sum of all individual potentials.
        
        Args:
            x: x-coordinate of the point in meters
            y: y-coordinate of the point in meters
            z: z-coordinate of the point in meters
        
        Returns:
            float: Electric potential in Volts (V)
        
        Raises:
            ValueError: If the point coincides with any charge position
        
        Example:
            >>> system = ChargeSystem()
            >>> system.add_charge(0, 0, 0, 1e-9)  # 1 nC at origin
            >>> V = system.potential_at(1, 0, 0)
            >>> print(f"V = {V:.2f} V")
        """
        if not self.charges:
            return 0.0
        
        V_total = 0.0
        
        for charge in self.charges.values():
            r = charge.distance_to(x, y, z)
            
            if r < 1e-15:  # Essentially zero distance
                raise ValueError(
                    f"Point ({x}, {y}, {z}) coincides with charge ID {charge.charge_id} "
                    f"at ({charge.x}, {charge.y}, {charge.z}). Potential is undefined."
                )
            
            V_total += K * charge.q / r
        
        return V_total
    
    def field_from_single_charge(self, charge_id: int, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """
        Calculate the electric field at a point from a single specific charge.
        
        Args:
            charge_id: ID of the charge
            x: x-coordinate of the field point
            y: y-coordinate of the field point
            z: z-coordinate of the field point
        
        Returns:
            Tuple[float, float, float]: Electric field components (Ex, Ey, Ez) in N/C
        
        Raises:
            KeyError: If charge_id is not found
            ValueError: If the field point coincides with the charge
        """
        if charge_id not in self.charges:
            raise KeyError(f"Charge with ID {charge_id} not found")
        
        charge = self.charges[charge_id]
        
        dx = x - charge.x
        dy = y - charge.y
        dz = z - charge.z
        r = math.sqrt(dx**2 + dy**2 + dz**2)
        
        if r < 1e-15:
            raise ValueError(f"Field point coincides with charge ID {charge_id}")
        
        E_mag = K * charge.q / (r**2)
        
        return (E_mag * dx / r, E_mag * dy / r, E_mag * dz / r)
    
    def potential_from_single_charge(self, charge_id: int, x: float, y: float, z: float) -> float:
        """
        Calculate the electric potential at a point from a single specific charge.
        
        Args:
            charge_id: ID of the charge
            x: x-coordinate of the point
            y: y-coordinate of the point
            z: z-coordinate of the point
        
        Returns:
            float: Electric potential in Volts
        
        Raises:
            KeyError: If charge_id is not found
            ValueError: If the point coincides with the charge
        """
        if charge_id not in self.charges:
            raise KeyError(f"Charge with ID {charge_id} not found")
        
        charge = self.charges[charge_id]
        r = charge.distance_to(x, y, z)
        
        if r < 1e-15:
            raise ValueError(f"Point coincides with charge ID {charge_id}")
        
        return K * charge.q / r


# Convenience functions for quick calculations

def calculate_field(charges: List[Tuple[float, float, float, float]], 
                   point: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """
    Convenience function to calculate electric field from a list of charges.
    
    Args:
        charges: List of tuples (x, y, z, q) for each charge
        point: Tuple (x, y, z) of the field point
    
    Returns:
        Tuple (Ex, Ey, Ez) of electric field components in N/C
    
    Example:
        >>> charges = [(0, 0, 0, 1e-9), (1, 0, 0, -1e-9)]
        >>> E = calculate_field(charges, (0.5, 0, 0))
    """
    system = ChargeSystem()
    for x, y, z, q in charges:
        system.add_charge(x, y, z, q)
    return system.electric_field_at(*point)


def calculate_potential(charges: List[Tuple[float, float, float, float]], 
                       point: Tuple[float, float, float]) -> float:
    """
    Convenience function to calculate electric potential from a list of charges.
    
    Args:
        charges: List of tuples (x, y, z, q) for each charge
        point: Tuple (x, y, z) of the point
    
    Returns:
        Electric potential in Volts
    
    Example:
        >>> charges = [(0, 0, 0, 1e-9), (1, 0, 0, -1e-9)]
        >>> V = calculate_potential(charges, (0.5, 0, 0))
    """
    system = ChargeSystem()
    for x, y, z, q in charges:
        system.add_charge(x, y, z, q)
    return system.potential_at(*point)
