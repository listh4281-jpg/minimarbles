# Minimarbles Trading Platform - Requirements Q&A

## Overview
A system for friends to record trades with each other using a virtual currency called "minimarbles".

---

## Questions & Answers

### Q1: How many friends will be using this system?
**Answer:** 3 to start, up to maybe 10.

---

### Q2: Is this a trusted group where everyone can see all trades and balances, or do you need private accounts with logins?
**Answer:** Don't worry about privacy yet - everything can be open for now. Keep privacy as an option for later.

---

### Q3: How does a trade get created? Does one person propose it and the other accepts, or do you just record trades after they've already been agreed verbally?
**Answer:** End state: propose-and-accept flow. Start simpler: just record trades that have been agreed elsewhere.

---

### Q4: What information defines a trade? (e.g., who's involved, stake amount, description of the bet, settlement date, settlement conditions)
**Answer:**
- Who's on each side
- Stake amount (minimarbles)
- Description of the bet
- Settlement date/conditions
- Trade type info to enable semi-automatic settlement:
  - Underlyings: input settlement price → calculates payout
  - Binaries: input yes/no outcome → settles automatically

---

### Q5: For an "underlying" trade, what exactly is being bet? E.g., "I think AAPL will be above $200 on Dec 31" or more like "I'll buy AAPL exposure at $195" where the payout scales with the final price?
**Answer:** Two trade types only:
- **Binary:** Threshold-based, yes/no outcome, fixed payout (e.g., "AAPL above $200 on Dec 31")
- **Underlying:** Linear exposure, payout scales with price (e.g., "buy at $195, settle at final price")

---

### Q6: For an underlying trade, how does the stake work? E.g., if I "buy at $195" with 10 minimarbles at stake, and it settles at $205, what's the payout? Is there a "per point" multiplier, or a max loss cap, or something else?
**Answer:**
- **Underlying:** "Lot size" not stake. Profit/loss = lot size × (settlement price - trade price). No cap, linear both ways.
- **Binary:** Stake = fixed amount won/lost.

---

### Q7: Who decides the settlement outcome? Does one party input the settlement price/result and the other confirm, or is it whoever gets there first, or something else?
**Answer:** Both parties must accept the settlement outcome.

---

### Q8: Does everyone start with the same amount of minimarbles? How many?
**Answer:** Admin-configurable, default 1000 minimarbles per person.

---

### Q9: Can balances go negative, or must you have sufficient minimarbles to enter a trade?
**Answer:** Must have sufficient minimarbles - no negative balances allowed.

---

### Q10: For underlying trades, the potential loss is uncapped. How do you check "sufficient" at trade entry? Is there a margin/collateral requirement (e.g., must have 100 minimarbles per lot), or do you just not worry about it until settlement?
**Answer:** Don't worry about it - trust the group.

---

### Q11: What's your technical background? Are you comfortable with code, running servers, databases, command line, etc.?
**Answer:** Codes Python at work with support. First solo home project - wants to learn. Comfortable with command line and database read/write. Limited server knowledge.

---

### Q12: Where do you want this to run? Options range from simplest to most "real":
- Just on your laptop (friends would need to be with you or you share screenshots)
- A shared Google Sheet or Notion database
- A simple web app you host somewhere (friends access via browser)
**Answer:** Wants a web app friends can access on their phones.

---

### Q13: Are you comfortable with Git/GitHub?
**Answer:** Uses GitHub at work but poorly. Wants to use it here to improve.

---

### Q14: Budget for hosting?
**Answer:** $5-7/month is fine.

---

### Q15: Anything else?
**Answer:** Wants to build with lots of tests - learning testing is a goal.

---

## Summary & Recommended Approach

### MVP Features
- Web app accessible on phones
- Users: 3-10 friends, open access (no login for now)
- Record trades (binary or underlying) after verbal agreement
- Settlement requires both parties to confirm
- Track minimarble balances (start at 1000, admin-configurable)
- Simple, clean mobile-friendly UI

### Trade Types
- **Binary:** Description, settlement condition, stake amount. Outcome: yes/no. Winner gets stake from loser.
- **Underlying:** Description, trade price, lot size. Settlement: input final price. P&L = lot size × (settlement price - trade price).

### Tech Stack
- **Flask** (Python web framework)
- **SQLite** (database)
- **pytest** (testing - a learning goal)
- **GitHub** (version control)
- **Render or Railway** (hosting)

### Future Additions
- Propose/accept trade flow
- User accounts & privacy
- Resting bids/offers

### Learning Goals
- Git/GitHub workflow
- Testing with pytest
- Web development basics
- Server/hosting

