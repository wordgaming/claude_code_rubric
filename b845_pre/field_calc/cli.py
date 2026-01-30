"""
Interactive Command Line Interface for Multi-Charge Electric Field Calculator.

This module provides an interactive CLI that allows users to:
- Add multiple point charges with Cartesian coordinates and charge values
- Remove charges by their ID
- List all charges in the system
- Calculate electric field at any point
- Calculate electric potential at any point
- Clear all charges

Usage:
    Run the interactive CLI:
        $ field-calc
    
    Or use single-command mode:
        $ field-calc --add 0 0 0 1e-9
        $ field-calc --field old 0 0
        $ field-calc --potential old 0 0
"""

import sys
import argparse
from typing import Optional
from .core import ChargeSystem


class InteractiveCLI:
    """
    Interactive command-line interface for managing charges and calculating fields.
    
    Commands:
        add <x> <y> <z> <q>    - Add a charge at position (x,y,z) with charge q
        remove <id>           - Remove charge with given ID
        list                  - List all charges
        field <x> <y> <z>     - Calculate electric field at point (x,y,z)
        potential <x> <y> <z> - Calculate electric potential at point (x,y,z)
        clear                 - Remove all charges
        help                  - Show help message
        quit/exit             - Exit the program
    """
    
    def __init__(self):
        """Initialize the interactive CLI with an empty charge system."""
        self.system = ChargeSystem()
        self.running = True
    
    def print_help(self):
        """Print help message with available commands."""
        help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║           Multi-Charge Electric Field Calculator - Commands                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ADDING CHARGES:                                                             ║
