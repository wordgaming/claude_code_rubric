import sys
from .core import electric_flux, electric_field

def main():
    if len(sys.argv) not in (2, 3):
        print('Usage: field-calc <charge_in_C> [radius_in_m|"r"]')
        sys.exit(1)

    q_arg = sys.argv[1]
    r_arg = sys.argv[2] if len(sys.argv) == 3 else 'r'

    try:
        q = float(q_arg)
    except ValueError:
        print('Error: charge must be a number')
        sys.exit(1)

    electric_flux(q)

    if r_arg == 'r':
        electric_field(q, 'r')
    else:
        try:
            r = float(r_arg)
        except ValueError:
            print('Error: radius must be a number or "r"')
            sys.exit(1)
        electric_field(q, r)

if __name__ == '__main__':
    main()
