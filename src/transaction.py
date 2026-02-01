import time

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
        return round(self.get_input_sum(utxo_manager) - self.get_output_sum(), 3)



def create_transaction(sender, receiver, amount, utxo_manager, fee=0.001):

    utxos = utxo_manager.get_utxos_for_owner(sender)

    if not utxos:
        raise ValueError("Sender has no UTXOs")

    inputs = []
    total = 0.0

    for (txid, index, utxo_amount) in utxos:
        inputs.append({
            "prev_tx": txid,
            "index": index,
            "owner": sender
        })
        total += utxo_amount

        if total >= amount + fee:
            break

    if total < amount + fee:
        raise ValueError("Insufficient funds")

    outputs = []

    outputs.append({
        "amount": amount,
        "address": receiver
    })

    change = round(total - amount - fee, 3)

    if change > 0:
        outputs.append({
            "amount": change,
            "address": sender
        })

    tx_id = f"tx_{sender}_{receiver}_{amount}_{int(time.time())}"

    return Transaction(tx_id, inputs, outputs)