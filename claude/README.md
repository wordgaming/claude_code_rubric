# Multi-Charge Electric Field Calculator

A Python package for calculating electric fields and potentials from multiple point charges in 3D Cartesian space.

## Features

- **Multiple Charges**: Add any number of point charges with specified positions and charge values
- **Dynamic Management**: Add and remove charges freely between calculations
- **Electric Field**: Calculate the total electric field vector at any point
- **Electric Potential**: Calculate the total electric potential at any point
- **Interactive CLI**: User-friendly command-line interface for interactive use
- **Programmatic API**: Clean Python API for integration into other projects

## Installation

```bash
cd project/claude
pip install -e .
```

## Quick Start

### Interactive Mode

Start the interactive CLI:

```bash
field-calc
```

This opens an interactive prompt where you can add charges and calculate fields:

```
============================================================
  Multi-Charge Electric Field Calculator
  Type 'help' for available commands, 'quit' to exit
============================================================

field-calc> add 0 0 0 1e-9
✓ Added charge ID 1: position=(0.0, 0.0, 0.0) m, q=1.00e-09 C

field-calc> add 1 0 0 -1e-9
✓ Added charge ID 2: position=(1.0, 0.0, 0.0) m, q=-1.00e-09 C

field-calc> field 0.5 0 0
============================================================
Electric Field at (0.5, 0.0, 0.0) m:
============================================================
  Ex =  -7.1900e+01 N/C
  Ey =   0.0000e+00 N/C
  Ez =   0.0000e+00 N/C
  |E| =  7.1900e+01 N/C
============================================================

field-calc> potential 0.5 0 0
============================================================
Electric Potential at (0.5, 0.0, 0.0) m:
============================================================
  V =   0.0000e+00 V
============================================================
```

### Command-Line Mode

Calculate fields directly from the command line:

```bash
# Define charges and calculate field
field-calc --charges "0,0,0,1e-9;1,0,0,-1e-9" --field 0.5,0,0

# Calculate potential
field-calc --charges "0,0,0,1e-9;1,0,0,-1e-9" --potential 0.5,0,0
```

### Python API

```python
from field_calc import ChargeSystem

# Create a charge system
system = ChargeSystem()

# Add charges: add_charge(x, y, z, q)
id1 = system.add_charge(0, 0, 0, 1e-9)    # 1 nC at origin
id2 = system.add_charge(1, 0, 0, -1e-9)   # -1 nC at (1,0,0)
id3 = system.add_charge(0, 1, 0, 2e-9)    # 2 nC at (0,1,0)

# Calculate electric field at a point
Ex, Ey, Ez = system.electric_field_at(0.5, 0.5, 0)
print(f"E = ({Ex:.2e}, {Ey:.2e}, {Ez:.2e}) N/C")

# Calculate field magnitude
E_mag = system.electric_field_magnitude_at(0.5, 0.5, 0)
print(f"|E| = {E_mag:.2e} N/C")

# Calculate electric potential at a point
V = system.potential_at(0.5, 0.5, 0)
print(f"V = {V:.2e} V")

# Remove a charge
system.remove_charge(id2)

# List all charges
for charge in system.list_charges():
    print(charge)

# Clear all charges
system.clear_all()
```

## Interactive CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <x> <y> <z> <q>` | Add a point charge at position (x,y,z) with charge q | `add 0 0 0 1e-9` |
| `remove <id>` | Remove charge with given ID | `remove 1` |
| `list` | List all charges in the system | `list` |
| `field <x> <y> <z>` | Calculate electric field at point (x,y,z) | `field 0.5 0 0` |
| `potential <x> <y> <z>` | Calculate electric potential at point (x,y,z) | `potential 0.5 0 0` |
| `clear` | Remove all charges | `clear` |
| `help` | Show help message | `help` |
| `quit` / `exit` | Exit the program | `quit` |

### Command Aliases

- `remove` can also be written as `rm` or `delete`
- `list` can also be written as `ls`
- `field` can also be written as `e`
- `potential` can also be written as `v`
- `quit` can also be written as `exit` or `q`

## How to Add Multiple Charges

### Method 1: Interactive CLI

```bash
field-calc
```

Then at the prompt:
```
field-calc> add 0 0 0 1e-9
field-calc> add 1 0 0 -1e-9
field-calc> add 0.5 0.5 0 2e-9
field-calc> list
```

### Method 2: Command Line with Multiple Charges

Use semicolons to separate charges:
```bash
field-calc --charges "0,0,0,1e-9;1,0,0,-1e-9;0.5,0.5,0,2e-9" --field 0.5,0,0
```

### Method 3: Python API

