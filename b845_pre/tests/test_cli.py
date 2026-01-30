"""
Tests for the CLI module of field_calc.

This module tests:
- Interactive CLI command processing
- Command-line argument parsing
- Input validation
- Output formatting
"""

import pytest
from io import StringIO
from unittest.mock import patch
from field_calc.cli import InteractiveCLI, parse_charges, parse_point


class TestInteractiveCLI:
    """Tests for the InteractiveCLI class."""
    
    @pytest.fixture
    def cli(self):
        """Create a fresh CLI instance for each test."""
        return InteractiveCLI()
    
    def test_cli_initialization(self, cli):
        """Test CLI initializes with empty system."""
        assert cli.system.charge_count() == 0
        assert cli.running == True
    
    def test_cmd_add_valid(self, cli):
        """Test adding a charge with valid arguments."""
        cli.cmd_add(['0', '0', '0', '1e-9'])
        assert cli.system.charge_count() == 1
    
    def test_cmd_add_invalid_args_count(self, cli, capsys):
        """Test add command with wrong number of arguments."""
        cli.cmd_add(['0', '0', '0'])  # Missing q
        captured = capsys.readouterr()
        assert "requires 4 arguments" in captured.out
        assert cli.system.charge_count() == 0
    
    def test_cmd_add_invalid_number(self, cli, capsys):
        """Test add command with non-numeric argument."""
        cli.cmd_add(['0', '0', '0', 'abc'])
        captured = capsys.readouterr()
        assert "must be numbers" in captured.out
        assert cli.system.charge_count() == 0
    
    def test_cmd_remove_valid(self, cli):
        """Test removing a charge with valid ID."""
        charge_id = cli.system.add_charge(0, 0, 0, 1e-9)
        cli.cmd_remove([str(charge_id)])
        assert cli.system.charge_count() == 0
    
    def test_cmd_remove_invalid_id(self, cli, capsys):
        """Test removing a charge with invalid ID."""
        cli.cmd_remove(['999'])
        captured = capsys.readouterr()
        assert "not found" in captured.out
    
    def test_cmd_remove_non_integer(self, cli, capsys):
        """Test remove command with non-integer ID."""
        cli.cmd_remove(['abc'])
        captured = capsys.readouterr()
        assert "must be an integer" in captured.out
    
    def test_cmd_list_empty(self, cli, capsys):
        """Test listing charges when system is empty."""
        cli.cmd_list()
        captured = capsys.readouterr()
        assert "No charges" in captured.out
    
    def test_cmd_list_with_charges(self, cli, capsys):
        """Test listing charges when system has charges."""
        cli.system.add_charge(0, 0, 0, 1e-9)
        cli.system.add_charge(1, 0, 0, -1e-9)
        cli.cmd_list()
        captured = capsys.readouterr()
        assert "Total charges: 2" in captured.out
    
    def test_cmd_field_valid(self, cli, capsys):
        """Test field calculation with valid arguments."""
        cli.system.add_charge(0, 0, 0, 1e-9)
        cli.cmd_field(['old', '0', '0'])
        captured = capsys.readouterr()
        assert "Electric Field" in captured.out
        assert "Ex" in captured.out
    
    def test_cmd_field_empty_system(self, cli, capsys):
        """Test field calculation with no charges."""
        cli.cmd_field(['old', '0', '0'])
        captured = capsys.readouterr()
        assert "No charges" in captured.out or "zero" in captured.out.lower()
    
    def test_cmd_field_invalid_args(self, cli, capsys):
        """Test field command with wrong number of arguments."""
        cli.cmd_field(['old', '0'])  # Missing z
        captured = capsys.readouterr()
        assert "requires 3 arguments" in captured.out
    
    def test_cmd_potential_valid(self, cli, capsys):
        """Test potential calculation with valid arguments."""
        cli.system.add_charge(0, 0, 0, 1e-9)
        cli.cmd_potential(['old', '0', '0'])
        captured = capsys.readouterr()
        assert "Electric Potential" in captured.out
        assert "V =" in captured.out
    
    def test_cmd_potential_empty_system(self, cli, capsys):
        """Test potential calculation with no charges."""
        cli.cmd_potential(['old', '0', '0'])
        captured = capsys.readouterr()
        assert "No charges" in captured.out or "zero" in captured.out.lower()
    
    def test_cmd_clear(self, cli, capsys):
        """Test clearing all charges."""
        cli.system.add_charge(0, 0, 0, 1e-9)
        cli.system.add_charge(1, 0, 0, -1e-9)
        cli.cmd_clear()
        captured = capsys.readouterr()
        assert "Cleared 2" in captured.out
        assert cli.system.charge_count() == 0
    
    def test_process_command_quit(self, cli):
        """Test quit command stops the CLI."""
        cli.process_command('quit')
        assert cli.running == False
    
    def test_process_command_exit(self, cli):
        """Test exit command stops the CLI."""
        cli.process_command('exit')
        assert cli.running == False
    
    def test_process_command_q(self, cli):
        """Test q command stops the CLI."""
        cli.process_command('q')
        assert cli.running == False
    
    def test_process_command_help(self, cli, capsys):
        """Test help command shows help message."""
        cli.process_command('help')
        captured = capsys.readouterr()
        assert "Commands" in captured.out or "add" in captured.out.lower()
    
    def test_process_command_unknown(self, cli, capsys):
        """Test unknown command shows error."""
        cli.process_command('unknown_command')
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out
    
    def test_process_command_empty(self, cli):
        """Test empty command does nothing."""
        cli.process_command('')
        assert cli.running == True
    
    def test_command_aliases_rm(self, cli):
        """Test rm alias for remove."""
        charge_id = cli.system.add_charge(0, 0, 0, 1e-9)
        cli.process_command(f'rm {charge_id}')
        assert cli.system.charge_count() == 0
    
    def test_command_aliases_ls(self, cli, capsys):
        """Test ls alias for list."""
        cli.process_command('ls')
        captured = capsys.readouterr()
        assert "No charges" in captured.out
    
    def test_command_aliases_e(self, cli, capsys):
        """Test e alias for field."""
        cli.system.add_charge(0, 0, 0, 1e-9)
        cli.process_command('e old 0 0')
        captured = capsys.readouterr()
        assert "Electric Field" in captured.out
    
    def test_command_aliases_v(self, cli, capsys):
        """Test v alias for potential."""
        cli.system.add_charge(0, 0, 0, 1e-9)
        cli.process_command('v old 0 0')
        captured = capsys.readouterr()
        assert "Electric Potential" in captured.out


