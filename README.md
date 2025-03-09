# Shipping Cost Calculator with Discounts

## Overview
This Python script calculates shipping costs based on predefined price rules for different providers (`LP`, `MR`) and package sizes (`S`, `M`, `L`). It applies discount rules such as:  
- Matching the lowest price for small (`S`) shipments.  
- Making the third large (`L`) shipment via `LP` in a month free.  
- Capping total monthly discounts at **€10**.  

The script reads input from a text file containing shipments and outputs the calculated costs with applied discounts.

## Features
✔ Parses shipment data from a text file.  
✔ Applies discount rules automatically.  
✔ Ensures monthly discount cap.  
✔ Provides clear output in a structured format.  
✔ Includes unit tests for validation.  

## Installation
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-username/shipping-cost-calculator.git
