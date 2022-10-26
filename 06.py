import time
import json
from hashlib import sha256


class Block:

    def __init__(self, data: str, previous_hash: str):
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp: str = str(time.time())
        self.nonce: str = ""
        self.current_hash = self.hash

    @property
    def hash(self):
        txt = self.data + self.nonce + self.previous_hash + self.timestamp
        return str(sha256(txt.encode('utf-8')).hexdigest())

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_hashable(self, init):
        txt = self.data + str(init) + self.nonce + self.previous_hash + self.timestamp
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
        self.data = "Changed string."
        return self


class Wallet:

    def __init__(self, name):
        self.name = name


class Transaction:

    def __init__(self, sender: str, recipient: str, value: float, inputs: list):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.inputs = inputs
        self.outputs = []
        self.transaction_id = self.calculate_hash()

    def calculate_hash(self):
        txt = self.sender + self.recipient
        return str(sha256(txt.encode('utf-8')).hexdigest())


class TransactionInput:

    def __init__(self, transaction_outputs: str):
        self.transaction_outputs = transaction_outputs
        self.utxo = []


class TransactionOutput:

    def __init__(self, recipient: str, value: float, parent_transaction: str):
        self.recipient = recipient
        self.value: str = str(value)
        self.parent_transaction = parent_transaction
        self.id = self.id

    @property
    def id(self):
        txt = self.recipient + self.value + self.parent_transaction
        return str(sha256(txt.encode('utf-8')).hexdigest())


if __name__ == '__main__':

    try:
        difficulty = int(input("Choose difficulty (integer): "))
    except ValueError:
        pass
    chain = []
    print("\n")

    chain.append(Block("Hello, I am the first block", "0"))
    print("Mining fist block...")
    try:
        chain[0].mine_block(difficulty)
    except NameError:
        chain[0].mine_block()
    print("First block mined: " + chain[0].current_hash)
    # print(Block.to_JSON(genesisBlock))
    # print("1st block's hash: " + genesisBlock.current_hash)

    chain.append(Block("I am the second block.", chain[0].current_hash))
    print("\nMining second block...")
    try:
        chain[1].mine_block(difficulty)
    except NameError:
        chain[1].mine_block()
    print("Second block mined: " + chain[1].current_hash)
    # print(Block.to_JSON(secondBlock))
    # print("2nd block's hash: " + secondBlock.current_hash)

    chain.append(Block("And I am the third one.", chain[1].current_hash))
    print("\nMining third block...")
    try:
        chain[2].mine_block(difficulty)
    except NameError:
        chain[2].mine_block()
    print("Third block mined: " + chain[2].current_hash)
    # print(Block.to_JSON(thirdBlock))
    # print("3rd block's hash: " + thirdBlock.current_hash)

    def is_chain_valid() -> bool:
        for block in chain:
            txt = block.data + block.nonce + block.previous_hash + block.timestamp
            if str(sha256(txt.encode('utf-8')).hexdigest()) != block.current_hash:
                block.current_hash = block.hash
                return False
        return True

    changing = input("\nDo you want to change second block? (y/n): ")
    if changing == "y":
        print("Printing current state for control:\n" + chain[1].to_JSON())
        chain[1].change_block()
        print("Block changed.")
    else:
        print("Not changing.")

    print("\nBlockchain valid: " + str(is_chain_valid()))

    print("\nBlockchain: " + chain[0].to_JSON() + "\n" + chain[1].to_JSON() + "\n"
          + chain[2].to_JSON())

    walletA = Wallet("Alice")
    walletB = Wallet("Bob")

    print(walletA.name)

    transaction = Transaction(walletA.name, walletB.name, 5, None)

