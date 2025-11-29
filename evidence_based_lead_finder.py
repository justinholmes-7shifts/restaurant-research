#!/usr/bin/env python3
"""
Evidence-Based Lead Finder
Identifies restaurants with ACTUAL staffing evidence, not assumptions.

Based on learnings from manual research:
- High volume ≠ staffing problems
- Need to look for: job postings, employee reviews, customer complaints
- Focus on restaurants where we have decision-maker contacts
"""

import csv
import json
from typing import Dict, List, Set
from collections import defaultdict

# Staffing evidence keywords to look for in descriptions/reviews
STAFFING_KEYWORDS = {
    'urgent': ['hiring now', 'immediate hire', 'join our team', 'now hiring', 'apply today', 'careers'],
    'understaffed': ['understaffed', 'short staffed', 'short-staffed', 'not enough staff'],
    'slow_service': ['slow service', 'long wait', 'waited forever', 'took forever'],
    'turnover': ['high turnover', 'constant turnover', 'always hiring'],
    'scheduling': ['scheduling issues', 'schedule problems', 'bad scheduling']
}

# Decision maker titles with scheduling authority
PRIMARY_DECISION_MAKERS = [
    'owner', 'ceo', 'president', 'general manager', 'gm',
    'director of operations', 'operations manager', 'operating partner',
    'regional manager', 'district manager', 'managing partner'
]

def is_decision_maker(title: str) -> bool:
    """Check if title indicates scheduling decision-making authority."""
    if not title or title == 'N/A':
        return False

    title_lower = title.lower().strip()
    return any(dm_title in title_lower for dm_title in PRIMARY_DECISION_MAKERS)

def has_valid_contact(row: Dict) -> bool:
    """Check if restaurant has valid decision-maker contact info."""
    has_email = row.get('Email') and row['Email'] != 'N/A' and row.get('Mailtester') == 'Valid Email'
    has_dm = is_decision_maker(row.get('Title', ''))
    return has_email and has_dm

def check_description_for_keywords(description: str) -> Dict[str, List[str]]:
    """Scan description for staffing-related keywords."""
    if not description or description == 'N/A':
        return {}

    description_lower = description.lower()
    found = defaultdict(list)

    for category, keywords in STAFFING_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description_lower:
                found[category].append(keyword)

    return dict(found)

def calculate_research_priority(row: Dict) -> int:
    """
    Calculate priority for manual research (0-100).
    Higher score = research this one first.
    """
    score = 0

    # Has decision maker with valid email (50 points)
    if has_valid_contact(row):
        score += 50

    # Has phone number (10 points)
    if row.get('Phone') and row['Phone'] != 'N/A':
        score += 10

    # Has LinkedIn profile (10 points)
    if row.get('Person Linkedin') and 'linkedin.com' in row.get('Person Linkedin', ''):
        score += 10

    # High review count suggests established operation (10 points)
    try:
        reviews = int(row.get('Reviews Count', 0) or 0)
        if reviews > 500:
            score += 10
        elif reviews > 100:
            score += 5
    except (ValueError, TypeError):
        pass

    # Working website (10 points)
    if row.get('Website Status') == 'Web Working':
        score += 10

    # Keywords in description (10 points)
    keywords = check_description_for_keywords(row.get('Description', ''))
    if keywords:
        score += 10

    return score

