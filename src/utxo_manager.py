class UTXOManager:
    def __init__(self):
        # store utxos as a dict with key (tx_id, index) -> (amount, owner)
        self.utxo_set = {}

    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        self.utxo_set[(tx_id, index)] = (amount, owner)

    def remove_utxo(self, tx_id: str, index: int):
        self.utxo_set.pop((tx_id, index), None)

    def get_balance(self, owner: str) -> float:
        return sum(amount for (amount, o) in self.utxo_set.values() if o == owner)

    def exists(self, tx_id: str, index: int) -> bool:
        return (tx_id, index) in self.utxo_set

    def get_utxos_for_owner(self, owner: str) -> list:
        return [(tx_id, index, amount) for ((tx_id, index), (amount, o)) in self.utxo_set.items() if o == owner]
