import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from bitcash import Key
from pathlib import Path
import json


class LocalWalletManager:
    # Your existing LocalWalletManager code goes here...

    def add_token_to_wallet(self, address, token_name, token_balance):
        for wallet in self.wallet_data["keys"]:
            if wallet["address"] == address:
                if "tokens" not in wallet:
                    wallet["tokens"] = []
                wallet["tokens"].append({"name": token_name, "balance": token_balance})
                self.save_wallet_data()


class TokenCreationWidget(QWidget):
    def __init__(self, local_wallet_manager):
        super(TokenCreationWidget, self).__init__()

        self.local_wallet_manager = local_wallet_manager

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Token Creation")

        self.token_name_label = QLabel("Token Name:", self)
        self.token_name_edit = QLineEdit(self)

        self.token_balance_label = QLabel("Token Balance:", self)
        self.token_balance_edit = QLineEdit(self)

        self.create_token_button = QPushButton("Create Token", self)
        self.create_token_button.clicked.connect(self.create_and_publish_token)

        layout = QVBoxLayout()
        layout.addWidget(self.token_name_label)
        layout.addWidget(self.token_name_edit)
        layout.addWidget(self.token_balance_label)
        layout.addWidget(self.token_balance_edit)
        layout.addWidget(self.create_token_button)

        self.setLayout(layout)

    def create_and_publish_token(self):
        token_name = self.token_name_edit.text()
        token_balance = float(
            self.token_balance_edit.text()
        )  # Assuming balance is a float

        # Create a new token (for simplicity, just a random private key)
        key = Key()
        token_address = key.address

        # Add the token to the current user's wallet
        current_user_address = self.local_wallet_manager.get_wallet_by_address(
            self.local_wallet_manager.wallet_data["keys"][0]["address"]
        )
        if current_user_address:
            self.local_wallet_manager.add_token_to_wallet(
                current_user_address["address"], token_name, token_balance
            )

            # Publish the token information to a central server or share it with other users
            # For simplicity, here we just print the details
            print(
                f"Token Name: {token_name}, Token Address: {token_address}, Token Balance: {token_balance}"
            )
        else:
            print("Error: User's address not found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wallet_manager = LocalWalletManager()
    token_creation_widget = TokenCreationWidget(wallet_manager)
    token_creation_widget.show()

    sys.exit(app.exec_())
