# Shipping price table for different providers and sizes.
# 'LP' and 'MR' are the providers, and 'S', 'M', 'L' are the size options.
PRICES = {
    ('LP', 'S'): 1.50,  
    ('LP', 'M'): 4.90,  
    ('LP', 'L'): 6.90, 
    ('MR', 'S'): 2.00,  
    ('MR', 'M'): 3.00,  
    ('MR', 'L'): 4.00   
}

# Discount rules
MAX_MONTHLY_DISCOUNT = 10.00  # Maximum allowable discount per month
# Lowest price for 'S' size, used for matching rule
LOWEST_S_PRICE = min(price for (provider, size), price in PRICES.items() if size == 'S')

# Function to parse each line from the input file
def parse_line(line):
    parts = line.strip().split()  # Remove leading/trailing spaces and split by whitespace
    if len(parts) != 3:  # Ensure exactly 3 parts: date, size, provider
        return None, "Ignored"  # Invalid format
    
    date_str, size, provider = parts  # Unpack the parts
    
    # Validate date format (YYYY-MM-DD)
    if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
        return None, "Ignored"  # Invalid date format
    
    try:
        # Try converting the date to year, month, day as integers
        year, month, day = map(int, date_str.split('-'))
    except ValueError:
        return None, "Ignored"  # If date cannot be parsed, ignore the line
    
    # Check if the (provider, size) combination exists in the price table
    if (provider, size) not in PRICES:
        return None, "Ignored"  # Invalid provider/size combination
    
    # Ensure size is valid
    if size not in ["S", "M", "L"]:
        return None, "Ignored"  # Invalid size
    
    # Ensure provider is valid
    if provider not in ["MR", "LP"]:
        return None, "Ignored"  # Invalid provider
    
    # Return the parsed data (date tuple, size, provider) if all checks pass
    return ((year, month, day), size, provider), None

# Define rules as functions
def rule_all_s_shipments_match_lowest_price(base_price, size):
    # If size is 'S', apply a discount to match the lowest price for 'S'
    if size == 'S':
        return base_price - LOWEST_S_PRICE  # Return the difference to adjust to the lowest price
    return 0.0  # No discount for other sizes

def rule_third_lp_large_shipment_is_free(base_price, month_key, provider, size, lp_large_counter):
    discount = 0.0
    # If the provider is 'LP' and size is 'L', track large shipments in the month
    if provider == 'LP' and size == 'L':
        if month_key not in lp_large_counter:
            lp_large_counter[month_key] = 0  # Initialize count for the month if not already present
        lp_large_counter[month_key] += 1  # Increment the count for this month
        
        # If this is the 3rd large shipment in the month, apply a discount equal to the base price
        if lp_large_counter[month_key] == 3:
            discount = base_price  # The 3rd shipment is free (full discount)
    return discount

def rule_total_monthly_discount_cap(month_key, discount, monthly_discounts):
    # Calculate how much discount is available for this month
    available_discount = MAX_MONTHLY_DISCOUNT - monthly_discounts.get(month_key, 0)
    # If the discount exceeds the available amount, reduce it to fit the cap
    if discount > available_discount:
        discount = available_discount
    
    # Update the total discount for the month
    monthly_discounts[month_key] = monthly_discounts.get(month_key, 0) + discount
    return discount

# Manage rules and apply them to a shipment
def apply_rules(base_price, size, provider, month_key, lp_large_counter, monthly_discounts):
    discount = 0.0
    
    # Apply rule 1: All 'S' shipments should match the lowest price
    discount += rule_all_s_shipments_match_lowest_price(base_price, size)
    
    # Apply rule 2: Third 'L' shipment via 'LP' in a month is free
    discount += rule_third_lp_large_shipment_is_free(base_price, month_key, provider, size, lp_large_counter)
    
    # Apply rule 3: Total monthly discount cap
    discount = rule_total_monthly_discount_cap(month_key, discount, monthly_discounts)
    return discount

# Main function to process shipments from an input file
def process_shipments(file_path):
    monthly_discounts = {}  # Track discounts for each month
    lp_large_counter = {}   # Track the count of large LP shipments per month
    results = []            # Store the results for output
    
    with open(file_path, 'r') as file:
        for line in file:
            # Parse the line and handle any errors
            parsed, error = parse_line(line)
            if error:
                results.append(f"{line.strip()} {error}")  # Append ignored lines with the error
                continue  # Skip to the next line if there was an error
            
            (year, month, day), size, provider = parsed  # Unpack the parsed data
            base_price = PRICES[(provider, size)]  # Get the base price for this shipment
            month_key = (year, month)  # Use (year, month) as the key for monthly discounts
            
            # Apply all discount rules to calculate the discount
            discount = apply_rules(base_price, size, provider, month_key, lp_large_counter, monthly_discounts)
            
            # Calculate the final price by subtracting the discount from the base price
            final_price = base_price - discount
            
            # Format the discount string (show '-' if no discount)
            discount_str = f"{discount:.2f}" if discount > 0 else "-"
            
            # Append the result in the format: date size provider final_price discount
            results.append(f"{year}-{month:02d}-{day:02d} {size} {provider} {final_price:.2f} {discount_str}")
    
    return results

# Entry point for the script
if __name__ == "__main__":
    file_path = "input.txt"  # Path to the input file
    output = process_shipments(file_path)  # Process the shipments in the file
    for line in output:
        print(line)  # Print the output results