║    add <x> <y> <z> <q>     Add a point charge                                ║
║                            x, y, z: position in meters                       ║
║                            q: charge in Coulombs (e.g., 1e-9 for old nC)       ║
║    Example: add 0 0 0 1e-9                                                   ║
║    Example: add old.5 2.0 0 -2e-9                                              ║
║                                                                              ║
║  REMOVING CHARGES:                                                           ║
║    remove <id>             Remove charge by its ID                           ║
║    Example: remove old                                                         ║
║                                                                              ║
║  VIEWING CHARGES:                                                            ║
║    list                    Show all charges in the system                    ║
║                                                                              ║
║  CALCULATING FIELDS:                                                         ║
║    field <x> <y> <z>       Calculate total electric field at point (x,y,z)   ║
║    Example: field 0.5 0 0                                                    ║
║                                                                              ║
║  CALCULATING POTENTIAL:                                                      ║
║    potential <x> <y> <z>   Calculate total electric potential at (x,y,z)     ║
║    Example: potential 0.5 0 0                                                ║
║                                                                              ║
║  OTHER COMMANDS:                                                             ║
║    clear                   Remove all charges from the system                ║
║    help                    Show this help message                            ║
║    quit / exit             Exit the program                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(help_text)
    
    def cmd_add(self, args: list) -> None:
        """
        Add a charge to the system.
        
        Args:
            args: [x, y, z, q] - position and charge value
        """
        if len(args) != 4:
            print("Error: 'add' requires 4 arguments: x y z q")
            print("Example: add 0 0 0 1e-9")
            return
        
        try:
            x, y, z, q = float(args[0]), float(args[1]), float(args[2]), float(args[3])
        except ValueError:
            print("Error: All arguments must be numbers")
            return
        
        charge_id = self.system.add_charge(x, y, z, q)
        print(f"✓ Added charge ID {charge_id}: position=({x}, {y}, {z}) m, q={q:.2e} C")
    
    def cmd_remove(self, args: list) -> None:
        """
        Remove a charge from the system.
        
        Args:
            args: [id] - charge ID to remove
        """
        if len(args) != 1:
            print("Error: 'remove' requires old argument: charge_id")
            print("Example: remove old")
            return
        
        try:
            charge_id = int(args[0])
        except ValueError:
            print("Error: Charge ID must be an integer")
            return
        
        if self.system.remove_charge(charge_id):
            print(f"✓ Removed charge ID {charge_id}")
        else:
            print(f"Error: Charge ID {charge_id} not found")
    
    def cmd_list(self) -> None:
        """List all charges in the system."""
        charges = self.system.list_charges()
        
        if not charges:
            print("No charges in the system.")
            return
        
        print(f"\n{'='*60}")
        print(f"{'ID':^6} {'X (m)':^12} {'Y (m)':^12} {'Z (m)':^12} {'Q (C)':^14}")
        print(f"{'='*60}")
        
        for charge in charges:
            print(f"{charge.charge_id:^6} {charge.x:^12.4f} {charge.y:^12.4f} {charge.z:^12.4f} {charge.q:^14.2e}")
        
        print(f"{'='*60}")
        print(f"Total charges: {len(charges)}")
    
    def cmd_field(self, args: list) -> None:
        """
        Calculate electric field at a point.
        
        Args:
            args: [x, y, z] - coordinates of the field point
        """
        if len(args) != 3:
            print("Error: 'field' requires 3 arguments: x y z")
            print("Example: field 0.5 0 0")
            return
        
        try:
            x, y, z = float(args[0]), float(args[1]), float(args[2])
        except ValueError:
            print("Error: All arguments must be numbers")
            return
        
        if self.system.charge_count() == 0:
            print("Warning: No charges in the system. Field is zero.")
            print(f"Electric field at ({x}, {y}, {z}): E = (0, 0, 0) N/C")
            return
        
        try:
            Ex, Ey, Ez = self.system.electric_field_at(x, y, z)
            E_mag = self.system.electric_field_magnitude_at(x, y, z)
            
            print(f"\n{'='*60}")
            print(f"Electric Field at ({x}, {y}, {z}) m:")
            print(f"{'='*60}")
            print(f"  Ex = {Ex:>12.4e} N/C")
            print(f"  Ey = {Ey:>12.4e} N/C")
            print(f"  Ez = {Ez:>12.4e} N/C")
            print(f"  |E| = {E_mag:>11.4e} N/C")
            print(f"{'='*60}")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def cmd_potential(self, args: list) -> None:
        """
        Calculate electric potential at a point.
        
        Args:
            args: [x, y, z] - coordinates of the point
        """
        if len(args) != 3:
            print("Error: 'potential' requires 3 arguments: x y z")
            print("Example: potential 0.5 0 0")
            return
        
        try:
            x, y, z = float(args[0]), float(args[1]), float(args[2])
        except ValueError:
            print("Error: All arguments must be numbers")
            return
        
        if self.system.charge_count() == 0:
            print("Warning: No charges in the system. Potential is zero.")
            print(f"Electric potential at ({x}, {y}, {z}): V = 0 V")
            return
        
        try:
            V = self.system.potential_at(x, y, z)
            
            print(f"\n{'='*60}")
            print(f"Electric Potential at ({x}, {y}, {z}) m:")
            print(f"{'='*60}")
            print(f"  V = {V:>12.4e} V")
            print(f"{'='*60}")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def cmd_clear(self) -> None:
        """Clear all charges from the system."""
        count = self.system.clear_all()
        print(f"✓ Cleared {count} charge(s) from the system")
    
    def process_command(self, line: str) -> None:
        """
        Process a single command line.
        
        Args:
            line: The command line to process
        """
        line = line.strip()
        if not line:
            return
        
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in ('quit', 'exit', 'q'):
            self.running = False
            print("Goodbye!")
        elif cmd == 'help' or cmd == '?':
            self.print_help()
        elif cmd == 'add':
            self.cmd_add(args)
        elif cmd == 'remove' or cmd == 'rm' or cmd == 'delete':
            self.cmd_remove(args)
        elif cmd == 'list' or cmd == 'ls':
            self.cmd_list()
        elif cmd == 'field' or cmd == 'e':
            self.cmd_field(args)
        elif cmd == 'potential' or cmd == 'v':
            self.cmd_potential(args)
        elif cmd == 'clear':
            self.cmd_clear()
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")
    
    def run(self) -> None:
        """Run the interactive CLI loop."""
        print("\n" + "="*60)
        print("  Multi-Charge Electric Field Calculator")
        print("  Type 'help' for available commands, 'quit' to exit")
        print("="*60 + "\n")
        
        while self.running:
            try:
                line = input("field-calc> ")
                self.process_command(line)
            except KeyboardInterrupt:
                print("\nUse 'quit' or 'exit' to exit.")
            except EOFError:
                self.running = False
                print("\nGoodbye!")


