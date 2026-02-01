from src.transaction import Transaction
from src.block import mine_block
from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.validator import Validator


def fresh_env():
    utxo = UTXOManager()
    mempool = Mempool()
    validator = Validator(utxo, mempool)

    utxo.add_utxo("genesis", 0, 50, "Alice")
    utxo.add_utxo("genesis", 1, 30, "Bob")
    utxo.add_utxo("genesis", 2, 20, "Charlie")
    utxo.add_utxo("genesis", 3, 10, "David")
    utxo.add_utxo("genesis", 4, 5, "Eve")

    return utxo, mempool, validator


def run_tests():

    test_no = input("Enter test number (1-10) : ")

    
    # Test 1: Basic Valid Transaction
    
    if test_no == "1":
        print("Test 1: Basic Valid Transaction")
        utxo, mempool, validator = fresh_env()

        tx1 = Transaction(
            "tx1",
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 10, "address": "Bob"},
            {"amount": 39.999, "address": "Alice"}]
        )
        print("ALice sends 10 BTC to Bob")
        valid , msg = validator.submit_transaction(tx1)
        if valid :
            print("Success: ",msg)
            print("Fee:", tx1.get_fee(utxo))
        else:
            print("Error: ",msg)

    
    # Test 2: Multiple Inputs
  
    if test_no == "2":
        print("\nTest 2: Multiple Inputs")
        utxo, mempool, validator = fresh_env()

        utxo.add_utxo("extra", 0, 20, "Alice")

        tx2 = Transaction(
            "tx2",
            [
                {"prev_tx": "genesis", "index": 0, "owner": "Alice"},
                {"prev_tx": "extra", "index": 0, "owner": "Alice"}
            ],
            [{"amount": 60, "address": "Bob"},
            {"amount": 9.999, "address": "Alice"}]
        )
        print("ALice sends 60 BTC to Bob using 2 UTXOS")
        valid , msg = validator.submit_transaction(tx2)
        if valid :
            print("Success: ",msg)
            print("Fee:", tx2.get_fee(utxo))
        else:
            print("Error: ",msg)

   
    # Test 3: Double Spend Same Transaction
  
    if test_no == "3":
        print("\nTest 3: Double Spend in Same TX")
        utxo, mempool, validator = fresh_env()

        tx3 = Transaction(
            "tx3",
            [
                {"prev_tx": "genesis", "index": 1, "owner": "Bob"},
                {"prev_tx": "genesis", "index": 1, "owner": "Bob"}
            ],
            [{"amount": 5, "address": "Alice"}]
        )
        print("ALice sends 5 BTC to Bob using same utxos twice in the same transaction")
        valid , msg = validator.submit_transaction(tx3)
        if valid :
            print("Success: ",msg)
            print("Fee:", tx3.get_fee(utxo))
        else:
            print("Error: ",msg)

 
    # Test 4: Mempool Double Spend

    if test_no == "4":
        print("\nTest 4: Mempool Double Spend")
        utxo, mempool, validator = fresh_env()

        tx4a = Transaction(
            "tx4a",
            [{"prev_tx": "genesis", "index": 2, "owner": "Charlie"}],
            [{"amount": 5, "address": "Bob"},
            {"amount": 14.999, "address": "Charlie"}]
        )

        tx4b = Transaction(
            "tx4b",
            [{"prev_tx": "genesis", "index": 2, "owner": "Charlie"}],
            [{"amount": 5, "address": "Alice"},
            {"amount": 14.999, "address": "Charlie"}]
        )
        print("Charlie sends 5 BTC to Bob and 5 BTC to Alice using same utxo")
        valid , msg = validator.submit_transaction(tx4a)
        if valid :
            print("1st transaction valid: ",msg)
            print("Fee:", tx4a.get_fee(utxo))
        else:
            print("Error: ",msg)

        valid , msg = validator.submit_transaction(tx4b)
        if valid :
            print("2nd transaction valid: ",msg)
            print("Fee:", tx4b.get_fee(utxo))
        else:
            print("Error: ",msg)

    # Test 5: Insufficient Funds
    
    if test_no == "5":
        print("\nTest 5: Insufficient Funds")
        utxo, mempool, validator = fresh_env()

        tx5 = Transaction(
            "tx5",
            [{"prev_tx": "genesis", "index": 1, "owner": "Bob"}],
            [{"amount": 100, "address": "Alice"}]
        )

        print("Bob tries to send 35 BTC (has only 30 BTC)")
        valid , msg = validator.submit_transaction(tx5)
        if valid :
            print("Success: ",msg)
            print("Fee:", tx5.get_fee(utxo))
        else:
            print("Error: ",msg)
    

   
    # Test 6: Negative Amount
   
    if test_no == "6":
        print("\nTest 6: Negative Output")
        utxo, mempool, validator = fresh_env()

        tx6 = Transaction(
            "tx6",
            [{"prev_tx": "genesis", "index": 3, "owner": "David"}],
            [{"amount": -5, "address": "Alice"}]
        )

        print("David tries to send -5 BTC to Alice")
        valid , msg = validator.submit_transaction(tx6)
        if valid :
            print("Success: ",msg)
            print("Fee:", tx6.get_fee(utxo))
        else:
            print("Error: ",msg)
        

    
    # Test 7: Zero Fee
    
    if test_no == "7":
        print("\nTest 7: Zero Fee")
        utxo, mempool, validator = fresh_env()

        tx7 = Transaction(
            "tx7",
            [{"prev_tx": "genesis", "index": 4, "owner": "Eve"}],
            [{"amount": 5, "address": "Bob"}]
        )

        print("Input and Output have same amounts (zero fee)")
        valid , msg = validator.submit_transaction(tx7)
        if valid :
            print("Success: ",msg)
            print("Fee:", tx7.get_fee(utxo))
        else:
            print("Error: ",msg)
        

    
    # Test 8: Race Attack
   
    if test_no == "8":
        print("\nTest 8: Race Attack")
        utxo, mempool, validator = fresh_env()

        utxo.add_utxo("race", 0, 10, "Alice")

        low = Transaction(
            "low",
            [{"prev_tx": "race", "index": 0, "owner": "Alice"}],
            [{"amount": 9.9, "address": "Bob"},
            {"amount": 0.099, "address": "Alice"}]
        )

        high = Transaction(
            "high",
            [{"prev_tx": "race", "index": 0, "owner": "Alice"}],
            [{"amount": 5, "address": "Charlie"},
            {"amount": 4.999, "address": "Alice"}]
        )

        print("Low fee transaction comes before high fee transaction")
        valid , msg = validator.submit_transaction(low)
        if valid :
            print("low fee transaction: ",msg)
            print("Fee:", low.get_fee(utxo))
        else:
            print("low fee transaction Error: ",msg)

        valid , msg = validator.submit_transaction(high)
        if valid :
            print("high fee transaction: ",msg)
            print("Fee:", high.get_fee(utxo))
        else:
            print("High fee transaction Error: ",msg)

  
    # Test 9: Mining Flow
   
    if test_no == "9":
        print("\nTest 9: Mining")
        utxo, mempool, validator = fresh_env()

        tx9 = Transaction(
            "tx9",
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 10, "address": "Bob"},
            {"amount": 39.999, "address": "Alice"}]
        )

        print("multiple transactions added to mempool")
        valid , msg = validator.submit_transaction(tx9)
        if valid :
            print("Transaction Success: ",msg)
            print("Miner Fee:", tx9.get_fee(utxo))
            mine_block("Vishnu",mempool,utxo)
            print("Miner balance: ",utxo.get_balance("Vishnu"))
            print("UTXOS updated")
        else:
            print("Error: ",msg)

    
    # Test 10: Unconfirmed Chain
   
    if test_no == "10":
        print("\nTest 10: Unconfirmed Chain")
        utxo, mempool, validator = fresh_env()

        parent = Transaction(
            "p",
            [{"prev_tx": "genesis", "index": 0, "owner": "Alice"}],
            [{"amount": 5, "address": "Bob"},
            {"amount": 44.999, "address": "Alice"}]
        )

        child = Transaction(
            "c",
            [{"prev_tx": "p", "index": 0, "owner": "Bob"}],
            [{"amount": 2, "address": "Charlie"},
            {"amount": 2.999, "address": "Bob"}]
        )

        print("Alice does a transaction to bob and bob tries to use the new created utxo before the transaction is mined")
        valid , msg = validator.submit_transaction(parent)
        if valid :
            print("Parent transaction: ",msg)
            print("Fee:", parent.get_fee(utxo))
        else:
            print("1st transaction Error: ",msg)
        valid , msg = validator.submit_transaction(child)
        if valid :
            print("Child transaction: ",msg)
            print("Fee:", child.get_fee(utxo))
        else:
            print("child transaction Error: ","utxo not yet confirmed as mining is not done")
