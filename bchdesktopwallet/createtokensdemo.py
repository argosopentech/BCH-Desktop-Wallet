# createtokensdemo.py
import bchdesktopwallet.localwalletman as localwalletman
from bitcash import Key


class TokenMan:
    def __init__(self, key):
        self.key = key

    def create_token(self, token_name, token_symbol, token_amount):
        # Make a transaction to create a fresh unspent
        # outputs = [(self.key.address, 0.01, "usd")]
        # self.key.send(outputs)

        # Get the genesis unspent
        unspents = self.key.get_unspents()
        print(unspents)

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
