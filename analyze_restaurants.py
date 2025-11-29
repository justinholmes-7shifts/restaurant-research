#!/usr/bin/env python3
"""
Restaurant Lead Analysis Script
Analyzes restaurant data to identify:
1. Restaurants with staffing indicators
2. Lead quality and potential
3. Decision-maker contact information
4. Scheduling decision-makers
"""

import csv
import re
from collections import defaultdict
from typing import Dict, List, Tuple

# Decision-maker titles that indicate scheduling authority
SCHEDULING_DECISION_MAKERS = [
    'owner', 'ceo', 'president', 'general manager', 'gm',
    'director of operations', 'operations manager', 'operating partner',
    'regional manager', 'district manager', 'managing partner'
]

# Titles that might have scheduling input but less authority
SCHEDULING_INFLUENCERS = [
    'manager', 'assistant manager', 'shift manager',
    'hr manager', 'human resources'
]

def is_scheduling_decision_maker(title: str) -> Tuple[bool, str]:
    """
    Check if title indicates scheduling decision-making authority.
    Returns (is_decision_maker, level)
    """
    if not title or title == 'N/A':
        return False, 'none'

    title_lower = title.lower().strip()

    for dm_title in SCHEDULING_DECISION_MAKERS:
        if dm_title in title_lower:
            return True, 'primary'

    for inf_title in SCHEDULING_INFLUENCERS:
        if inf_title in title_lower:
            return True, 'secondary'

    return False, 'none'

def calculate_lead_score(row: Dict) -> int:
    """
    Calculate lead quality score (0-100)
    Based on: contact info, decision maker, website status, reviews
    """
    score = 0

    # Has valid email (30 points)
    if row.get('Email') and row['Email'] != 'N/A' and row.get('Mailtester') == 'Valid Email':
        score += 30

    # Has decision maker contact (25 points)
    is_dm, level = is_scheduling_decision_maker(row.get('Title', ''))
    if is_dm and level == 'primary':
        score += 25
    elif is_dm and level == 'secondary':
        score += 15

    # Working website (15 points)
    if row.get('Website Status') == 'Web Working':
        score += 15

    # Has phone number (10 points)
    if row.get('Phone') and row['Phone'] != 'N/A':
        score += 10

    # Review count indicates size/activity (10 points)
    try:
        reviews = int(row.get('Reviews Count', 0) or 0)
        if reviews > 1000:
            score += 10
        elif reviews > 500:
            score += 7
        elif reviews > 100:
            score += 5
        elif reviews > 50:
            score += 3
    except (ValueError, TypeError):
        pass

    # Has LinkedIn profile (5 points)
    if row.get('Person Linkedin') and row['Person Linkedin'] != 'N/A' and 'linkedin.com' in row['Person Linkedin']:
        score += 5

    # Rating indicates operational quality (5 points)
    try:
        rating = float(row.get('Rating', 0) or 0)
        if rating >= 4.0:
            score += 5
        elif rating >= 3.5:
            score += 3
    except (ValueError, TypeError):
        pass

    return min(score, 100)

def analyze_staffing_indicators(row: Dict) -> List[str]:
    """
    Identify potential staffing pain points/indicators
    """
    indicators = []

    # Low rating could indicate operational issues
    try:
        rating = float(row.get('Rating', 0) or 0)
        if rating and rating < 3.5:
            indicators.append('Low rating (potential ops/staffing issues)')
    except (ValueError, TypeError):
        pass

    # Multiple locations might indicate growth/staffing needs
    company_name = row.get('Company Name', '')
    if any(term in company_name.lower() for term in ['#', 'location', 'branch']):
        indicators.append('Multi-location operation')

    # Chain restaurants often have staffing challenges
    if row.get('Website Status') == 'Duplicate Company':
        indicators.append('Chain/franchise (standardized scheduling needs)')

    # High review count suggests high volume
    try:
        reviews = int(row.get('Reviews Count', 0) or 0)
        if reviews > 2000:
            indicators.append('High volume (2000+ reviews)')
        elif reviews > 1000:
            indicators.append('Medium-high volume (1000+ reviews)')
    except (ValueError, TypeError):
        pass

    return indicators

