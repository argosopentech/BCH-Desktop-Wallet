# https://bitcash.dev/o

import bitcash

# Create a key
key = bitcash.Key()
# Or import a key from int
# key = bitcash.Key.from_int(15842665189923097459977717756102871267576260263646752100155231323389051784997)
print(f"Address: {key.address}")

# Get the balance
balance = key.get_balance()
print(f"Balance: {balance}")

# Send some money
outputs = [
    ("bitcoincash:qz69e5y8yrtujhsyht7q9xq5zhu4mrklmv0ap7tq5f", 1, "usd"),
    # you can add more recipients here
]
key.send(outputs)
