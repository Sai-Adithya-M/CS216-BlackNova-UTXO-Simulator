class Transaction:
    def __init__(self, tx_id: str, inputs: list, outputs: list):
        """
        inputs: list of dicts:
            {
                "prev_tx": str,
                "index": int,
                "owner": str
            }

        outputs: list of dicts:
            {
                "amount": float,
                "address": str
            }
        """
        self.tx_id = tx_id
        self.inputs = inputs
        self.outputs = outputs


    def get_input_sum(self, utxo_manager):
        total = 0.0
        for inp in self.inputs:
            key = (inp["prev_tx"], inp["index"])
            amount, _ = utxo_manager.utxo_set[key]
            total += amount
        return total
    

    def get_output_sum(self):
        return sum(out["amount"] for out in self.outputs)

    def get_fee(self, utxo_manager):
        return self.get_input_sum(utxo_manager) - self.get_output_sum()

    def validate(self, utxo_manager, mempool=None):
        seen = set()

        # Rule 1 + 2: inputs exist & no duplicate inputs
        for inp in self.inputs:
            key = (inp["prev_tx"], inp["index"])

            if key in seen:
                return False, "Same UTXO used twice in transaction"

            seen.add(key)

            if not utxo_manager.exists(inp["prev_tx"], inp["index"]):
                return False, f"UTXO {key} does not exist"

        # Rule 3: Sum(inputs) >= Sum(outputs)
        input_sum = self.get_input_sum(utxo_manager)
        output_sum = self.get_output_sum()

        if input_sum < output_sum:
            return False, "Insufficient funds"

        # Rule 4: No negative outputs
        for out in self.outputs:
            if out["amount"] < 0:
                return False, "Negative output amount"

        # Rule 5: No mempool conflict
        if mempool is not None:
            for inp in self.inputs:
                key = (inp["prev_tx"], inp["index"])
                if key in mempool.spent_utxos:
                    return False, f"UTXO {key} already spent in mempool"

        return True, "Transaction valid"

