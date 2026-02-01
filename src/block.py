import hashlib
import time

class Block:
    def __init__(self, transactions, previous_hash):
        # 1. The data we want to store
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        # 2. Mining variables
        self.nonce = 0
        self.hash = ""
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.previous_hash}{self.timestamp}{self.transactions}{self.nonce}"

        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def mine_block(miner_address, mempool, utxo_manager, previous_hash, difficulty=4, num_txs=5):
        # 1. Select top transactions from mempool
        selected_txs = mempool.get_top_transactions(num_txs)
        if not selected_txs:
            return None, "No transactions to mine"

        # 2. Update UTXO set (remove inputs, add outputs)
        for tx in selected_txs:
            # Remove spent inputs
            for inp in tx.inputs:
                utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])
            
            # Add new outputs as spendable UTXOs
            for i, out in enumerate(tx.outputs):
                utxo_manager.add_utxo(tx.tx_id, i, out["amount"], out["address"])

        # 3. Handle Miner Reward (Coinbase Transaction)
        # In a real chain, this is a special tx, but here we add it directly to UTXOs
        reward = 12.5  # Block reward
        utxo_manager.add_utxo("COINBASE", 0, reward, miner_address)

        # 4. Perform Proof of Work
        new_block = Block(selected_txs, previous_hash)
        print(f"Mining started for {len(selected_txs)} transactions...")
        new_block.mine(difficulty)

        # 5. Remove mined transactions from mempool
        for tx in selected_txs:
            mempool.remove_transaction(tx.tx_id)

        return new_block, "Success"

    def to_dict(self):
        return {
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "transactions": [tx.to_dict() for tx in self.transactions]
        }
    
    