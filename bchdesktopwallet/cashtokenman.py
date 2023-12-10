from time import sleep

from bitcash import Key

import bchdesktopwallet.localwalletman as localwalletman


class CashTokenManager:
    def __init__(self, key):
        self.key = key

    def create_token(self, token_amount):
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

    def get_cashtokenbalance(self):
        return self.key.get_cashtokenbalance()


# Demo if run as main
if __name__ == "__main__":
    wallet_manager = localwalletman.LocalWalletManager()
    wallets = wallet_manager.get_wallets()
    wallet = wallets[0]
    tm = CashTokenManager(Key.from_int(wallet["private_key"]))
    tm.create_token(2000)
    print(f"Token Balance: {tm.get_cashtokenbalance()}")
