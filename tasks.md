# Minimarbles MVP Task List

**Instructions:** Find the first unchecked task (`- [ ]`), complete it using TDD, then mark it done (`- [x]`).

Each task: write test first → watch it fail → write code → watch it pass → commit → exit

---

## Phase 1: Pure Business Logic (no database)
- [x] **1.1** Binary payout calculation - function that takes (alice_stake, bob_stake, outcome) → returns (alice_pnl, bob_pnl)
- [x] **1.2** Underlying payout calculation - function that takes (lot_size, trade_price, settlement_price) → returns (long_pnl, short_pnl)

## Phase 2: Data Models (database schema)
- [x] **2.1** User model - id, name, balance
- [x] **2.2** Binary trade model - id, party_a, party_b, stake_a, stake_b, description, outcome, status
- [x] **2.3** Underlying trade model - id, long_party, short_party, lot_size, trade_price, settlement_price, description, status

## Phase 3: Database Operations
- [x] **3.1** Create user with starting balance
- [x] **3.2** Create binary trade (open status)
- [x] **3.3** Create underlying trade (open status)
- [x] **3.4** Settle binary trade - update status, update both user balances
- [x] **3.5** Settle underlying trade - update status, update both user balances
- [x] **3.6** Get user balance / list all users

## Phase 4: Flask Routes (API)
- [x] **4.1** GET /users - list all users and balances
- [x] **4.2** POST /users - create new user
- [x] **4.3** GET /trades - list all trades
- [ ] **4.4** POST /trades/binary - create binary trade
- [ ] **4.5** POST /trades/underlying - create underlying trade
- [ ] **4.6** POST /trades/<id>/settle - settle a trade

## Phase 5: UI (HTML templates)
- [ ] **5.1** Home page - show leaderboard (users + balances)
- [ ] **5.2** Trade list page - show all trades with status
- [ ] **5.3** Create trade form
- [ ] **5.4** Settle trade form
