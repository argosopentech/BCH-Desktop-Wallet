import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox
from bchdesktopwallet.localwalletman import LocalWalletManager

class ManageWalletsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the LocalWalletManager
        self.wallet_manager = LocalWalletManager()

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel('Manage Wallets')
        self.wallet_list_label = QLabel('Wallets:')
        self.wallet_list_widget = QListWidget()

        self.refresh_wallet_list()

        self.create_button = QPushButton('Create Wallet')
        self.create_button.clicked.connect(self.create_wallet)

        self.delete_button = QPushButton('Delete Selected Wallet')
        self.delete_button.clicked.connect(self.delete_selected_wallet)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.wallet_list_label)
        layout.addWidget(self.wallet_list_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def refresh_wallet_list(self):
        # Clear the existing items in the list widget
        self.wallet_list_widget.clear()

        # Get all wallets and add them to the list widget
        wallets = self.wallet_manager.get_wallets()
        for wallet in wallets:
            address = wallet['address']
            self.wallet_list_widget.addItem(address)

    def create_wallet(self):
        # Create a new wallet using the LocalWalletManager
        self.wallet_manager.create_wallet()

        # Refresh the wallet list
        self.refresh_wallet_list()

    def delete_selected_wallet(self):
        # Get the selected item from the list widget
        selected_item = self.wallet_list_widget.currentItem()

        if selected_item is not None:
            # Get the address of the selected wallet
            address_to_delete = selected_item.text()

            # Show a confirmation dialog before deleting
            confirmation = QMessageBox.question(self, 'Delete Wallet', f'Delete wallet with address: {address_to_delete}?', QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                # Delete the wallet using the LocalWalletManager
                self.wallet_manager.wallet_data['keys'] = [wallet for wallet in self.wallet_manager.wallet_data['keys'] if wallet['address'] != address_to_delete]

                # Save the updated wallet data
                self.wallet_manager.save_wallet_data()

                # Refresh the wallet list
                self.refresh_wallet_list()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    manage_wallets_widget = ManageWalletsWidget()
    manage_wallets_widget.setWindowTitle('Manage Wallets')
    manage_wallets_widget.setGeometry(100, 100, 400, 300)
    manage_wallets_widget.show()

    sys.exit(app.exec_())

