# Minimarbles - Agent Prompt

## Project Overview
A web app for friends to record trades with each other using a virtual currency called "minimarbles".

## Development Approach
- **TDD (Test-Driven Development):** Always write the test first, watch it fail, then write code to make it pass.
- **Bite-sized commits:** Each task should result in a commit with passing tests.
- **Explain as you go:** The user is learning - explain what you're doing and why.

## Tech Stack
- **Flask** - Python web framework
- **SQLite** - Database (via Flask-SQLAlchemy when we add it)
- **pytest** - Testing framework
- **GitHub** - Version control

## Key Business Rules

### Trade Types
1. **Binary:** Yes/no outcome with asymmetric stakes (e.g., 20:10 odds)
   - Party A stakes X, Party B stakes Y
   - If outcome is YES: A wins Y, B loses Y
   - If outcome is NO: B wins X, A loses X

2. **Underlying:** Linear exposure to a price
   - Long party and short party agree on trade price and lot size
   - P&L = lot_size × (settlement_price - trade_price)
   - Long gains if price goes up, short gains if price goes down

### Minimarbles
- Each user starts with 1000 (admin-configurable)
- Zero-sum: minimarbles are conserved across all trades
- Users must have sufficient balance to trade (but no margin checks for underlying)

## Current Task
Check `tasks.md` for the current task list. Work through tasks in order.

## Testing Commands
```bash
source venv/bin/activate
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_file.py # Run specific file
pytest -x                 # Stop on first failure
```
