import sys

from bitcash import Key
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bchdesktopwallet.localwalletman import LocalWalletManager


class TransactionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the LocalWalletManager
        self.wallet_manager = LocalWalletManager()

        # Initialize the selected wallet address variable
        self.selected_wallet_address = None

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel("Make Transaction")
        self.wallet_list_label = QLabel("Select Wallet:")
        self.wallet_list_widget = QListWidget()

        self.refresh_wallet_list()

        self.amount_label = QLabel("Amount (USD):")
        self.amount_entry = QLineEdit()

        self.recipient_address_label = QLabel("Recipient Address:")
        self.recipient_address_entry = QLineEdit()

        self.send_button = QPushButton("Send Transaction")
        self.send_button.clicked.connect(self.send_transaction)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.wallet_list_label)
        layout.addWidget(self.wallet_list_widget)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_entry)
        layout.addWidget(self.recipient_address_label)
        layout.addWidget(self.recipient_address_entry)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def refresh_wallet_list(self):
        # Clear the existing items in the list widget
        self.wallet_list_widget.clear()

        # Get all wallets and add them to the list widget
        wallets = self.wallet_manager.get_wallets()
        for wallet in wallets:
            address = wallet["address"]
            self.wallet_list_widget.addItem(address)

        # Connect the item selection signal to the slot
        self.wallet_list_widget.itemSelectionChanged.connect(
            self.handle_wallet_selection
        )

    def handle_wallet_selection(self):
        # Get the selected item from the list widget
        selected_item = self.wallet_list_widget.currentItem()

        if selected_item is not None:
            # Get the address of the selected wallet
            self.selected_wallet_address = selected_item.text()

    def send_transaction(self):
        recipient_address = self.recipient_address_entry.text()

        # Check if a wallet is selected
        if self.selected_wallet_address is None:
            QMessageBox.warning(
                self,
                "No Wallet Selected",
                "Please select a wallet before sending a transaction.",
                QMessageBox.Ok,
            )
            return

        # Get the amount from the entry field
        amount_text = self.amount_entry.text()

        if not amount_text:
            QMessageBox.warning(
                self,
                "Invalid Amount",
                "Please enter a valid amount before sending a transaction.",
                QMessageBox.Ok,
            )
            return

        try:
            # Convert the amount to a float
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Amount",
                "Please enter a valid numeric amount.",
                QMessageBox.Ok,
            )
            return

        # Get the selected wallet
        selected_wallet = self.wallet_manager.get_wallet_by_address(
            self.selected_wallet_address
        )

        if selected_wallet is not None:
            # Create a Key instance for the selected wallet
            key = Key.from_int(selected_wallet["private_key"])

            # Create a list of outputs
            outputs = [(recipient_address, amount, "usd")]

            # Send the transaction
            try:
                transaction_id = key.send(outputs)
            except ValueError as e:
                QMessageBox.warning(
                    self,
                    "Transaction Error",
                    f"Transaction failed: {e}",
                    QMessageBox.Ok,
                )
                return

            # Show a success message
            QMessageBox.information(
                self,
                "Transaction Sent",
                f"Transaction sent!\nTransaction ID: {transaction_id}",
                QMessageBox.Ok,
            )

        else:
            QMessageBox.warning(
                self,
                "Wallet Not Found",
                "Selected wallet not found. Please try again.",
                QMessageBox.Ok,
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    transaction_widget = TransactionWidget()
    transaction_widget.setWindowTitle("Make Transaction")
    transaction_widget.setGeometry(100, 100, 400, 200)
    transaction_widget.show()

    sys.exit(app.exec_())
