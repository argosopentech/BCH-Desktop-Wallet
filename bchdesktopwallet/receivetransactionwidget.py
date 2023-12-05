import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox, QTextEdit
from bchdesktopwallet.localwalletman import LocalWalletManager

class ReceiveTransactionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the LocalWalletManager
        self.wallet_manager = LocalWalletManager()

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel('Receive Transaction')
        self.wallet_list_label = QLabel('Select Wallet:')
        self.wallet_list_widget = QListWidget()

        self.refresh_wallet_list()

        self.address_label = QLabel('Your Wallet Address:')
        self.address_display = QTextEdit()
        self.address_display.setReadOnly(True)

        self.copy_button = QPushButton('Copy Address to Clipboard')
        self.copy_button.clicked.connect(self.copy_address_to_clipboard)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.wallet_list_label)
        layout.addWidget(self.wallet_list_widget)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_display)
        layout.addWidget(self.copy_button)

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

            # Display the selected wallet address
            self.address_display.setPlainText(selected_wallet_address)

    def copy_address_to_clipboard(self):
        # Get the current text from the address display
        address_to_copy = self.address_display.toPlainText()

        # Copy the address to the clipboard
        QApplication.clipboard().setText(address_to_copy)

        # Show a success message
        QMessageBox.information(self, 'Address Copied', 'Wallet address copied to clipboard!', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    receive_transaction_widget = ReceiveTransactionWidget()
    receive_transaction_widget.setWindowTitle('Receive Transaction')
    receive_transaction_widget.setGeometry(100, 100, 400, 200)
    receive_transaction_widget.show()

    sys.exit(app.exec_())

