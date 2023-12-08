import bchdesktopwallet.localwalletman as localwalletman
from bitcash import Key


class TokenMan:
    def __init__(self, wallet_manager):
        self.wallet_manager = wallet_manager

    def create_token(self, token_name, token_symbol, token_amount):
        pass
