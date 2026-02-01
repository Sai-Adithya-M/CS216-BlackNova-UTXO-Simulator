def mine_block(miner_address, mempool, utxo_manager, num_txs=5):

    selected = mempool.get_top_transactions(num_txs, utxo_manager)

    if not selected:
        print("No transactions to mine")
        return 0.0

    total_fee = 0.0

    for tx in selected:
        total_fee += tx.get_fee(utxo_manager)
        
        for inp in tx.inputs:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        for i, out in enumerate(tx.outputs):
            utxo_manager.add_utxo(
                tx.tx_id,
                i,
                out["amount"],
                out["address"]
            )

        mempool.remove_transaction(tx.tx_id)

    utxo_manager.add_utxo("coinbase", 0, total_fee, miner_address)

    print(f"Miner {miner_address} receives {total_fee} BTC")

    return total_fee
