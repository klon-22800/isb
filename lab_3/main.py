import sys

import serialize

from typing import Callable

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QPushButton,
    QToolTip,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
    QDialog,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QComboBox,
)
from PyQt5.QtGui import QFont, QIcon

from crypto_lib import Symmetrical, Asymmetrical


class MessageBox:
    def __init__(self, parent: QWidget, text: str) -> None:
        """constructor of MessageBox
        Args:
            parent (_type_): QWidget
            text (str): text to show
        """
        message_box = QMessageBox(parent)
        message_box.setText(text)
        ok_button = message_box.addButton(QMessageBox.Ok)
        ok_button.setStyleSheet(
            "background:#0e172c; border-radius: 5px; min-width: 100px;"
        )
        message_box.setStyleSheet("color: white")
        message_box.exec_()


class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs) -> None:
        """
        Constructor of ScrollLabel
        """
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        text = QWidget(self)
        self.setWidget(text)
        lay = QVBoxLayout(text)
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)
        self.label.setFont(QFont("SansSerif", 15))

    def setText(self, text: str) -> None:
        """The function set text to ScrollLabel object

        Args:
            text (str): text to set
        """
        self.label.setText(text)


class Window(QWidget):
    def __init__(self) -> None:
        """
        Constructor of main Window
        """
        super().__init__()
        self.initUI()
        self.setStyleSheet(
            "background:#061E33; color: #C3D0DB; font-weight:bold; border-radius: 5px;"
        )
        self.sym = Symmetrical()
        self.asym = Asymmetrical()
        self.block_size = 0

    def main_window_button_maker(self, text: str, function: Callable) -> QPushButton:
        """function for making button on main window

        Args:
            text (str): text on button
            function (Callable): function for connecting

        Returns:
            QPushButton: QPushButton elem
        """
        button = QPushButton(text, self)
        button.adjustSize()
        button.setFont(QFont("Arial", 15))
        button.setStyleSheet(
            "background:#3C5A75; border-radius: 5px; min-width: 300px; min-height: 200px;"
        )
        button.clicked.connect(function)
        return button

    def initUI(self) -> None:
        """
        The function create an UI object of main Window
        """
        self.showFullScreen()

        self.setWindowTitle("Encoder")
        QToolTip.setFont(QFont("SansSerif", 10))
        self.setWindowIcon(QIcon("home.png"))

        self.button_key_generator = self.main_window_button_maker(
            "Hybrid system \n key generation", self.key_window
        )

        self.button_data_encryption = self.main_window_button_maker(
            "Data encryption with\n a hybrid system", self.encryption_window
        )

        self.button_data_decryption = self.main_window_button_maker(
            "Data decryption with\n a hybrid system", self.decryption_window
        )

        self.exit = QPushButton("Exit", self)
        self.exit.adjustSize()
        self.exit.setFont(QFont("Arial", 15))
        self.exit.setStyleSheet(
            "background:#8C5A75; border-radius: 5px; min-width: 300px; min-height: 200px;"
        )
        self.exit.clicked.connect(self.choice_exit)

        self.text_main_label = ScrollLabel(self)
        self.text_main_label.setStyleSheet("background:#d9d4e7; color: #3C5A75; ")

        self.symmetric_key_label = ScrollLabel(self)
        self.symmetric_key_label.setStyleSheet("background:#f9d4e7; color: #3C5A75; ")

        self.private_key_label = ScrollLabel(self)
        self.private_key_label.setStyleSheet("background:#a9d4e7; color: #3C5A75; ")

        self.public_key_label = ScrollLabel(self)
        self.public_key_label.setStyleSheet("background:#19d4e7; color: #3C5A75; ")

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.button_key_generator, 0, 0)
        layout.addWidget(self.button_data_encryption, 1, 0)
        layout.addWidget(self.button_data_decryption, 2, 0)
        layout.addWidget(self.exit, 3, 0)
        layout.addWidget(self.text_main_label, 0, 2, 4, 1)
        layout.addWidget(self.symmetric_key_label, 0, 3, 1, 1)
        layout.addWidget(self.private_key_label, 1, 3, 1, 1)
        layout.addWidget(self.public_key_label, 2, 3, 2, 1)
        self.show()

    def button_maker_dialog(self, text: str, function, dialog: QDialog) -> QPushButton:
        """function for making button in dialogue window

        Args:
            text (str): text on button
            function (_type_): function for connecting
            dialog (QDialog): dialogue window

        Returns:
            QPushButton: QPushButton elem
        """
        button = QPushButton(text, dialog)
        button.setFont(QFont("Sanserif", 10))
        button.clicked.connect(function)
        button.setStyleSheet(
            "background:#3C5A75; border-radius: 5px; min-height:30%; margin-bottom: 10px;"
        )
        button.adjustSize()
        return button

    def path_line_maker(self, dialog: QDialog) -> QLineEdit:
        """function for making path_line

        Args:
            dialog (QDialog): dialogue window

        Returns:
            QLineEdit: QLineEdit elem
        """
        path_line_edit = QLineEdit(dialog)
        path_line_edit.setEnabled(False)
        path_line_edit.setTextMargins(10, 10, 10, 10)
        path_line_edit.setStyleSheet(
            "background:#d9d4e7; border-radius: 5px; color: #0e172c; min-height:30%;"
        )
        return path_line_edit

    def combo_maker(self, args: list[str]) -> QComboBox:
        """function for making combobox elem

        Args:
            args (list[str]): list of args for combobox

        Returns:
            QComboBox: QComboBox elem
        """
        combo = QComboBox(self)
        combo.setStyleSheet(
            "background:#d9d4e7; color: #0e172c; margin-bottom:10px; padding:2px;"
        )
        combo.setFont(QFont("Sanserif", 9))
        combo.addItems(args)
        return combo

    def dialogue_window_key_generator(self) -> None:
        """
        The function show dialog window to generate keys
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Load")
        dialog.setFixedSize(500, 400)

        path_label = QLabel("Choose paths:", dialog)
        path_label.setStyleSheet("color: #C3D0DB; min-height:30%")

        self.path_encrypted_symmetric_key = ""
        self.path_public_key = ""
        self.path_private_key = ""

        self.path_line_encrypted_symmetric_key = self.path_line_maker(dialog)
        self.path_line_public_key = self.path_line_maker(dialog)
        self.path_line_private_key = self.path_line_maker(dialog)

        button_encrypted_symmetric_key = self.button_maker_dialog(
            "Path to save encrypted symmetric key", self.get_save_symmetric_key, dialog
        )
        button_public_key = self.button_maker_dialog(
            "Path to save public key", self.get_save_public_key, dialog
        )
        button_private_key = self.button_maker_dialog(
            "Path to save private key", self.get_save_private_key, dialog
        )
        button_key_generate = self.button_maker_dialog(
            "Generate keys", self.generate_keys, dialog
        )

        self.key_len = self.combo_maker(["16", "24", "32"])

        layout = QVBoxLayout()
        layout.addWidget(path_label)
        layout.addWidget(self.key_len)

        layout.addWidget(self.path_line_encrypted_symmetric_key)
        layout.addWidget(button_encrypted_symmetric_key)

        layout.addWidget(self.path_line_public_key)
        layout.addWidget(button_public_key)

        layout.addWidget(self.path_line_private_key)
        layout.addWidget(button_private_key)

        layout.addWidget(button_key_generate)
        dialog.setLayout(layout)

        dialog.exec_()

    def dialogue_window_crypt(self) -> None:
        """
        The function show dialog window to encrypt or decrypt text
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Load")
        dialog.setFixedSize(500, 500)

        path_label = QLabel("Choose paths:", dialog)
        path_label.setStyleSheet("color: #C3D0DB; min-height:30%")

        self.path_to_open_text = ""
        self.path_private_key = ""
        self.path_encrypted_symmetric_key = ""
        self.path_to_save_text = ""

        self.path_line_open_text = self.path_line_maker(dialog)
        self.path_line_private_key = self.path_line_maker(dialog)
        self.path_line_encrypted_symmetric_key = self.path_line_maker(dialog)
        self.path_line_save_text = self.path_line_maker(dialog)

        path_to_open_text_button = self.button_maker_dialog(
            "Choose path to text", self.get_path_to_open, dialog
        )
        path_to_private_key_button = self.button_maker_dialog(
            "Choose private key", self.get_open_private_key, dialog
        )
        path_to_encr_symmetric_key_button = self.button_maker_dialog(
            "Choose encrypted symmetric key", self.get_open_symmetric_key, dialog
        )
        path_to_save_text_button = self.button_maker_dialog(
            "Choose path to save text", self.get_path_to_save, dialog
        )

        if self.mode == "encrypt":
            button_crypt = self.button_maker_dialog(
                "Encrypt", self.encrypt_text, dialog
            )
        elif self.mode == "decrypt":
            button_crypt = self.button_maker_dialog(
                "Decrypt", self.decrypt_text, dialog
            )

        layout = QVBoxLayout()
        layout.addWidget(path_label)

        layout.addWidget(self.path_line_open_text)
        layout.addWidget(path_to_open_text_button)

        layout.addWidget(self.path_line_private_key)
        layout.addWidget(path_to_private_key_button)

        layout.addWidget(self.path_line_encrypted_symmetric_key)
        layout.addWidget(path_to_encr_symmetric_key_button)

        layout.addWidget(self.path_line_save_text)
        layout.addWidget(path_to_save_text_button)
        layout.addWidget(button_crypt)

        dialog.setLayout(layout)

        dialog.exec_()

    def key_window(self) -> None:
        """
        Function run window for key generation
        """
        self.dialogue_window_key_generator()

    def encryption_window(self) -> None:
        """
        Function switch mode to 'encrypt' and run dialogue_window with this mode
        """
        self.mode = "encrypt"
        self.dialogue_window_crypt()

    def decryption_window(self) -> None:
        """
        Function switch mode to 'decrupt' and run dialogue_window with this mode
        """
        self.mode = "decrypt"
        self.dialogue_window_crypt()

    def get_save_symmetric_key(self) -> None:
        """
        The function gets the path to the save symmetric key
        """
        self.path_encrypted_symmetric_key = (
            QFileDialog.getSaveFileName(
                self, "Select File", "symmetric_key.txt", "(*.txt)"
            )
        )[0].replace("/", "\\")
        if len(self.path_encrypted_symmetric_key) > 0:
            self.path_line_encrypted_symmetric_key.setText(
                self.path_encrypted_symmetric_key
            )
        else:
            MessageBox(self, "Incorrect path")
            self.path_encrypted_symmetric_key = ""

    def get_save_public_key(self) -> None:
        """
        The function gets the path to the save public key in .pem file
        """
        self.path_public_key = (
            QFileDialog.getSaveFileName(
                self, "Select File", "public_key.pem", "(*.pem)"
            )
        )[0].replace("/", "\\")
        if len(self.path_public_key) > 0:
            self.path_line_public_key.setText(self.path_public_key)
        else:
            MessageBox(self, "Incorrect path")
            self.path_public_key = ""

    def get_save_private_key(self) -> None:
        """
        The function gets the path to the save private key in .pem file
        """
        self.path_private_key = (
            QFileDialog.getSaveFileName(
                self, "Select File", "private_key.pem", "(*.pem)"
            )
        )[0].replace("/", "\\")
        if len(self.path_private_key) > 0:
            self.path_line_private_key.setText(self.path_private_key)
        else:
            MessageBox(self, "Incorrect path")
            self.path_private_key = ""

    def get_open_symmetric_key(self) -> None:
        """
        The function gets the path to the open symmetric key
        """
        self.path_encrypted_symmetric_key = (
            QFileDialog.getOpenFileName(
                self, "Select File", "symmetric_key.txt", "(*.txt)"
            )
        )[0].replace("/", "\\")
        if len(self.path_encrypted_symmetric_key) > 0:
            self.path_line_encrypted_symmetric_key.setText(
                self.path_encrypted_symmetric_key
            )
        else:
            MessageBox(self, "Incorrect path")
            self.path_encrypted_symmetric_key = ""

    def get_open_public_key(self) -> None:
        """
        The function gets the path to the open .pem file with public key
        """
        self.path_encr_public_key = (
            QFileDialog.getOpenFileName(
                self, "Select File", "public_key.pem", "(*.pem)"
            )
        )[0].replace("/", "\\")
        if len(self.path_encr_public_key) > 0:
            self.path_line_encrypted_symmetric_key.setText(self.path_encr_public_key)
        else:
            MessageBox(self, "Incorrect path")
            self.path_encr_public_key = ""

    def get_open_private_key(self) -> None:
        """
        The function gets the path to the open .pem file with private key
        """
        self.path_private_key = (
            QFileDialog.getOpenFileName(
                self, "Select File", "private_key.pem", "(*.pem)"
            )
        )[0].replace("/", "\\")
        if len(self.path_private_key) > 0:
            self.path_line_private_key.setText(self.path_private_key)
        else:
            MessageBox(self, "Incorrect path")
            self.path_private_key = ""

    def generate_keys(self) -> None:
        """function generate keys and serialize them in files"""
        try:
            self.block_size = int(self.key_len.currentText())
            decr_symmetric_key = self.sym.key_generate(self.block_size)
            assym_keys = self.asym.key_generate()
            private_key = assym_keys[0]
            public_key = assym_keys[1]
            serialize.write_private_key(self.path_private_key, private_key)
            serialize.wrute_public_key(self.path_public_key, public_key)
            encrypted_symmetric_key = self.asym.encrypt_symmetrical_key(
                decr_symmetric_key,
                self.path_public_key,
                self.path_encrypted_symmetric_key,
            )
            self.public_key_label.setText(str(public_key))
            self.symmetric_key_label.setText(str(encrypted_symmetric_key))
            self.private_key_label.setText(str(private_key))
            MessageBox(self, "Complete")
        except Exception as ex:
            MessageBox(self, ex)

    def encrypt_text(self) -> None:
        """function encrypt text"""
        key_len = self.block_size
        symmetric_key = self.asym.decrypt_symmetrical_key(
            self.path_encrypted_symmetric_key, self.path_private_key
        )
        encr_text = self.sym.encrypt_text(
            self.path_to_open_text, symmetric_key, self.path_to_save_text, key_len * 8
        )
        self.text_main_label.setText(str(encr_text))

    def decrypt_text(self) -> str:
        """function decrypt text

        Returns:
            str: decrypted text
        """
        key_len = self.block_size
        symmetric_key = self.asym.decrypt_symmetrical_key(
            self.path_encrypted_symmetric_key, self.path_private_key
        )
        decr_text = self.sym.decrypt_text(
            symmetric_key, self.path_to_open_text, self.path_to_save_text, key_len * 8
        )
        self.text_main_label.setText(str(decr_text))
        return decr_text

    def get_path_to_save(self) -> None:
        """
        The function gets the path to the save file
        """
        self.path_to_save_text = (
            QFileDialog.getSaveFileName(self, "Select File", "", "Text files (*.txt)")
        )[0].replace("/", "\\")
        if len(self.path_to_save_text) > 0:
            self.path_line_save_text.setText(self.path_to_save_text)
        else:
            MessageBox(self, "Incorrect path")
            self.path_to_save_text = ""

    def get_path_to_open(self) -> None:
        """
        The function gets the path to the save file
        """
        self.path_to_open_text = (
            QFileDialog.getOpenFileName(self, "Select File", "", "Text files (*.txt)")
        )[0].replace("/", "\\")
        self.path_line_open_text.setText(self.path_to_open_text)

    def choice_exit(self) -> None:
        """
        The function closes the program
        """
        sys.exit()


def run() -> None:
    """
    The function makes a main Window and show it
    """
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
