# receivetransactionwidget.py
import sys

from bitcash import Key
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from bchdesktopwallet.localwalletman import LocalWalletManager


class ReceiveTransactionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the LocalWalletManager
        self.wallet_manager = LocalWalletManager()

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.label = QLabel("Receive Transaction")
        self.wallet_list_label = QLabel("Select Wallet:")
        self.wallet_list_widget = QListWidget()

        self.refresh_wallet_list()

        self.address_label = QLabel("Your Wallet Address:")
        self.address_display = QTextEdit()
        self.address_display.setReadOnly(True)

        self.address_type_label = QLabel("Select Address Type:")
        self.address_type_combobox = QComboBox()
        self.address_type_combobox.addItems(["Bitcoin Cash (BCH)", "Bitcoin CashToken"])
        self.address_type_combobox.currentIndexChanged.connect(
            self.handle_address_type_change
        )

        self.copy_button = QPushButton("Copy Address to Clipboard")
        self.copy_button.clicked.connect(self.copy_address_to_clipboard)

        self.qr_code_label = QLabel()
        self.qr_code_label.setAlignment(QtCore.Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.wallet_list_label)
        layout.addWidget(self.wallet_list_widget)
        layout.addWidget(self.address_type_label)
        layout.addWidget(self.address_type_combobox)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_display)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.qr_code_label)

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
            selected_wallet_address = selected_item.text()

            # Get the current index of the address type combo box
            index = self.address_type_combobox.currentIndex()

            # Update the displayed address based on the selected address type
            private_key = self.wallet_manager.get_private_key(selected_wallet_address)
            if private_key is not None:
                if index == 1:  # Bitcoin CashToken selected
                    key = Key.from_int(private_key)
                    selected_wallet_address = key.cashtoken_address

            # Display the selected wallet address
            self.address_display.setPlainText(selected_wallet_address)

    def handle_address_type_change(self, index):
        # Update the displayed address based on the selected address type
        selected_wallet_address = self.address_display.toPlainText()
        private_key = self.wallet_manager.get_private_key(selected_wallet_address)

        if private_key is not None:
            if index == 1:  # Bitcoin CashToken selected
                key = Key.from_int(private_key)
                selected_wallet_address = key.cashtoken_address

        self.address_display.setPlainText(selected_wallet_address)

    def copy_address_to_clipboard(self):
        # Get the current text from the address display
        address_to_copy = self.address_display.toPlainText()

        # Copy the address to the clipboard
        QApplication.clipboard().setText(address_to_copy)

        # Show a success message
        QMessageBox.information(
            self,
            "Address Copied",
            "Wallet address copied to clipboard!",
            QMessageBox.Ok,
        )

        # Display the QR code
        self.display_qr_code(address_to_copy)

    def display_qr_code(self, data):
        from io import BytesIO

        import qrcode
        from PyQt5.QtGui import QPixmap

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        qr_code_pixmap = QPixmap()
        qr_code_pixmap.loadFromData(buffer.getvalue())

        self.qr_code_label.setPixmap(qr_code_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    receive_transaction_widget = ReceiveTransactionWidget()
    receive_transaction_widget.setWindowTitle("Receive Transaction")
    receive_transaction_widget.setGeometry(100, 100, 400, 250)
    receive_transaction_widget.show()

    sys.exit(app.exec_())
