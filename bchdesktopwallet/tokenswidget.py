import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QPushButton,
)
from PyQt5.QtCore import Qt
from bitcash import Key
from pathlib import Path
import json
from bchdesktopwallet.localwalletman import LocalWalletManager


class TokenViewer(QWidget):
    def __init__(self, local_wallet_manager):
        super(TokenViewer, self).__init__()

        self.local_wallet_manager = local_wallet_manager

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Token Viewer")

        self.address_list_widget = QListWidget(self)
        self.address_list_widget.addItems(
            [wallet["address"] for wallet in self.local_wallet_manager.get_wallets()]
        )
        self.address_list_widget.itemClicked.connect(self.show_tokens)

        self.tokens_label = QLabel(self)
        self.tokens_label.setAlignment(Qt.AlignCenter)

        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.clicked.connect(self.refresh_address_list)

        layout = QVBoxLayout()
        layout.addWidget(self.address_list_widget)
        layout.addWidget(self.tokens_label)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def show_tokens(self, item):
        selected_address = item.text()
        wallet = self.local_wallet_manager.get_wallet_by_address(selected_address)

        if wallet and "tokens" in wallet:
            tokens_info = "\n".join(
                [f"{token['name']}: {token['balance']}" for token in wallet["tokens"]]
            )
            self.tokens_label.setText(f"Tokens for {selected_address}:\n{tokens_info}")
        else:
            self.tokens_label.setText("No tokens found for the selected address.")

    def refresh_address_list(self):
        self.address_list_widget.clear()
        self.address_list_widget.addItems(
            [wallet["address"] for wallet in self.local_wallet_manager.get_wallets()]
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wallet_manager = LocalWalletManager()
    token_viewer = TokenViewer(wallet_manager)
    token_viewer.show()

    sys.exit(app.exec_())
