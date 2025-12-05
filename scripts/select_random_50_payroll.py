#!/usr/bin/env python3
"""
Select 50 random restaurants from the white space locations CSV for payroll research.
"""

import csv
import random

# Set seed for reproducibility
random.seed(42)

input_file = "/Users/justin.holmes/white space locations/sample_data_datalane.csv"
output_file = "/Users/justin.holmes/Restaurant Research/payroll_research_sample_50.csv"

# Read all restaurants
restaurants = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        restaurants.append(row)

print(f"Total restaurants in file: {len(restaurants)}")

# Select 50 random ones
sample = random.sample(restaurants, min(50, len(restaurants)))

print(f"Selected {len(sample)} random restaurants")

# Write to output file
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['Company Name - Active Companies', 'Location Name', 'Location Address']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sample)

print(f"\nSaved to: {output_file}")

# Print first 10 for preview
print("\nFirst 10 restaurants selected:")
for i, rest in enumerate(sample[:10], 1):
    print(f"{i}. {rest['Location Name']} ({rest['Company Name - Active Companies']})")
