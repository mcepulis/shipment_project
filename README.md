
# Shipping Cost Calculator  

## Description  
This Python script calculates shipping costs based on predefined pricing rules and applies discounts according to specific conditions:  

- The lowest price for a small package is always applied.  
- The third large package shipped via LP within a month is free.  
- The total discount in a month cannot exceed **€10**.  

The script reads shipment data from a text file, processes it, and outputs the calculated cost along with any applied discounts.  

## How It Works  
1. **Reads input from `input.txt`**  
   - Each line represents a shipment with date, size (S, M, L), and provider (LP, MR).  
2. **Applies discount rules** based on predefined conditions.  
3. **Outputs results** with calculated prices and discounts.  

## Installation  
1. Clone the repository:  
   ```sh
   git clone https://github.com/mcepulis/shipment_project.git
   ```  
2. Navigate to the project directory:  
   ```sh
   cd shipment_project
   ```  
3. Ensure Python is installed on your system.  

## Usage  
Run the script with:  
```sh
python shipment.py
```  
The output format is:  
```
YYYY-MM-DD SIZE PROVIDER FINAL_PRICE DISCOUNT  
```  
where `DISCOUNT` is either the applied discount amount or `-` if no discount was applied.  

## Example Input (`input.txt`)  
```txt
2015-02-01 S MR  
2015-02-02 M LP  
2015-02-03 L LP  
2015-02-04 L LP  
2015-02-05 L LP  
```  

## Example Output  
```txt
2015-02-01 S MR 1.50 0.50  
2015-02-02 M LP 4.90 -  
2015-02-03 L LP 6.90 -  
2015-02-04 L LP 6.90 -  
2015-02-05 L LP 0.00 6.90  # Third large LP shipment is free  
```  

## Running Tests  
To ensure correctness, run:  
```sh
python -m unittest test_shipment.py
```  

## License  
This project is licensed under the MIT License.  

## Author  
Created by **Marius Cepulis**.  
