# flux and field calc
find electric flux and field by Gauss law

## Installation
    pip install -e .

## Usage
    field-calc <charge_in_C> [radius_in_m|"r"]

Examples:
    $ field-calc 1e-6
    Electric flux: 1.129e+05 N·m²/C
    Electric field: 8.988e+03/(r**2) N/C

    $ field-calc 1e-6 0.1
    Electric flux: 1.129e+17 N·m²/C
    Electric field at r=0.1 m: 8.992e+09 N/C
