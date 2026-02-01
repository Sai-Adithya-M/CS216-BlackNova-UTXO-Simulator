def validate(tx, utxo_manager, mempool=None):
        seen = set()

        # Rule 1 + 2: inputs exist & no duplicate inputs
        for inp in tx.inputs:
            key = (inp["prev_tx"], inp["index"])

            if key in seen:
                return False, "Same UTXO used twice in transaction"

            seen.add(key)

            if not utxo_manager.exists(inp["prev_tx"], inp["index"]):
                return False, f"UTXO {key} does not exist"

        # Rule 3: Sum(inputs) >= Sum(outputs)
        input_sum = tx.get_input_sum(utxo_manager)
        output_sum = tx.get_output_sum()

        if input_sum < output_sum:
            return False, "Insufficient funds"

        # Rule 4: No negative outputs
        for out in tx.outputs:
            if out["amount"] < 0:
                return False, "Negative output amount"

        # Rule 5: No mempool conflict
        if mempool is not None:
            for inp in tx.inputs:
                key = (inp["prev_tx"], inp["index"])
                if key in mempool.spent_utxos:
                    return False, f"UTXO {key} already spent in mempool"

        return True, "Transaction valid"

