import sys

from bitcash import Key
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import bchdesktopwallet.cashtokenman
from bchdesktopwallet.localwalletman import LocalWalletManager


class WalletTokenWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.wallet_manager = LocalWalletManager()
        self.wallets = self.wallet_manager.get_wallets()
        self.wallet = self.wallets[0]
        self.tm = bchdesktopwallet.cashtokenman.CashTokenManager(
            Key.from_int(self.wallet["private_key"])
        )

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        create_token_button = QPushButton("Create Token")
        create_token_button.clicked.connect(self.create_token)

        view_balance_button = QPushButton("View Token Balance")
        view_balance_button.clicked.connect(self.view_token_balance)

        self.token_name_input = QLineEdit()
        self.token_symbol_input = QLineEdit()
        self.token_amount_input = QLineEdit()

        self.view_token_display = QTextEdit()
        self.view_token_display.setReadOnly(True)

        layout.addWidget(QLabel("Token Name:"))
        layout.addWidget(self.token_name_input)
        layout.addWidget(QLabel("Token Symbol:"))
        layout.addWidget(self.token_symbol_input)
        layout.addWidget(QLabel("Token Amount:"))
        layout.addWidget(self.token_amount_input)
        layout.addWidget(create_token_button)
        layout.addWidget(view_balance_button)
        layout.addWidget(self.view_token_display)

        self.setLayout(layout)
        self.setWindowTitle("CashToken Manager")

    def create_token(self):
        token_name = self.token_name_input.text()
        token_symbol = self.token_symbol_input.text()
        token_amount = int(self.token_amount_input.text())
        self.tm.create_token(token_name, token_symbol, token_amount)

    def view_token_balance(self):
        balance = self.tm.get_token_balance()
        self.view_token_display.setText(str(balance))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = WalletTokenWidget()
    widget.show()
    sys.exit(app.exec_())
