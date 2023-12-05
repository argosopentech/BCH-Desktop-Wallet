import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox
from bchdesktopwallet.localwalletman import LocalWalletManager
from bitcash import Key

class ViewBalancesWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the LocalWalletManager
        self.wallet_manager = LocalWalletManager()

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel('View Balances')
        self.wallet_list_label = QLabel('Wallets:')
        self.wallet_list_widget = QListWidget()

        self.refresh_wallet_list()

        self.balance_label = QLabel('Balance (USD):')
        self.balance_display = QLabel('')

        self.refresh_button = QPushButton('Refresh Balances')
        self.refresh_button.clicked.connect(self.refresh_balances)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.wallet_list_label)
        layout.addWidget(self.wallet_list_widget)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.balance_display)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def refresh_wallet_list(self):
        # Clear the existing items in the list widget
        self.wallet_list_widget.clear()

        # Get all wallets and add them to the list widget
        wallets = self.wallet_manager.get_wallets()
        for wallet in wallets:
            address = wallet['address']
            self.wallet_list_widget.addItem(address)

        # Connect the item selection signal to the slot
        self.wallet_list_widget.itemSelectionChanged.connect(self.handle_wallet_selection)

    def handle_wallet_selection(self):
        # Get the selected item from the list widget
        selected_item = self.wallet_list_widget.currentItem()

        if selected_item is not None:
            # Get the address of the selected wallet
            selected_wallet_address = selected_item.text()

            # Get the selected wallet
            selected_wallet = self.wallet_manager.get_wallet_by_address(selected_wallet_address)

            if selected_wallet is not None:
                # Create a Key instance for the selected wallet
                key = Key.from_int(selected_wallet['private_key'])

                # Get the balance for the selected wallet
                balance = key.get_balance('usd')

                # Display the balance
                self.balance_display.setText(str(balance))
            else:
                QMessageBox.warning(self, 'Wallet Not Found', 'Selected wallet not found. Please try again.', QMessageBox.Ok)

    def refresh_balances(self):
        # Clear the balance display
        self.balance_display.clear()

        # Refresh the wallet list to trigger the handle_wallet_selection for the currently selected wallet
        self.refresh_wallet_list()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    view_balances_widget = ViewBalancesWidget()
    view_balances_widget.setWindowTitle('View Balances')
    view_balances_widget.setGeometry(100, 100, 400, 200)
    view_balances_widget.show()

    sys.exit(app.exec_())

