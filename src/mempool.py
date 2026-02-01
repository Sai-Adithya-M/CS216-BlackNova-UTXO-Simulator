class Mempool:
    def __init__(self, max_size=50):
        self.transactions = []
        self.spent_utxos = set()
        self.max_size = max_size

    def add_transaction(self, tx):
        if len(self.transactions) >= self.max_size:
            return False, "Mempool full"

        for inp in tx.inputs:
            key = (inp["prev_tx"], inp["index"])
            self.spent_utxos.add(key)

        self.transactions.append(tx)
        return True, "Transaction added to mempool"

    
    def remove_transaction(self, tx_id):
        for tx in self.transactions:
            if tx.tx_id == tx_id:
                for inp in tx.inputs:
                    key = (inp["prev_tx"], inp["index"])
                    self.spent_utxos.discard(key)

                self.transactions.remove(tx)
                return


    def get_top_transactions(self, n, utxo_manager):
        sorted_txs = sorted(
            self.transactions,
            key=lambda tx: tx.get_fee(utxo_manager),
            reverse=True
        )
        return sorted_txs[:n]

    
    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()
