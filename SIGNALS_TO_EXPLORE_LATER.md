# Alpha Signals to Explore Later

**Created:** November 30, 2025
**Status:** Deprioritized for now - revisit when resources/partnerships available

This document tracks alpha signals that are either partially feasible (requiring workarounds) or currently not feasible (blocked by partnerships/API access). These may become viable in the future.

---

## ⚠️ PARTIALLY FEASIBLE SIGNALS (Workarounds Required)

### 1. Hours Reduction Signal

**Current Status:** Partially Feasible - Requires building custom tracking infrastructure

**The Problem:**
- Google Places API only provides CURRENT operating hours
- No historical data available
- Must build our own tracking system

**Why We Want This:**
- Direct indicator of staffing shortage (7 days → 6 days)
- Strong timing signal (recent change = current pain)
- Great conversation starter: "I noticed you reduced hours - are you dealing with staffing constraints?"

**What It Would Take:**
1. Query Google Places API weekly for all restaurants
2. Store results in our own database with timestamps
3. Build comparison logic to detect changes
4. Flag reductions: days/week or hours/day

**Costs:**
- **Full dataset:** $585/month (8,598 restaurants × 4 queries/month)
- **Optimized:** $68/month (1,000 priority restaurants × 4 queries/month)
- **Infrastructure:** Database + cron job setup

**When to Revisit:**
- When we have budget for $68-585/month API costs
- When we have engineering resources to build tracking system
- After implementing the 6 highly feasible signals first

**Alpha Tier:** Tier 2 (Strong)

---

### 2. Manager LinkedIn Job Search Activity

**Current Status:** Partially Feasible - Manual monitoring only (no API)

**The Problem:**
- LinkedIn Sales Navigator is UI-based, no official API
- "Open to Work" badge only visible to LinkedIn Recruiters (not Sales Navigator)
- Automation would violate LinkedIn Terms of Service

**Why We Want This:**
- Manager leaving = knows there's a problem
- New GM (first 90 days) = change window, receptive to new solutions
- Decision-maker in transition

**What It Would Take:**
**Manual Approach:**
1. Subscribe to LinkedIn Sales Navigator ($99-149/month)
2. Build saved searches for "General Manager" OR "Owner" at target restaurants
3. Set up alerts for job changes
4. Weekly manual review of GM list
5. Trigger outreach to new GMs within first 90 days

**Automated Approach (Risky):**
- Browser automation (Puppeteer, Playwright) to scrape Sales Navigator
- ⚠️ Violates LinkedIn ToS - risk of account ban
- Not recommended

**Costs:**
- $99-149/month LinkedIn Sales Navigator subscription
- 1-2 hours/week manual monitoring time

**When to Revisit:**
- When we have dedicated SDR who can do weekly manual reviews
- If LinkedIn ever releases Sales Navigator API (unlikely)
- If we're willing to accept account ban risk with automation (not recommended)

**Alpha Tier:** Tier 3 (Moderate)

---

## ❌ LIMITED/NOT FEASIBLE SIGNALS (Blocked or Prohibitive)

### 3. Yelp Waitlist/Reservation Wait Times

**Current Status:** Not Feasible - Requires Yelp Partnership

**The Problem:**
- Yelp Waitlist API requires "onboarded Yelp Waitlist partner" status
- Yelp Reservations API requires "Yelp Reservations partner" status
- Not available via public Yelp Fusion API
- Enterprise tier pricing not publicly disclosed

**Why We Want This:**
- Consistently high wait times (30+ min) = high volume = complex scheduling needs
- "I see you have 45-min waits on weekends - are you optimizing labor for peaks?"
- Chronic demand signal

**What It Would Take:**
- Partnership agreement with Yelp
- Yelp Guest Manager (Enterprise tier) subscription
- Unknown pricing (likely $1,000s/month)

**Workaround:**
- Manual spot-checking: Check Yelp waitlist times during peak hours (Fri/Sat 7-8pm)
- Qualitative research only, not automated
- Note restaurants with consistent 30+ min waits

**When to Revisit:**
- If we establish a partnership with Yelp
- If Yelp opens up Waitlist API to public
- If we can justify Enterprise tier pricing

**Alpha Tier:** Tier 2-3 (Strong to Moderate)

---

### 4. Glassdoor "Interview Difficulty" Score Decrease

**Current Status:** Not Feasible - API Closed, No Historical Data

**The Problem:**
- Glassdoor API was closed to public access in 2021
- Even when API was open, no historical rating data was available
- Only current ratings accessible
- Cannot track changes over time

**Why We Want This:**
- Interview difficulty decrease (3.5 → 2.0) = lowering hiring bar = desperation
- "Your interview process got easier - are you desperate to fill positions?"
- Signals recruiting crisis

**What It Would Take:**
- Glassdoor would need to:
  1. Re-open public API access (unlikely)
  2. Add historical ratings endpoint (unlikely)
- OR we manually scrape interview reviews and do qualitative assessment

**Workaround:**
- Manual monitoring of Glassdoor interview reviews
- Qualitative read: "process was very easy" vs "rigorous multi-round"
- Not scalable

**When to Revisit:**
- If Glassdoor re-opens public API (extremely unlikely)
- If we have time for manual qualitative review (low priority)

**Alpha Tier:** Tier 3 (Moderate)

**Recommendation:** ❌ Deprioritize entirely unless Glassdoor changes API policy

---

## 🔄 NEXT STEPS

**When to revisit this list:**

1. **After implementing the 6 highly feasible signals** (3-6 months)
   - Health Inspection Timing
   - Liquor License Applications
   - Menu Simplification
   - Ghost Kitchen/Virtual Brand Launch
   - Franchise Owner Portfolios
   - Negative Local News Coverage

2. **When we have additional budget** ($100-700/month)
   - Hours Reduction tracking ($68-585/month)
   - LinkedIn Sales Navigator ($99-149/month)

3. **When we have engineering resources**
   - Build Hours Reduction tracking system
   - Database + cron job infrastructure

4. **When we have dedicated SDR time**
   - Manual LinkedIn monitoring (1-2 hours/week)

5. **If partnerships become available**
   - Yelp partnership discussions
   - Check if Glassdoor API reopens

---

## 📊 PRIORITIZATION DECISION TREE

**Should I implement a "to explore later" signal?**

```
Have we implemented all 6 highly feasible signals?
├─ NO → Focus on those first
└─ YES → Continue below

Do we have $100-700/month budget?
├─ NO → Wait
└─ YES → Continue below

Do we have engineering resources?
├─ NO → Consider LinkedIn manual monitoring only
└─ YES → Implement Hours Reduction tracking

Do we have dedicated SDR time (1-2 hrs/week)?
├─ NO → Skip LinkedIn monitoring
└─ YES → Add LinkedIn Sales Navigator
```

**Bottom line:** Don't explore these signals until the highly feasible ones are fully operationalized and producing results.

---

**Last Updated:** November 30, 2025
**Next Review:** After Q1 2026 (once Phase 1 signals are live)
