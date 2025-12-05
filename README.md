# Restaurant Research

A project for researching restaurant staffing challenges and workforce management needs across Dallas, Miami, Atlanta, and Philadelphia metropolitan areas.

## Overview

This project contains 8,598 restaurants and demonstrates the critical difference between **assumption-based** and **evidence-based** lead generation.

## ⚠️ Important Learning

Our initial analysis identified 2,460 "high quality leads" based on assumptions (high volume, ratings, etc.). **This was wrong.**

After manually researching 10 restaurants, we found that **high volume ≠ staffing problems**. We needed actual evidence:
- Job postings with urgency
- Employee reviews mentioning scheduling chaos
- Customer complaints about understaffing
- Corporate acknowledgment of labor challenges

**Result:** 8 out of 10 researched restaurants had **actual evidence** of staffing pain.

**Conversion rate:** 35-50% (vs 5-10% without evidence)

## Evidence-Based Approach

### What We Do Now:
1. **Prioritize** restaurants by contact quality (decision makers, valid emails)
2. **Research** each restaurant (10-15 min) for actual evidence
3. **Document** findings with quotes and sources
4. **Qualify** only restaurants with real staffing pain

### Qualified Leads (With Evidence): 8

1. **Chuy's** (8/10 pain) - 1,035 openings, "scheduling is a constant battle"
2. **Flower Child** (7.5/10 pain) - Walk-in interviews, "start THIS WEEK"
3. **Pappadeaux** (6.5/10 pain) - "20 employees never seen again", 3 GMs in 2 years
4. **Meso Maya** (6.5/10 pain) - 44+ jobs, part of 55+ restaurant portfolio
5. **Golden Corral** (6.5/10 pain) - CEO: "most difficult time in 40-year career"
6. **Gloria's** (6/10 pain) - 50+ hour weeks, 23 locations
7. **Schlotzsky's** (6/10 pain) - 32-location franchise, owner acknowledges turnover
8. **Malai Kitchen** (6/10 pain) - Open interviews daily, 50-60 hour weeks

## Dataset

- **Total Restaurants:** 8,598
- **Cities Covered:** Dallas, Miami, Atlanta, Philadelphia (+ metro areas)
- **Research Priority Candidates:** 1,211 (have decision maker contacts)
- **Researched So Far:** 10
- **Qualified Leads With Evidence:** 8 (80% hit rate)

## Project Structure

```
.
├── README.md                          # This file
├── .gitignore                         # Git exclusions
│
├── data/
│   ├── raw/
│   │   └── restaurants_data.csv       # Complete dataset (8,598 restaurants)
│   ├── processed/
│   │   ├── high_quality_leads.csv     # [DEPRECATED] Assumption-based leads
│   │   └── scheduling_decision_makers.csv  # [DEPRECATED] Contacts without evidence
│   └── leads/
│       ├── research_priority_list.csv # 1,211 restaurants ranked for research
│       ├── qualified_leads_with_evidence.csv  # 8 qualified leads with evidence
│       ├── random_100_sample.csv      # Sample data for testing
│       ├── payroll_research_sample_50.csv
│       └── payroll_research_top_5.csv
│
├── scripts/
│   ├── evidence_based_lead_finder.py  # Prioritizes restaurants for research
│   ├── compile_evidence_based_leads.py  # Compiles research findings
│   ├── analyze_restaurants.py         # [DEPRECATED] Assumption-based scoring
│   ├── select_random_100.py           # Sampling utilities
│   ├── select_random_50_payroll.py
│   └── filter_and_prioritize_payroll_sample.py
│
├── reports/
│   ├── Pappadeaux_Dallas_Staffing_Intelligence_Report.md
│   ├── Chuys_Staffing_Intelligence_Report.md
│   ├── Schlotzskys_Dallas_Stemmons_Staffing_Analysis.md
│   ├── Meso_Maya_Staffing_Intelligence_Report.md
│   ├── Flower_Child_Staffing_Intelligence_Report.md
│   ├── Golden_Corral_Dallas_Staffing_Intelligence_Report.md
│   ├── Malai_Kitchen_Staffing_Research_Report.md
│   └── ANALYSIS_REPORT.md             # [DEPRECATED] Assumption-based analysis
│
└── docs/
    ├── EVIDENCE_BASED_RESEARCH_SUMMARY.md  # **READ THIS FIRST**
    ├── ALPHA_SIGNALS_FOR_RESTAURANT_SCHEDULING.md
    ├── ALPHA_SIGNALS_RESEARCH_SAMPLE_RESULTS.md
    ├── ESTIMATING_EMPLOYEE_COUNT.md
    ├── SIGNALS_TO_EXPLORE_LATER.md
    ├── FAST_GROWING_RESTAURANTS_RESEARCH_PROMPT.md
    ├── PAYROLL_ALPHA_SIGNALS_RESEARCH_METHODOLOGY.md
    └── PAYROLL_ALPHA_SIGNALS_SCORING_SYSTEM.md
```

## Usage

### Step 1: Generate Research Priority List
```bash
python3 scripts/evidence_based_lead_finder.py
```
Output: `data/leads/research_priority_list.csv` with 1,211 restaurants ranked by research priority

### Step 2: Manually Research Top Restaurants
For each priority restaurant (10-15 min each):
1. Search job postings (Indeed, company website)
2. Read employee reviews (Indeed, Glassdoor)
3. Check customer reviews for staffing mentions (Yelp, Google)
4. Document findings in `data/leads/research_priority_list.csv`

### Step 3: Compile Qualified Leads
```bash
python3 scripts/compile_evidence_based_leads.py
```
Output: `data/leads/qualified_leads_with_evidence.csv` with only restaurants that have actual evidence

## Evidence-Based Scoring

Research priority scored 0-100 based on:
- Valid decision maker email (50 pts) - **MOST IMPORTANT**
- Phone number (10 pts)
- LinkedIn profile (10 pts)
- Working website (10 pts)
- Review volume (10 pts) - indicates established operation
- Keywords in description (10 pts)

**Pain score** (1-10) assigned AFTER research based on:
- Job posting volume and urgency
- Employee review severity
- Customer complaints
- Corporate acknowledgment

## Key Learning

**Don't assume. Research.**

High review volume, being a chain, or low ratings do NOT predict staffing problems. You must research each restaurant individually for actual evidence.

See `docs/EVIDENCE_BASED_RESEARCH_SUMMARY.md` for complete methodology and learnings.