def main():
    print("Evidence-Based Lead Finder")
    print("=" * 80)

    # Read CSV
    restaurants = []
    with open('restaurants_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            restaurants.append(row)

    print(f"\nTotal restaurants: {len(restaurants)}")

    # Prioritize for research
    research_candidates = []

    for restaurant in restaurants:
        priority = calculate_research_priority(restaurant)

        # Only include restaurants worth researching (priority >= 60)
        if priority >= 60:
            research_candidates.append({
                'name': restaurant.get('Company Name', 'N/A'),
                'priority_score': priority,
                'address': restaurant.get('Address', 'N/A'),
                'phone': restaurant.get('Phone', 'N/A'),
                'email': restaurant.get('Email', 'N/A'),
                'title': restaurant.get('Title', 'N/A'),
                'first_name': restaurant.get('First Name', 'N/A'),
                'last_name': restaurant.get('Last Name', 'N/A'),
                'website': restaurant.get('Website', 'N/A'),
                'rating': restaurant.get('Rating', 'N/A'),
                'reviews': restaurant.get('Reviews Count', 'N/A'),
                'description': restaurant.get('Description', 'N/A'),
                'keywords_found': check_description_for_keywords(restaurant.get('Description', ''))
            })

    # Sort by priority
    research_candidates.sort(key=lambda x: x['priority_score'], reverse=True)

    print(f"\nResearch Candidates (Priority >= 60): {len(research_candidates)}")
    print("\n" + "=" * 80)
    print("TOP 50 PRIORITY RESTAURANTS FOR MANUAL RESEARCH")
    print("=" * 80)
    print("\nThese have decision-maker contacts and should be researched for:")
    print("1. Active job postings (Indeed, LinkedIn, company website)")
    print("2. Employee reviews mentioning scheduling/staffing")
    print("3. Customer reviews mentioning slow service/understaffing")
    print("\n")

    for i, candidate in enumerate(research_candidates[:50], 1):
        print(f"{i}. {candidate['name']}")
        print(f"   Priority Score: {candidate['priority_score']}/100")
        print(f"   Contact: {candidate['first_name']} {candidate['last_name']} - {candidate['title']}")
        print(f"   Email: {candidate['email']}")
        print(f"   Phone: {candidate['phone']}")

        # Show city
        address = candidate['address']
        if ', TX,' in address:
            city = 'Dallas/TX'
        elif ', FL,' in address:
            city = 'Miami/FL'
        elif ', PA,' in address:
            city = 'Philadelphia/PA'
        elif ', GA,' in address:
            city = 'Atlanta/GA'
        else:
            city = 'Other'
        print(f"   Location: {city}")

        print(f"   Rating: {candidate['rating']} ({candidate['reviews']} reviews)")

        if candidate['keywords_found']:
            print(f"   🔍 Keywords in description: {candidate['keywords_found']}")

        print()

    # Export to CSV for tracking research
    with open('research_priority_list.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['priority_rank', 'name', 'priority_score', 'contact_name', 'title',
                     'email', 'phone', 'address', 'website', 'rating', 'reviews',
                     'research_status', 'evidence_found', 'staffing_pain_score', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, candidate in enumerate(research_candidates, 1):
            writer.writerow({
                'priority_rank': i,
                'name': candidate['name'],
                'priority_score': candidate['priority_score'],
                'contact_name': f"{candidate['first_name']} {candidate['last_name']}",
                'title': candidate['title'],
                'email': candidate['email'],
                'phone': candidate['phone'],
                'address': candidate['address'],
                'website': candidate['website'],
                'rating': candidate['rating'],
                'reviews': candidate['reviews'],
                'research_status': 'Not Started' if i > 10 else 'Priority',
                'evidence_found': '',
                'staffing_pain_score': '',
                'notes': ''
            })

    print("\n" + "=" * 80)
    print("RESEARCH TRACKING")
    print("=" * 80)
    print(f"✓ Created research_priority_list.csv with {len(research_candidates)} restaurants")
    print("\nThis file has columns for:")
    print("  - research_status: Track 'Not Started', 'In Progress', 'Completed'")
    print("  - evidence_found: 'Yes' or 'No'")
    print("  - staffing_pain_score: Rate 1-10 after research")
    print("  - notes: Add findings")
    print("\nManually research top restaurants using:")
    print("  1. Google: '[Restaurant Name] + jobs' or '[Restaurant Name] + careers'")
    print("  2. Indeed: Search employee reviews")
    print("  3. Glassdoor: Search company reviews")
    print("  4. Yelp/Google Reviews: Look for 'slow service', 'understaffed'")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total restaurants in database: {len(restaurants)}")
    print(f"Worth researching (60+ priority): {len(research_candidates)}")
    print(f"\nRecommendation: Start with top 20, spend 10-15 min per restaurant")
    print(f"Expected outcome: 30-40% will have staffing evidence")
    print(f"Estimated qualified leads from top 50: 15-20 restaurants")

if __name__ == '__main__':
    main()