def main():
    print("Restaurant Lead Analysis")
    print("=" * 80)

    # Read CSV
    restaurants = []
    with open('restaurants_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            restaurants.append(row)

    print(f"\nTotal restaurants: {len(restaurants)}")

    # Analysis
    high_quality_leads = []
    decision_makers = []
    staffing_indicators = []

    city_breakdown = defaultdict(int)

    for restaurant in restaurants:
        # Calculate lead score
        score = calculate_lead_score(restaurant)

        # Get city
        address = restaurant.get('Address', '')
        city = ''
        if ', TX,' in address:
            city = 'Dallas area'
        elif ', FL,' in address or 'Miami' in address:
            city = 'Miami area'
        elif ', PA,' in address or 'Philadelphia' in address or 'Philidelphia' in address:
            city = 'Philadelphia area'
        elif ', GA,' in address or 'Atlanta' in address or 'Atlantla' in address:
            city = 'Atlanta area'
        else:
            city = 'Other'

        city_breakdown[city] += 1

        # Staffing indicators
        indicators = analyze_staffing_indicators(restaurant)

        # Check if has decision maker
        is_dm, dm_level = is_scheduling_decision_maker(restaurant.get('Title', ''))

        # Compile results
        result = {
            'name': restaurant.get('Company Name', 'N/A'),
            'score': score,
            'city': city,
            'address': restaurant.get('Address', 'N/A'),
            'phone': restaurant.get('Phone', 'N/A'),
            'email': restaurant.get('Email', 'N/A'),
            'company_email': restaurant.get('Company Generic Emails', 'N/A'),
            'title': restaurant.get('Title', 'N/A'),
            'first_name': restaurant.get('First Name', 'N/A'),
            'last_name': restaurant.get('Last Name', 'N/A'),
            'linkedin': restaurant.get('Person Linkedin', 'N/A'),
            'website': restaurant.get('Website', 'N/A'),
            'rating': restaurant.get('Rating', 'N/A'),
            'reviews': restaurant.get('Reviews Count', 'N/A'),
            'is_decision_maker': is_dm,
            'dm_level': dm_level,
            'staffing_indicators': indicators,
            'email_valid': restaurant.get('Mailtester') == 'Valid Email'
        }

        # High quality leads (score >= 60)
        if score >= 60:
            high_quality_leads.append(result)

        # Has decision maker contact
        if is_dm and dm_level == 'primary':
            decision_makers.append(result)

        # Has staffing indicators
        if indicators:
            staffing_indicators.append(result)

    # Sort by score
    high_quality_leads.sort(key=lambda x: x['score'], reverse=True)
    decision_makers.sort(key=lambda x: x['score'], reverse=True)

    # Generate Report
    print("\n" + "=" * 80)
    print("CITY BREAKDOWN")
    print("=" * 80)
    for city, count in sorted(city_breakdown.items(), key=lambda x: x[1], reverse=True):
        print(f"{city:30s}: {count:4d} restaurants")

    print("\n" + "=" * 80)
    print(f"HIGH QUALITY LEADS (Score >= 60): {len(high_quality_leads)}")
    print("=" * 80)
    print(f"\nTop 20 leads with decision-maker contacts:\n")

    dm_high_quality = [l for l in high_quality_leads if l['is_decision_maker'] and l['dm_level'] == 'primary']

    for i, lead in enumerate(dm_high_quality[:20], 1):
        print(f"{i}. {lead['name']}")
        print(f"   Score: {lead['score']}/100")
        print(f"   Contact: {lead['first_name']} {lead['last_name']} - {lead['title']}")
        print(f"   Email: {lead['email']} {'✓' if lead['email_valid'] else ''}")
        if lead['company_email'] != 'N/A':
            print(f"   Company Email: {lead['company_email']}")
        print(f"   Phone: {lead['phone']}")
        print(f"   City: {lead['city']}")
        print(f"   Rating: {lead['rating']} ({lead['reviews']} reviews)")
        if lead['staffing_indicators']:
            print(f"   Staffing Indicators: {', '.join(lead['staffing_indicators'])}")
        print()

    print("\n" + "=" * 80)
    print(f"DECISION MAKERS IDENTIFIED: {len(decision_makers)}")
    print("=" * 80)
    print(f"\nBreakdown by title:\n")

    title_counts = defaultdict(int)
    for dm in decision_makers:
        title_counts[dm['title']] += 1

    for title, count in sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"{title:40s}: {count:3d}")

    print("\n" + "=" * 80)
    print(f"RESTAURANTS WITH STAFFING INDICATORS: {len(staffing_indicators)}")
    print("=" * 80)

    # Count indicator types
    indicator_counts = defaultdict(int)
    for restaurant in staffing_indicators:
        for indicator in restaurant['staffing_indicators']:
            indicator_counts[indicator] += 1

    print("\nStaffing indicator breakdown:\n")
    for indicator, count in sorted(indicator_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{indicator:50s}: {count:4d}")

    # Export high quality leads with decision makers to CSV
    print("\n" + "=" * 80)
    print("EXPORTING RESULTS")
    print("=" * 80)

    with open('high_quality_leads.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'score', 'city', 'address', 'phone', 'email', 'company_email',
                     'title', 'first_name', 'last_name', 'linkedin', 'website', 'rating',
                     'reviews', 'dm_level', 'staffing_indicators', 'email_valid']
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for lead in high_quality_leads:
            lead_copy = lead.copy()
            lead_copy['staffing_indicators'] = '; '.join(lead_copy['staffing_indicators'])
            writer.writerow(lead_copy)

    print(f"✓ Exported {len(high_quality_leads)} high quality leads to high_quality_leads.csv")

    # Export decision makers separately
    with open('scheduling_decision_makers.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'score', 'city', 'address', 'phone', 'email', 'company_email',
                     'title', 'first_name', 'last_name', 'linkedin', 'website', 'rating',
                     'reviews', 'email_valid']
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(decision_makers)

    print(f"✓ Exported {len(decision_makers)} decision makers to scheduling_decision_makers.csv")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total restaurants analyzed: {len(restaurants)}")
    print(f"High quality leads (60+ score): {len(high_quality_leads)}")
    print(f"Decision makers with contact info: {len(decision_makers)}")
    print(f"High quality leads WITH decision makers: {len(dm_high_quality)}")
    print(f"Restaurants with staffing indicators: {len(staffing_indicators)}")
    print()

if __name__ == '__main__':
    main()
