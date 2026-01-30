class UTXOManager :

    def _init__(self) :
        self . utxo_set = {}

    def add_utxo ( self , tx_id : str , index : int , amount : float , owner : #o(1)
    str ) :
        if amount < 0 :
            raise ValueError("UTXO amount cannot be negative.")
        
        key = (tx_id,index)

        if(key in self.utxo_set) :
            raise KeyError(f"UTXO {tx_id}:{index} already exists")

        self.utxo_set[key] = {"amount": amount, "owner": owner}

        return 

    def remove_utxo ( self , tx_id : str , index : int ) :  #o(1)
        key = (tx_id, index)

        if key not in self.utxo_set:
            raise ValueError(f"Double spend detected! UTXO {tx_id}:{index} not found.")

        spent_utxo = self.utxo_set.pop(key)

        return spent_utxo 
    

    def get_balance ( self , owner : str ) -> float :  #o(n)
        owner_utxos = (data["amount"] for data in self.utxo_set.values() if data["owner"] == owner)
        total_balance = sum(owner_utxos)
        
        return round(total_balance, 8)
    
    def exists ( self , tx_id : str , index : int ) -> bool : #o(1)
        return (tx_id, index) in self.utxo_set
    
    def get_utxos_for_owner(self, owner: str) -> list: #o(n)

        return [
            {"tx_id": tid, "index": idx, "amount": data["amount"]}
            for (tid, idx), data in self.utxo_set.items()
            if data["owner"] == owner
        ]
