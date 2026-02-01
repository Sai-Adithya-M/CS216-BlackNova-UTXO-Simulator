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
            if key in utxo_manager.utxo_set:
                utxo_data = utxo_manager.utxo_set[key]
                # Access the 'amount' key specifically
                total += utxo_data["amount"]
            else:
                raise ValueError(f"Input UTXO {key} not found in UTXO set!")
        return total
    

    def get_output_sum(self):
        return sum(out["amount"] for out in self.outputs)

    def get_fee(self, utxo_manager):
        return self.get_input_sum(utxo_manager) - self.get_output_sum()

    

