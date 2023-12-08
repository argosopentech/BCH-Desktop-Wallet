# createtokensdemo.py
from time import sleep

from bitcash import Key

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
        txid = self.key.get_transactions()[-1]
        print(f"Transaction hash: {txid}")

        # Wait for transaction to confirm
        sleep(10)

        # Broken
        exit(1)
        """
        $ python bchdesktopwallet/createtokensdemo.py 
Wallet: {'address': 'bitcoincash:qpx53qg7rtddxykfacrg9rfnqf0sdhtr9qzfyhecmh', 'private_key': 15842665189923097459977717756102871267576260263646752100155231323389051784997}
Helper wallet funded.
Unspent genesis created.
Transaction hash: 081432467c2872767c0b66dd73419a29be8aa98101772ac82c1125f74e9655f0
Traceback (most recent call last):
  File "/home/ipfactory/git/BCH-Desktop-Wallet/bchdesktopwallet/createtokensdemo.py", line 68, in <module>
    tm.create_token("test", "tst", 1000)
  File "/home/ipfactory/git/BCH-Desktop-Wallet/bchdesktopwallet/createtokensdemo.py", line 40, in create_token
    self.key.send(
  File "/home/ipfactory/git/BCH-Desktop-Wallet/env/lib/python3.10/site-packages/bitcash/wallet.py", line 372, in send
    tx_hex = self.create_transaction(
  File "/home/ipfactory/git/BCH-Desktop-Wallet/env/lib/python3.10/site-packages/bitcash/wallet.py", line 305, in create_transaction
    unspents, outputs = sanitize_tx_data(
  File "/home/ipfactory/git/BCH-Desktop-Wallet/env/lib/python3.10/site-packages/bitcash/transaction.py", line 180, in sanitize_tx_data
    cashtoken.subtract_output(output)
  File "/home/ipfactory/git/BCH-Desktop-Wallet/env/lib/python3.10/site-packages/bitcash/cashtoken.py", line 410, in subtract_output
    raise InsufficientFunds("unspent category_id does not exist")
bitcash.exceptions.InsufficientFunds: unspent category_id does not exist

        """

        # Create the token
        self.key.send(
            [
                (
                    self.key.cashtoken_address,  # destination
                    token_amount,  # amount
                    "satoshi",  # currency
                    txid,  # category
                    "minting",  # NFT capability
                    None,  # NFT commitment, None
                    token_amount,  # fungible token amount
                )
            ]
        )

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
