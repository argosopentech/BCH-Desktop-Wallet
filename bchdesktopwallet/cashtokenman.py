from time import sleep

from bitcash import Key

import bchdesktopwallet.localwalletman as localwalletman


class CashTokenManager:
    def __init__(self, key):
        self.key = key

    def create_token(self, token_name, token_symbol, token_amount):
        txid = None
        unspents = self.key.get_unspents()
        for unspent in unspents:
            if unspent.txindex == 0:
                txid = unspent.txid
                break
        if txid is None:
            output = [(self.key.address, 546, "satoshi")]
            txid = self.key.send(output, combine=False)
            sleep(1)

        self.key.send(
            [
                (
                    self.key.cashtoken_address,  # destination
                    1000,  # amount
                    "satoshi",  # currency
                    txid,  # category_id
                    "minting",  # NFT capability
                    None,  # NFT commitment, None
                    token_amount,  # fungible token amount
                )
            ]
        )
        print("Token created successfully.")

    def get_token_balance(self):
        return self.key.cashtoken_balance


# Demo if run as main
if __name__ == "__main__":
    wallet_manager = localwalletman.LocalWalletManager()
    wallets = wallet_manager.get_wallets()
    wallet = wallets[0]
    print(f"Wallet: {wallet}")
    tm = CashTokenManager(Key.from_int(wallet["private_key"]))

    # tm.create_token("DoggyCash", "dogch", 1000)
    print(f"Token Balance: {tm.get_token_balance()}")
    # Expected behavior:
    # Token Balance: {'12d5637b7dac9cce41bebb2d59ba26bbff6ec6330036c2f8ca77d78545cd12a7': {'token_amount': 1000, 'nft': [{'capability': 'minting'}]}, '94b10ff15fbfc128f48bd551bfbf9123eade98a8619dc35055783faf8f8e7188': {'token_amount': 1000, 'nft': [{'capability': 'minting'}]}}
    # Behavior if create_token is commented out:
    # Token Balance: {}
