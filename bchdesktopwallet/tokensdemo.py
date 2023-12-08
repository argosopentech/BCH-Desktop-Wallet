import bitcash

# Bitcoin Cash Tokens Demo
# https://bitcash.dev/guide/cashtokens.html

# Hardcoded for testing lol
private_key = 35802989809929110344906770928891928395406747907426035337356610337891731325922
public_key = "bitcoincash:qrgfz9k93yp568jnlqwj47ufnkeu69tgpg4c8wvsf8"

# Create a Key instance based on the private key
key = bitcash.Key.from_int(private_key)
cashtoken_address = key.cashtoken_address

# Get unspents
unspents = key.get_unspents()
print(f"Unspents: {unspents}")

# The category comes from the transaction hash
category = "7c92532ea71b764aba805d5d5ebd94bb9ba0cf70ff68c11eec602391f4dbf710"

# Destination address
destination_address = cashtoken_address

# Send the transaction
send = False

if send:
    key.send([
        (
            destination_address,  # destination
            1000,  # amount
            "satoshi",  # currency
            category,  # category
            "minting",  # NFT capability
            None,  # NFT commitment, None
            10000  # fungible token amount
        )
    ])
    print("Transaction sent!")

balance = key.get_balance()
print(f"Balance: {balance}")

cashtoken_balance = key.cashtoken_balance
print(f"Cashtoken Balance: {cashtoken_balance}")

"""
Unspents: [Unspent(amount=171232, confirmations=1, script='76a914d09116c589034d1e53f81d2afb899db3cd15680a88ac', txid='7c92532ea71b764aba805d5d5ebd94bb9ba0cf70ff68c11eec602391f4dbf710', txindex=0)]
Transaction sent!
Balance: 170969
Cashtoken Balance: {'7c92532ea71b764aba805d5d5ebd94bb9ba0cf70ff68c11eec602391f4dbf710': {'token_amount': 10000, 'nft': [{'capability': 'minting'}]}}
"""
