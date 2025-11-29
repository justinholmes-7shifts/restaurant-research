# Restaurant Research

A project for researching restaurant staffing challenges and workforce management needs across Dallas, Miami, Atlanta, and Philadelphia metropolitan areas.

## Overview

This project analyzes 8,598 restaurants to identify high-quality leads for workforce management and scheduling solutions. Using automated lead scoring and decision-maker identification, we've identified 2,222 premium leads with direct contact information.

## Dataset

- **Total Restaurants:** 8,598
- **Cities Covered:** Dallas, Miami, Atlanta, Philadelphia (+ metro areas)
- **Data Points:** Contact info, ratings, reviews, decision makers, website status, LinkedIn profiles

## Key Results

- **High Quality Leads:** 2,460 restaurants (score 60+)
- **Decision Makers Identified:** 2,422 contacts
- **Perfect Score Leads:** 100+ restaurants with validated emails and primary decision makers
- **Staffing Indicators Found:** 2,898 restaurants showing volume or operational challenges

## Files

- `restaurants_data.csv` - Complete dataset (8,598 restaurants)
- `high_quality_leads.csv` - Scored leads 60+ (2,460 restaurants)
- `scheduling_decision_makers.csv` - Decision maker contacts (2,422 contacts)
- `analyze_restaurants.py` - Analysis script
- `ANALYSIS_REPORT.md` - Detailed findings and recommendations

## Usage

Run the analysis:
```bash
python3 analyze_restaurants.py
```

## Lead Scoring

Leads scored 0-100 based on:
- Valid email (30 pts)
- Decision maker contact (15-25 pts)
- Working website (15 pts)
- Phone number (10 pts)
- Review volume (5-10 pts)
- LinkedIn profile (5 pts)
- Rating quality (5 pts)

## Top Decision Maker Titles

- Owners: 1,150
- General Managers: 351
- CEOs: 96
- Presidents: 91
- Directors of Operations: 10+

See `ANALYSIS_REPORT.md` for complete findings and recommendations.