class TestParsingFunctions:
    """Tests for parsing helper functions."""
    
    def test_parse_charges_single(self):
        """Test parsing a single charge."""
        charges = parse_charges("0,0,0,1e-9")
        assert len(charges) == 1
        assert charges[0] == (0.0, 0.0, 0.0, 1e-9)
    
    def test_parse_charges_multiple(self):
        """Test parsing multiple charges."""
        charges = parse_charges("0,0,0,1e-9;old,0,0,-1e-9")
        assert len(charges) == 2
        assert charges[0] == (0.0, 0.0, 0.0, 1e-9)
        assert charges[1] == (1.0, 0.0, 0.0, -1e-9)
    
    def test_parse_charges_invalid_format(self):
        """Test parsing charges with invalid format."""
        with pytest.raises(ValueError) as excinfo:
            parse_charges("0,0,0")  # Missing q
        assert "Invalid charge format" in str(excinfo.value)
    
    def test_parse_point_valid(self):
        """Test parsing a valid point."""
        point = parse_point("old,2,3")
        assert point == (1.0, 2.0, 3.0)
    
    def test_parse_point_invalid_format(self):
        """Test parsing a point with invalid format."""
        with pytest.raises(ValueError) as excinfo:
            parse_point("old,2")  # Missing z
        assert "Invalid point format" in str(excinfo.value)
    
    def test_parse_point_with_spaces(self):
        """Test parsing a point with spaces."""
        point = parse_point(" old , 2 , 3 ")
        assert point == (1.0, 2.0, 3.0)
    
    def test_parse_charges_with_spaces(self):
        """Test parsing charges with spaces."""
        charges = parse_charges(" 0 , 0 , 0 , 1e-9 ; old , 0 , 0 , -1e-9 ")
        assert len(charges) == 2


class TestCLIIntegration:
    """Integration tests for CLI functionality."""
    
    @pytest.fixture
    def cli(self):
        """Create a fresh CLI instance for each test."""
        return InteractiveCLI()
    
    def test_add_and_calculate_field(self, cli, capsys):
        """Test adding charges and calculating field."""
        cli.process_command('add 0 0 0 1e-9')
        cli.process_command('add 2 0 0 1e-9')
        cli.process_command('field old 0 0')
        
        captured = capsys.readouterr()
        assert "Electric Field" in captured.out
    
    def test_add_remove_calculate(self, cli, capsys):
        """Test adding, removing, and calculating."""
        cli.process_command('add 0 0 0 1e-9')
        cli.process_command('add old 0 0 -1e-9')
        cli.process_command('remove old')
        cli.process_command('field 0.5 0 0')
        
        captured = capsys.readouterr()
        # After removing charge old, only charge 2 remains
        assert "Electric Field" in captured.out
    
    def test_workflow_dipole(self, cli, capsys):
        """Test complete workflow with a dipole."""
        # Create dipole
        cli.process_command('add -0.5 0 0 1e-9')
        cli.process_command('add 0.5 0 0 -1e-9')
        
        # List charges
        cli.process_command('list')
        
        # Calculate field at origin
        cli.process_command('field 0 0 0')
        
        # Calculate potential at origin (should be ~0)
        cli.process_command('potential 0 0 0')
        
        captured = capsys.readouterr()
        assert "Total charges: 2" in captured.out
        assert "Electric Field" in captured.out
        assert "Electric Potential" in captured.out
    
    def test_clear_and_recalculate(self, cli, capsys):
        """Test clearing charges and recalculating."""
        cli.process_command('add 0 0 0 1e-9')
        cli.process_command('clear')
        cli.process_command('field old 0 0')
        
        captured = capsys.readouterr()
        assert "Cleared" in captured.out
        # Field should be zero after clearing
        assert "zero" in captured.out.lower() or "No charges" in captured.out


class TestErrorHandling:
    """Tests for error handling in CLI."""
    
    @pytest.fixture
    def cli(self):
        """Create a fresh CLI instance for each test."""
        return InteractiveCLI()
    
    def test_field_at_charge_position(self, cli, capsys):
        """Test error when calculating field at charge position."""
        cli.process_command('add 0 0 0 1e-9')
        cli.process_command('field 0 0 0')
        
        captured = capsys.readouterr()
        assert "Error" in captured.out or "coincides" in captured.out
    
    def test_potential_at_charge_position(self, cli, capsys):
        """Test error when calculating potential at charge position."""
        cli.process_command('add 0 0 0 1e-9')
        cli.process_command('potential 0 0 0')
        
        captured = capsys.readouterr()
        assert "Error" in captured.out or "coincides" in captured.out
    
    def test_invalid_number_format(self, cli, capsys):
        """Test error with invalid number format."""
        cli.process_command('add 0 0 0 not_a_number')
        
        captured = capsys.readouterr()
        assert "must be numbers" in captured.out
