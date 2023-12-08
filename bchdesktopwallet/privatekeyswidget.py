import json
import sys
from pathlib import Path

from bitcash import Key
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from bchdesktopwallet.localwalletman import LocalWalletManager


class PrivateKeyViewer(QWidget):
    def __init__(self):
        super(PrivateKeyViewer, self).__init__()

        self.local_wallet_manager = LocalWalletManager()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Private Key Viewer")

        self.address_list_widget = QListWidget(self)
        self.address_list_widget.addItems(
            [wallet["address"] for wallet in self.local_wallet_manager.get_wallets()]
        )
        self.address_list_widget.itemClicked.connect(self.show_private_key)

        self.private_key_label = QLabel(self)
        self.private_key_label.setAlignment(Qt.AlignCenter)

        self.copy_button = QPushButton("Copy Private Key", self)
        self.copy_button.clicked.connect(self.copy_private_key)

        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.clicked.connect(self.refresh_address_list)

        self.path_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.address_list_widget)
        layout.addWidget(self.private_key_label)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.path_label)

        self.setLayout(layout)

    def show_private_key(self, item):
        selected_address = item.text()
        wallet = self.local_wallet_manager.get_wallet_by_address(selected_address)

        if wallet:
            private_key = wallet["private_key"]
            self.private_key_label.setText(
                f"Private Key for {selected_address}: {private_key}"
            )
        else:
            self.private_key_label.setText(
                "No private key found for the selected address."
            )

        self.path_label.setText(
            f"Private keys stored in: {self.local_wallet_manager.wallet_file_path}"
        )

    def copy_private_key(self):
        private_key_text = self.private_key_label.text().split(": ")[-1]
        clipboard = QApplication.clipboard()
        clipboard.setText(private_key_text)

    def refresh_address_list(self):
        self.address_list_widget.clear()
        self.address_list_widget.addItems(
            [wallet["address"] for wallet in self.local_wallet_manager.get_wallets()]
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    private_key_viewer = PrivateKeyViewer()
    private_key_viewer.show()

    sys.exit(app.exec_())
