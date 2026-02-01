import sys
sys.path.insert(0,"../src")
from transaction import Transaction

def run_tests(validator, utxo_manager,mempool):

    print("\n--- Double Spend Test ---")

    tx1 = Transaction(
        "tx1",
        [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
        [{"amount": 10, "address": "Bob"},
         {"amount": 39.999, "address": "Alice"}]
    )

    ok, msg = validator(tx1,utxo_manager,mempool)
    print("TX1:", msg)
