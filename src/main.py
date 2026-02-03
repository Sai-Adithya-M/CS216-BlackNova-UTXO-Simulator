from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.validator import Validator
from src.transaction import create_transaction
from src.block import mine_block
from tests.test_scenarios import run_tests

utxo = UTXOManager()
mempool = Mempool()
validator = Validator(utxo, mempool)

# Genesis UTXOs
utxo.add_utxo("genesis", 0, 50, "Alice")
utxo.add_utxo("genesis", 1, 30, "Bob")
utxo.add_utxo("genesis", 2, 20, "Charlie")
utxo.add_utxo("genesis", 3, 10, "David")
utxo.add_utxo("genesis", 4, 5, "Eve")

print( "=== Bitcoin Transaction Simulator ===")
print("Initial UTXOs ( Genesis Block ) :")
print("Alice :",utxo.get_balance("Alice")," BTC")
print("Bob :",utxo.get_balance("Bob")," BTC")
print("Charlie :",utxo.get_balance("Charlie")," BTC")
print("David :",utxo.get_balance("David")," BTC")
print("Eve :",utxo.get_balance("Eve")," BTC \n")
print("\n Main menu :")
print("\n1 Create TX")
print("2 View UTXO")
print("3 View Mempool")
print("4 Mine")
print("5 Tests")
print("6 Exit")

while True:

    c = input("\nEnter choice: ")

    if c == "1":
        sender = input("Enter Sender: ")
        print("Available balance: ",utxo.get_balance(sender)," BTC")
        recipient = input("Enter Recipient: ")
        amount = float(input("Enter Amount: "))
        print()
        print("Creating transaction... ")
        tx = create_transaction(sender, recipient, amount, utxo)
        if tx:
            valid , msg = validator.submit_transaction(tx)
            if(valid):
                print(msg, "Fee: 0.001 BTC")
                print("TX ID:", tx.tx_id)
                print("Transaction added to mempool")
                print("Mempool size:", len(mempool.transactions),"transactions")
            else:
                print("Transaction failed:", msg)
        else:
            print("Transaction creation failed.")
        

    if c == "2":
        print("UTXO SET: ")
        for key, (amount, owner) in utxo.utxo_set.items():
            print(f"TX: {key[0]}, Index: {key[1]}, Amount: {amount} BTC, Owner: {owner}")

    if c == "3":
        print("MEMPOOL TRANSACTIONS: ")
        if(len(mempool.transactions)==0):
            print("Mempool is empty")
            pass
        for tx in mempool.transactions:
            print(f"TX ID: {tx.tx_id}, Inputs: {tx.inputs}, Outputs: {tx.outputs}, Fee: {tx.get_fee(utxo)} BTC")

    if c == "4":
        miner = input("Miner name: ")
        mine_block(miner, mempool, utxo)

    elif c == "5":
        run_tests()

    elif c == "6":
        break
