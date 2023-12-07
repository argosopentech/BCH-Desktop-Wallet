import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from bchdesktopwallet.localwalletman import LocalWalletManager
from bchdesktopwallet.managewalletswidget import ManageWalletsWidget
from bchdesktopwallet.transactionwidget import TransactionWidget
from bchdesktopwallet.viewbalanceswidget import ViewBalancesWidget
from bchdesktopwallet.receivetransactionwidget import ReceiveTransactionWidget
from bchdesktopwallet.privatekeyswidget import PrivateKeyViewer

APPLICATION_NAME = "BCH Desktop Wallet"


class BCHDesktopWallet(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label = QLabel("Bitcoin Cash Desktop Wallet")
        self.manage_wallets_button = QPushButton("Manage Wallets")
        self.manage_wallets_button.clicked.connect(self.manage_wallets_button_clicked)
        self.send_transaction_button = QPushButton("Send Transaction")
        self.send_transaction_button.clicked.connect(
            self.send_transaction_button_clicked
        )
        self.view_balances_button = QPushButton("View Balances")
        self.view_balances_button.clicked.connect(self.view_balances_button_clicked)
        self.receive_transaction_button = QPushButton("Receive Transaction")
        self.receive_transaction_button.clicked.connect(
            self.receive_transaction_button_clicked
        )
        self.private_key_viewer_button = QPushButton("View Private Keys")
        self.private_key_viewer_button.clicked.connect(
            self.private_key_viewer_button_clicked
        )

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.manage_wallets_button)
        layout.addWidget(self.send_transaction_button)
        layout.addWidget(self.view_balances_button)
        layout.addWidget(self.receive_transaction_button)
        layout.addWidget(self.private_key_viewer_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle(APPLICATION_NAME)
        self.setGeometry(
            100, 100, 400, 200
        )  # Set window dimensions (x, y, width, height)

        # Show the window
        self.show()

    def manage_wallets_button_clicked(self):
        self.key_widget = ManageWalletsWidget()
        self.key_widget.setWindowTitle("Manage Wallets")
        self.key_widget.setGeometry(200, 200, 500, 300)
        self.key_widget.show()

    def send_transaction_button_clicked(self):
        self.transaction_widget = TransactionWidget()
        self.transaction_widget.setWindowTitle("Send Transaction")
        self.transaction_widget.setGeometry(200, 200, 500, 300)
        self.transaction_widget.show()

    def view_balances_button_clicked(self):
        self.view_balances_widget = ViewBalancesWidget()
        self.view_balances_widget.setWindowTitle("View Balances")
        self.view_balances_widget.setGeometry(200, 200, 500, 300)
        self.view_balances_widget.show()

    def receive_transaction_button_clicked(self):
        self.receive_transaction_widget = ReceiveTransactionWidget()
        self.receive_transaction_widget.setWindowTitle("Receive Transaction")
        self.receive_transaction_widget.setGeometry(200, 200, 500, 300)
        self.receive_transaction_widget.show()

    def private_key_viewer_button_clicked(self):
        self.private_key_viewer_widget = PrivateKeyViewer()
        self.private_key_viewer_widget.setWindowTitle("View Private Keys")
        self.private_key_viewer_widget.setGeometry(200, 200, 500, 300)
        self.private_key_viewer_widget.show()


def main():
    app = QApplication(sys.argv)
    basic_app = BCHDesktopWallet()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
