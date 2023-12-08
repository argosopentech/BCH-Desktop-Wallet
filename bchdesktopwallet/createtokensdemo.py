# createtokensdemo.py
from time import sleep

from bitcash import Key
from bitcash.exceptions import InsufficientFunds

import bchdesktopwallet.localwalletman as localwalletman


class TokenMan:
    def __init__(self, key):
        self.key = key

    def create_token(self, token_name, token_symbol, token_amount):
        # Create a helper wallet to create an unspent
        helper_key = Key()
        helper_address = helper_key.address

        # Fund the helper wallet with 1000 satoshis
        outputs = [(helper_address, 1e5, "satoshi")]
        self.key.send(outputs)
        print("Helper wallet funded.")

        sleep(1)

        # Send the 1000 satoshis back to the original wallet as an unspent genesis
        outputs = [(self.key.address, int(1e5 * 0.9), "satoshi")]
        helper_key.send(outputs)
        print("Unspent genesis created.")

        sleep(1)

        # Get transaction hash
        txid = self.key.get_transactions()[0]
        print(f"Transaction hash: {txid}")

        # Wait for transaction to confirm
        sleep(1)

        self.key.send(
            [
                (
                    self.key.cashtoken_address,  # destination
                    5e4,  # amount
                    "satoshi",  # currency
                    txid,  # category_id
                    "minting",  # NFT capability
                    None,  # NFT commitment, None
                    token_amount,  # fungible token amount
                )
            ]
        )
        print("Token created successfully.")

    def get_token_balance(self, token_name):
        return self.key.cashtoken_balance

    def get_token_unspents(self, token_name):
        return self.key.cashtoken_unspents


# Demo if run as main
if __name__ == "__main__":
    wallet_manager = localwalletman.LocalWalletManager()
    wallets = wallet_manager.get_wallets()
    wallet = wallets[0]
    print(f"Wallet: {wallet}")
    tm = TokenMan(Key.from_int(wallet["private_key"]))
    tm.create_token("test", "tst", 1000)
