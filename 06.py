import time
import json
from hashlib import sha256


class Block:

    def __init__(self, data: str, previous_hash: str):
        self.transaction = data
        self.previous_hash = previous_hash
        self.timestamp: str = str(time.time())
        self.nonce: str = ""
        self.current_hash = self.hash

    @property
    def hash(self):
        txt = self.transaction + self.nonce + self.previous_hash + self.timestamp
        return str(sha256(txt.encode('utf-8')).hexdigest())

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_hashable(self, init):
        txt = self.transaction + str(init) + self.nonce + self.previous_hash + self.timestamp
        return txt.encode('utf-8')

    def mine_block(self, dif: int = 4):
        start = time.time()
        init = 0
        start_seq = dif * "0"
        while not str(sha256(self.get_hashable(init)).hexdigest()).startswith(start_seq):
            init += 1
        end = time.time()
        print("Mining time: " + str(end - start) + " s")
        self.nonce = str(init)
        self.current_hash = self.hash
        return self

    def change_block(self):
        self.transaction = "Changed string."
        return self


class Wallet:

    def __init__(self, name):
        self.name = name
        self.UTXOs = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def send_funds(self, recipient, value):
        bill = value
        neededUTXOs = []

        for utxo in self.UTXOs:
            if bill > 0:
                bill -= utxo.UTXO
                neededUTXOs.append(utxo)
        transaction = Transaction(self.name, recipient.name, value, neededUTXOs)

        for UTXO in neededUTXOs:
            self.UTXOs.remove(UTXO)

        self.UTXOs.append(TransactionInput(transaction.outputs[0]))
        recipient.UTXOs.append(TransactionInput(transaction.outputs[1]))

        return transaction


class Transaction:

    def __init__(self, sender: str, recipient: str, value: float, inputs: list):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.inputs = inputs
        self.transaction_id = self.calculate_hash
        self.outputs = []
        self.outputs = self.process_transaction()

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @property
    def calculate_hash(self):
        txt = self.sender + self.recipient
        return str(sha256(txt.encode('utf-8')).hexdigest())

    def process_transaction(self):
        coins_in_input = 0
        for i in self.inputs:
            coins_in_input += i.UTXO
            if int(coins_in_input) < int(self.value):
                raise ValueError("Insufficient funds!")
        cashback = coins_in_input - int(self.value)
        outputs = [TransactionOutput(self.sender, cashback, self.transaction_id),
                   TransactionOutput(self.recipient, self.value, self.transaction_id)]
        return outputs


class TransactionInput:

    def __init__(self, transaction_outputs: str):
        self.UTXO = transaction_outputs.value
        self.transaction_output_id = transaction_outputs.id


class TransactionOutput:

    def __init__(self, recipient: str, value: float, parent_transaction_id: str):
        self.recipient = recipient
        self.value = value
        self.parent_transaction_id = parent_transaction_id
        self.id = self.calculate_hash

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @property
    def calculate_hash(self):
        txt = self.recipient + str(self.value) + self.parent_transaction_id
        return str(sha256(txt.encode('utf-8')).hexdigest())


if __name__ == '__main__':

    walletC = Wallet("Julie")
    walletD = Wallet("Robin")
    walletE = Wallet("Zlatik")
    DefTransaction = Transaction("0", "Julie", 300, [TransactionInput(TransactionOutput("0", 300, "0"))])
    Def2Transaction = Transaction("0", "SAMO", 150, [TransactionInput(TransactionOutput("0", 150, "0"))])
    Def3Transaction = Transaction("0", "Hanka", 20, [TransactionInput(TransactionOutput("0", 20, "0"))])
    print("DefTransaction:")
    print(DefTransaction)
    print("Def2Transaction:")
    print(Def2Transaction)
    print("walletC:")
    print(walletC)
    print("walletD:")
    print(walletD)
    print("walletE:")
    print(walletE)

    walletC.UTXOs = [TransactionInput(DefTransaction.outputs[1])]
    firstTransaction = walletC.send_funds(walletD, 80)
    print("firstTransaction:")
    print(firstTransaction)

    walletD.UTXOs = [TransactionInput(Def2Transaction.outputs[1])]
    secondTransaction = walletD.send_funds(walletC, 100)
    print("secondTransaction:")
    print(secondTransaction)

    walletE.UTXOs = [TransactionInput(Def3Transaction.outputs[1])]
    thirdTransaction = walletE.send_funds(walletC, 10)
    print("thirdTransaction:")
    print(thirdTransaction)

    print()

