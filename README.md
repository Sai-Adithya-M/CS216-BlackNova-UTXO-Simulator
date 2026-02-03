# UTXO Simulator

A simplified **UTXO-based blockchain simulator** that demonstrates how unspent transaction outputs, transaction validation, mempool handling, and mining work together in a Bitcoin-like system.

---

## Team: BlackNova

- **Member 1:** Kadasani Ashwartha Karthik Reddy  
- **Member 2:** Mannepalli Sai Adithya  
- **Member 3:** Katasani Vishnu Vardhan Reddy  
- **Member 4:** Yelisetti Vignesh  

---

##  How to Run the Program

From the project root directory, run:

```bash
python -m src.main
```

---

## Core Design Architecture

### UTXO-Based Model
Instead of account balances, the system tracks individual **Unspent Transaction Outputs (UTXOs)**.

- A user’s balance is the sum of all UTXOs they own
- Managed using the `UTXOManager`

---

### Transaction Lifecycle

1. **Creation**
   - Transactions consume existing UTXOs as inputs
   - Create new outputs (including change)

2. **Validation**
   - A `Validator` enforces consensus rules:
     - Solvency
     - Ownership
     - No double-spending

3. **Mempool**
   - Valid transactions wait in the mempool before confirmation

4. **Mining**
   - A simplified mining process selects high-fee transactions
   - Updates the global UTXO state

---

## Key Components

### UTXOManager (State)
- Maintains the global state of all valid, unspent coins
- Stores data as:
  ```
  (tx_id, index) -> (amount, owner)
  ```
- Handles atomic updates when blocks are mined

---

### Transaction (Data Structure)
- Composed of:
  - **Inputs:** References to previous UTXOs
  - **Outputs:** New owners and amounts
- Automatically calculates transaction fees:
  ```
  fee = total_inputs - total_outputs
  ```

---

### Validator (Security)
Ensures transactions are valid before entering the mempool.

Checks for:
- Existence of input UTXOs
- Double-spending (confirmed state and mempool)
- Non-negative output values
- Inputs ≥ Outputs

---

### Mempool
- Buffers unconfirmed transactions
- Prevents conflicts by tracking spent UTXOs
- Prioritizes transactions by fee

---

### Block / Mining 
- Selects top-fee transactions from the mempool
- Consumes input UTXOs and creates outputs
- Rewards the miner with total transaction fees (coinbase)

---

###  Main 
- Command-line interface to:
  - Create transactions
  - View UTXOs
  - Mine blocks
- Initializes Genesis UTXOs (Alice, Bob, etc.) for testing

---

## Features

### Satisfied
- UTXO-based accounting
- Double-spend prevention
- Fee-based transaction prioritization

### Limitations
- No cryptographic signatures
- No peer-to-peer networking
- No Proof-of-Work
- Single-node simulation