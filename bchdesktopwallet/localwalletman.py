import json
from pathlib import Path
from bitcash import Key

class LocalWalletManager:
    def __init__(self, wallet_file_name='bch-wallet.json'):
        self.wallet_file_path = Path.home() / '.local' / 'share' / 'com.argosopentech.BCH-Desktop-Wallet' / wallet_file_name
        self.wallet_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.wallet_data = self.load_wallet_data()

    def load_wallet_data(self):
        if self.wallet_file_path.exists():
            with open(self.wallet_file_path, 'r') as file:
                return json.load(file)
        else:
            return {'keys': []}

    def save_wallet_data(self):
        with open(self.wallet_file_path, 'w') as file:
            json.dump(self.wallet_data, file, indent=2)

    def create_wallet(self):
        key = Key()
        wallet_entry = {'address': key.address, 'private_key': key.to_int()}
        self.wallet_data['keys'].append(wallet_entry)
        self.save_wallet_data()

    def get_wallets(self):
        return self.wallet_data['keys']

    def get_wallet_by_address(self, address):
        for wallet in self.wallet_data['keys']:
            if wallet['address'] == address:
                return wallet
        return None

if __name__ == '__main__':
    # Example usage:
    wallet_manager = LocalWalletManager()

    # Create a new wallet
    wallet_manager.create_wallet()

    # Get all wallets
    wallets = wallet_manager.get_wallets()
    print("All Wallets:")
    for wallet in wallets:
        print(wallet)

    # Get a wallet by address
    address_to_search = 'bitcoincash:qqqwummkpw72lx6ewhgvc05lj4xayfrtfscvgmr9ca'
    found_wallet = wallet_manager.get_wallet_by_address(address_to_search)
    print(f"\nWallet with Address {address_to_search}:")
    print(found_wallet)

