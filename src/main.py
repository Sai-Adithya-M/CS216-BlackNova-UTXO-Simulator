import sys
sys.path.insert(0, "../tests")
from utxo_manager import UTXOManager
from mempool import Mempool
from validator import validate
from transaction import Transaction
from block import Block
from test_scenarios import run_tests

utxo = UTXOManager()
mempool = Mempool()


# Genesis UTXOs
utxo.add_utxo("genesis", 0, 50, "Alice")
utxo.add_utxo("genesis", 1, 30, "Bob")
utxo.add_utxo("genesis", 2, 20, "Charlie")
utxo.add_utxo("genesis", 3, 10, "David")
utxo.add_utxo("genesis", 4, 5, "Eve")

while True:
    print("\n1 Create TX")
    print("2 View UTXO")
    print("3 View Mempool")
    print("4 Mine")
    print("5 Tests")
    print("6 Exit")

    c = input("> ")

    if c == "4":
        miner = input("Miner name: ")
        Block.mine_block(miner, mempool, utxo)

    elif c == "5":
        run_tests(validate, utxo,mempool)

    elif c == "6":
        pass