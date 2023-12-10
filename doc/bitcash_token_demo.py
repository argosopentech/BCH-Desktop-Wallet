# https://bitcash.dev/o
import bitcash

key = bitcash.Key.from_int(
    77074755880332255200656847990278517270974204413887705285835939060385312456371
)
print(f"Address: {key.address}")

# Get the CashToken balance
cashtokenbalance = key.get_cashtokenbalance()
print(f"Balance: {cashtokenbalance}")

# Send some money
outputs = [
    ("bitcoincash:zru4tm3ld4jgmddtrpje4qv8v6s4j6c435adydlhle", 1, "usd"),
]
print(key.send(outputs))