```python
from field_calc import ChargeSystem

system = ChargeSystem()

# Add charges one by one
system.add_charge(0, 0, 0, 1e-9)
system.add_charge(1, 0, 0, -1e-9)
system.add_charge(0.5, 0.5, 0, 2e-9)

# Or use the convenience function
from field_calc.core import calculate_field, calculate_potential

charges = [
    (0, 0, 0, 1e-9),
    (1, 0, 0, -1e-9),
    (0.5, 0.5, 0, 2e-9)
]

E = calculate_field(charges, (0.5, 0, 0))
V = calculate_potential(charges, (0.5, 0, 0))
```

## Physical Background

### Electric Field

The electric field from a point charge is calculated using Coulomb's law:

$$\vec{E} = k \frac{q}{r^2} \hat{r}$$

where:
- $k = \frac{1}{4\pi\epsilon_0} \approx 8.99 \times 10^9 \, \text{N·m}^2/\text{C}^2$ (Coulomb's constant)
- $q$ is the charge in Coulombs
- $r$ is the distance from the charge to the field point
- $\hat{r}$ is the unit vector pointing from the charge to the field point

For multiple charges, the total field is the vector sum (superposition principle):

$$\vec{E}_{total} = \sum_i \vec{E}_i$$

### Electric Potential

The electric potential from a point charge is:

$$V = k \frac{q}{r}$$

For multiple charges, the total potential is the scalar sum:

$$V_{total} = \sum_i V_i$$

## Units

- **Position**: meters (m)
- **Charge**: Coulombs (C)
  - Common values: 1 nC = 1e-9 C, 1 μC = 1e-6 C
- **Electric Field**: Newtons per Coulomb (N/C) or Volts per meter (V/m)
- **Electric Potential**: Volts (V)

## Examples

### Example 1: Electric Dipole

An electric dipole consists of two equal and opposite charges:

```python
from field_calc import ChargeSystem

system = ChargeSystem()
system.add_charge(-0.5, 0, 0, 1e-9)   # +1 nC
system.add_charge(0.5, 0, 0, -1e-9)   # -1 nC

# Field along the axis
Ex, Ey, Ez = system.electric_field_at(2, 0, 0)
print(f"Field on axis: E = ({Ex:.2e}, {Ey:.2e}, {Ez:.2e}) N/C")

# Field perpendicular to axis
Ex, Ey, Ez = system.electric_field_at(0, 2, 0)
print(f"Field perpendicular: E = ({Ex:.2e}, {Ey:.2e}, {Ez:.2e}) N/C")
```

### Example 2: Square Configuration

Four charges at the corners of a square:

```python
from field_calc import ChargeSystem

system = ChargeSystem()
# Charges at corners of a 1m x 1m square
system.add_charge(0, 0, 0, 1e-9)
system.add_charge(1, 0, 0, 1e-9)
system.add_charge(0, 1, 0, 1e-9)
system.add_charge(1, 1, 0, 1e-9)

# Field at center
Ex, Ey, Ez = system.electric_field_at(0.5, 0.5, 0)
print(f"Field at center: E = ({Ex:.2e}, {Ey:.2e}, {Ez:.2e}) N/C")
# Due to symmetry, the field at the center should be zero
```

### Example 3: Linear Charge Array

```python
from field_calc import ChargeSystem

system = ChargeSystem()
# 5 charges along the x-axis
for i in range(5):
    system.add_charge(i, 0, 0, 1e-9)

# Field at a point above the array
Ex, Ey, Ez = system.electric_field_at(2, 1, 0)
E_mag = system.electric_field_magnitude_at(2, 1, 0)
print(f"Field: E = ({Ex:.2e}, {Ey:.2e}, {Ez:.2e}) N/C")
print(f"Magnitude: |E| = {E_mag:.2e} N/C")
```

## Running Tests

```bash
cd project/claude
pytest tests/ -v
```

## API Reference

### ChargeSystem Class

#### Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `add_charge(x, y, z, q)` | Add a charge at position (x,y,z) with charge q | Charge ID (int) |
| `remove_charge(id)` | Remove charge by ID | True if removed, False if not found |
| `get_charge(id)` | Get charge by ID | PointCharge or None |
| `list_charges()` | Get all charges | List of PointCharge |
| `clear_all()` | Remove all charges | Number of charges removed |
| `charge_count()` | Get number of charges | int |
| `electric_field_at(x, y, z)` | Calculate field at point | Tuple (Ex, Ey, Ez) |
| `electric_field_magnitude_at(x, y, z)` | Calculate field magnitude | float |
| `potential_at(x, y, z)` | Calculate potential at point | float |

### PointCharge Class

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `x` | float | x-coordinate in meters |
| `y` | float | y-coordinate in meters |
| `z` | float | z-coordinate in meters |
| `q` | float | Charge in Coulombs |
| `charge_id` | int | Unique identifier |

## License

MIT License