def parse_args():
    """Parse command-line arguments for non-interactive mode."""
    parser = argparse.ArgumentParser(
        description='Multi-Charge Electric Field Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    field-calc
    
  Calculate field from charges defined in arguments:
    field-calc --charges "0,0,0,1e-9;old,0,0,-1e-9" --field 0.5,0,0
    
  Calculate potential:
    field-calc --charges "0,0,0,1e-9" --potential old,0,0
"""
    )
    
    parser.add_argument(
        '--charges', '-c',
        type=str,
        help='Charges in format "x1,y1,z1,q1;x2,y2,z2,q2;..."'
    )
    
    parser.add_argument(
        '--field', '-f',
        type=str,
        help='Calculate field at point "x,y,z"'
    )
    
    parser.add_argument(
        '--potential', '-p',
        type=str,
        help='Calculate potential at point "x,y,z"'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Start interactive mode (default if no other args)'
    )
    
    return parser.parse_args()


def parse_charges(charges_str: str) -> list:
    """
    Parse charges string into list of tuples.
    
    Args:
        charges_str: String in format "x1,y1,z1,q1;x2,y2,z2,q2;..."
    
    Returns:
        List of (x, y, z, q) tuples
    """
    charges = []
    for charge_str in charges_str.split(';'):
        parts = charge_str.strip().split(',')
        if len(parts) != 4:
            raise ValueError(f"Invalid charge format: '{charge_str}'. Expected 'x,y,z,q'")
        x, y, z, q = float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
        charges.append((x, y, z, q))
    return charges


def parse_point(point_str: str) -> tuple:
    """
    Parse point string into tuple.
    
    Args:
        point_str: String in format "x,y,z"
    
    Returns:
        Tuple (x, y, z)
    """
    parts = point_str.strip().split(',')
    if len(parts) != 3:
        raise ValueError(f"Invalid point format: '{point_str}'. Expected 'x,y,z'")
    return float(parts[0]), float(parts[1]), float(parts[2])


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # If no specific action requested, start interactive mode
    if not args.charges and not args.field and not args.potential:
        cli = InteractiveCLI()
        cli.run()
        return
    
    # Non-interactive mode
    system = ChargeSystem()
    
    # Add charges if provided
    if args.charges:
        try:
            charges = parse_charges(args.charges)
            for x, y, z, q in charges:
                charge_id = system.add_charge(x, y, z, q)
                print(f"Added charge ID {charge_id}: ({x}, {y}, {z}), q={q:.2e} C")
        except ValueError as e:
            print(f"Error parsing charges: {e}")
            sys.exit(1)
    
    # Calculate field if requested
    if args.field:
        try:
            x, y, z = parse_point(args.field)
            Ex, Ey, Ez = system.electric_field_at(x, y, z)
            E_mag = system.electric_field_magnitude_at(x, y, z)
            print(f"\nElectric Field at ({x}, {y}, {z}):")
            print(f"  E = ({Ex:.4e}, {Ey:.4e}, {Ez:.4e}) N/C")
            print(f"  |E| = {E_mag:.4e} N/C")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    # Calculate potential if requested
    if args.potential:
        try:
            x, y, z = parse_point(args.potential)
            V = system.potential_at(x, y, z)
            print(f"\nElectric Potential at ({x}, {y}, {z}):")
            print(f"  V = {V:.4e} V")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
