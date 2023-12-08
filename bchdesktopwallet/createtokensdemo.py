# createtokensdemo.py
import bchdesktopwallet.localwalletman as localwalletman
from bitcash import Key


class TokenMan:
    def __init__(self, key):
        self.key = key

    def create_token(self, token_name, token_symbol, token_amount):
        # Create a helper wallet to create an unspent
        helper_key = Key()
        helper_address = helper_key.address

        # Fund the helper wallet with 1000 satoshis
        outputs = [(helper_address, 1e4, "satoshi")]
        self.key.send(outputs)
        print("Helper wallet funded.")

        # Send the 1000 satoshis back to the original wallet as an unspent genesis
        outputs = [(self.key.address, int(1e4 * 0.9), "satoshi")]
        helper_key.send(outputs)
        print("Unspent genesis created.")

        unspent = self.key.get_unspents()[-1]
        print(unspent)

    def get_token_balance(self, token_name):
        return self.key.cashtoken_balance

    def get_token_unspents(self, token_name):
        return self.key.cashtoken_unspents


# Demo if run as main
if __name__ == "__main__":
    wallet_manager = localwalletman.LocalWalletManager()
    wallets = wallet_manager.get_wallets()
    for wallet in wallets:
        print(f"Wallet: {wallet}")
        tm = TokenMan(Key.from_int(wallet["private_key"]))
        tm.create_token("test", "tst", 1000)
