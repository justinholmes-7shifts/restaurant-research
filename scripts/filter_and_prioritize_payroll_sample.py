#!/usr/bin/env python3
"""
Filter non-restaurants and prioritize for payroll research.
Score based on:
- Multi-location operators (higher complexity)
- Known restaurant groups (vs single locations)
- Established concepts (vs new/unknown)
"""

import csv

input_file = "/Users/justin.holmes/Restaurant Research/payroll_research_sample_50.csv"
output_file = "/Users/justin.holmes/Restaurant Research/payroll_research_top_5.csv"

# Read the sample
restaurants = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Location Name']:  # Skip empty rows
            restaurants.append(row)

print(f"Total entries: {len(restaurants)}")

# Filter out non-restaurants
non_restaurants = ['Bong Bros 12 Smoke Shop', 'Studio 183 Lounge', 'HGVJGJ', 'Museum of Ice Cream']
filtered = [r for r in restaurants if r['Location Name'] not in non_restaurants and r['Location Name'].strip()]

print(f"After filtering non-restaurants: {len(filtered)}")

# Score each restaurant for research priority
def calculate_priority_score(restaurant):
    score = 0
    company = restaurant['Company Name - Active Companies']
    location = restaurant['Location Name']

    # Multi-location operators (40 pts)
    multi_location_indicators = [
        'Sushi Sake Corporate',  # Multiple locations in sample
        'Bondi Sushi',  # Multiple locations in sample
        '(Miami) MCA-Airports',  # Airport group
        'Gastronomica Restaurant Group',
        'Ariete Hospitality Group',
        'Groot Hospitality',
        'CVI.CHE 105',
        'South Region - Anthony\'s Coal Fired Pizza',
        'V&E - Marabu',
        'Dos Croquetas',
        'Black Market',
        'Estefan Enterprises',
        'Fire Pit Hospitality',
        'SHAHS OF KABOB',
        'Japan Inn',
        'Nothing Bundt Cakes',
        'OL\'DAYS',
        'Mother Wolf',
        'SEXY FISH',
        'Talkin Tacos'
    ]

    if any(indicator in company for indicator in multi_location_indicators):
        score += 40

    # Known high-end/established brands (20 pts)
    premium_brands = ['Sexy Fish', 'Mother Wolf', 'Seaspice', 'Ariete', 'Yamashiro',
                      'Estefan Kitchen', 'Anthony\'s Coal Fired', 'Benihana']
    if any(brand in location for brand in premium_brands):
        score += 20

    # Chain/franchise operations (30 pts for complexity)
    chains = ['Sushi Sake', 'Anthony\'s Coal Fired', 'Benihana', 'Nothing Bundt Cakes',
              'Bondi Sushi', 'Dos Croquetas', 'Japan Inn']
    if any(chain in company or chain in location for chain in chains):
        score += 30

    # Airport locations (10 pts - complex operations)
    if 'Airport' in company or 'MIA-' in location:
        score += 10

    return score

# Score all restaurants
for restaurant in filtered:
    restaurant['priority_score'] = calculate_priority_score(restaurant)

# Sort by priority score
filtered.sort(key=lambda x: x['priority_score'], reverse=True)

print("\n=== TOP 10 BY PRIORITY SCORE ===")
for i, r in enumerate(filtered[:10], 1):
    print(f"{i}. [{r['priority_score']} pts] {r['Location Name']} ({r['Company Name - Active Companies']})")

# Select top 5
top_5 = filtered[:5]

print(f"\n=== SELECTED TOP 5 FOR RESEARCH ===")
for i, r in enumerate(top_5, 1):
    print(f"{i}. [{r['priority_score']} pts] {r['Location Name']} ({r['Company Name - Active Companies']})")
    print(f"   Address: {r['Location Address']}")
    print()

# Save to CSV
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['Company Name - Active Companies', 'Location Name', 'Location Address', 'priority_score']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(top_5)

print(f"Saved top 5 to: {output_file}")
