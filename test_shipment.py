# Unit tests using the unittest framework
import unittest
from shipment import parse_line, process_shipments  # Import the functions to be tested

class TestShipmentProcessing(unittest.TestCase):
    """Test cases for shipment processing logic."""

    def test_parse_valid_line(self):
        """Test that a valid input line is parsed correctly."""
        self.assertEqual(parse_line("2015-02-01 S MR"), (((2015, 2, 1), 'S', 'MR'), None))
    
    def test_parse_invalid_date(self):
        """Test that an invalid date format results in an 'Ignored' response."""
        self.assertEqual(parse_line("invalid-date S MR"), (None, "Ignored"))
    
    def test_parse_invalid_format(self):
        """Test that a missing provider in the input results in an 'Ignored' response."""
        self.assertEqual(parse_line("2015-02-01 S"), (None, "Ignored"))
    
    def test_parse_unknown_provider(self):
        """Test that an unknown provider results in an 'Ignored' response."""
        self.assertEqual(parse_line("2015-02-01 S XYZ"), (None, "Ignored"))
    
    def test_discount_rule_s_price(self):
        """Test that the discount rule is correctly applied for small shipments (S) via MR provider."""
        shipments = ["2015-02-01 S MR"]
        
        # Create a temporary input file for testing
        with open("test_input.txt", "w") as f:
            f.write("\n".join(shipments))
        
        # Process the input file
        output = process_shipments("test_input.txt")
        
        # The expected output should contain "1.50 0.50" (original price, discount applied)
        self.assertIn("1.50 0.50", output[0])
    
    def test_third_large_lp_free(self):
        """Test that the third large LP shipment in a month is free (0.00)."""
        shipments = [
            "2015-02-01 L LP",
            "2015-02-02 L LP",
            "2015-02-03 L LP"  # This should be free
        ]
        
        # Create a temporary input file for testing
        with open("test_input.txt", "w") as f:
            f.write("\n".join(shipments))
        
        # Process the input file
        output = process_shipments("test_input.txt")
        
        # The third shipment should have "0.00" as the price, and "6.90" as the discount
        self.assertIn("0.00 6.90", output[2])
    
    def test_monthly_discount_cap(self):
        """Test that the monthly discount does not exceed 10€."""
        shipments = ["2015-02-01 S MR"] * 30  # More than enough to exceed the 10€ discount cap
        
        # Create a temporary input file for testing
        with open("test_input.txt", "w") as f:
            f.write("\n".join(shipments))
        
        # Process the input file
        output = process_shipments("test_input.txt")
        
        # Calculate total discount by summing up the last column (discount values)
        total_discount = sum(float(line.split()[-1]) if line.split()[-1] != "-" else 0 for line in output)
        
        # The total discount should not exceed 10€
        self.assertLessEqual(total_discount, 10.00)

if __name__ == "__main__":
    unittest.main()
