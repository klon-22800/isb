import sys

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
from matplotlib import pyplot as plt

import func
import serialization


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
        self.card = func.Card("", "", [])

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

        self.setWindowTitle("Card_bruteforcer")
        QToolTip.setFont(QFont("SansSerif", 10))
        self.setWindowIcon(QIcon("home.png"))

        self.button_card = self.main_window_button_maker(
            "Card bruteforce", self.card_load_window
        )

        self.button_luna_check = self.main_window_button_maker(
            "Luna check", self.luna_check
        )

        self.button_time_test = self.main_window_button_maker(
            "Time test", self.dialogue_window_time_test
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

        self.card_info_label = ScrollLabel(self)
        self.card_info_label.setStyleSheet("background:#f9d4e7; color: #3C5A75; ")

        self.card_bruteforce_label = ScrollLabel(self)
        self.card_bruteforce_label.setStyleSheet("background:#a9d4e7; color: #3C5A75; ")

        self.luna_label = ScrollLabel(self)
        self.luna_label.setStyleSheet("background:#19d4e7; color: #3C5A75; ")

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.button_card, 0, 0)
        layout.addWidget(self.button_luna_check, 1, 0)
        layout.addWidget(self.button_time_test, 2, 0)
        layout.addWidget(self.exit, 3, 0)
        layout.addWidget(self.text_main_label, 0, 2, 4, 1)
        layout.addWidget(self.card_info_label, 0, 3, 1, 1)
        layout.addWidget(self.card_bruteforce_label, 1, 3, 1, 1)
        layout.addWidget(self.luna_label, 2, 3, 2, 1)
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

    def dialogue_window_card_load(self) -> None:
        """
        The function show dialog window to load card info
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Load")
        dialog.setFixedSize(500, 350)

        path_label = QLabel("Choose paths:", dialog)
        path_label.setStyleSheet("color: #C3D0DB; min-height:30%")

        self.path_card = ""
        self.path_card_number = ""

        self.path_line_card = self.path_line_maker(dialog)
        self.path_line_card_number = self.path_line_maker(dialog)

        button_card_info = self.button_maker_dialog(
            "Path to card info", self.get_open_card_info, dialog
        )
        button_card_info_save = self.button_maker_dialog(
            "Path to save card number", self.get_save_card_info, dialog
        )
        button_card_info_view = self.button_maker_dialog(
            "Load info", self.load_card_info, dialog
        )
        button_card_bruteforce = self.button_maker_dialog(
            "Brutforce", self.card_bruteforce, dialog
        )

        layout = QVBoxLayout()
        layout.addWidget(path_label)

        layout.addWidget(self.path_line_card)
        layout.addWidget(button_card_info)
        layout.addWidget(self.path_line_card_number)
        layout.addWidget(button_card_info_save)
        layout.addWidget(button_card_info_view)
        layout.addWidget(button_card_bruteforce)

        dialog.setLayout(layout)

        dialog.exec_()

    def dialogue_window_time_test(self) -> None:
        """
        The function show dialog window to run time test
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Load")
        dialog.setFixedSize(500, 250)

        path_label = QLabel("Choose paths:", dialog)
        path_label.setStyleSheet("color: #C3D0DB; min-height:30%")

        self.path_test = ""

        self.path_line_test = self.path_line_maker(dialog)

        button_test = self.button_maker_dialog(
            "Path to save plot", self.get_save_test, dialog
        )
        button_start_test = self.button_maker_dialog("Save", self.start_test, dialog)

        layout = QVBoxLayout()
        layout.addWidget(path_label)

        layout.addWidget(self.path_line_test)
        layout.addWidget(button_test)
        layout.addWidget(button_start_test)

        dialog.setLayout(layout)

        dialog.exec_()

    def card_load_window(self) -> None:
        """
        Function run window for load card info
        """
        self.dialogue_window_card_load()

    def get_open_card_info(self) -> None:
        """
        The function gets the path to the open file with card info
        """
        self.path_card = (
            QFileDialog.getOpenFileName(self, "Select File", "card.json", "(*.json)")
        )[0].replace("/", "\\")
        if len(self.path_card) > 0:
            self.path_line_card.setText(self.path_card)
        else:
            MessageBox(self, "Incorrect path")
            self.path_encrypted_symmetric_key = ""

    def get_save_card_info(self) -> None:
        """function get path to save card info"""
        self.path_card_number = (
            QFileDialog.getSaveFileName(
                self, "Select File", "card_num.json", "(*.json)"
            )
        )[0].replace("/", "\\")
        if len(self.path_card_number) > 0:
            self.path_line_card_number.setText(self.path_card_number)
        else:
            MessageBox(self, "Incorrect path")
            self.path_card_number = ""

    def load_card_info(self) -> None:
        """function load card info from .json file"""
        info = serialization.read_json(self.path_card)
        last_num = info["LAST_NUM"]
        hash = info["HASH"]
        bin_list = info["BIN_LIST"]
        self.card = func.Card(last_num, hash, bin_list)
        self.card_info_label.setText(
            f"Last_num: {last_num}\n Hash: {hash}\n Bins: {bin_list}"
        )

    def card_bruteforce(self) -> None:
        """function try to brutforce card number and serilize them"""
        MessageBox(self, "Bruteforcing...")
        self.card_num = self.card.num_bruteforce(6)
        self.card_bruteforce_label.setText(str(self.card_num[0]))
        if len(self.path_card_number) > 0:
            serialization.write_json(
                self.path_card_number, {"Number": self.card_num[0]}
            )

    def luna_check(self) -> None:
        """function check card_number by luna algorithm"""
        check = func.luna(self.card_num)
        if check:
            self.luna_label.setText("Карта действительна")
        self.luna_label.setText("Карта не действительна")

    def get_save_test(self) -> None:
        """function get path to save plot of time test"""
        self.path_test = (
            QFileDialog.getSaveFileName(self, "Select File", "test.png", "(*.png)")
        )[0].replace("/", "\\")
        if len(self.path_test) > 0:
            self.path_line_test.setText(self.path_test)
        else:
            MessageBox(self, "Incorrect path")
            self.path_test = ""

    def start_test(self) -> None:
        """frunction start time test"""
        if (
            len(self.card.bin_list) > 0
            and len(self.card.hash) > 0
            and len(self.card.bin_list) > 0
        ):
            test = self.card.time_test()
            x = test[0]
            y = test[1]
            plt.plot(x, y, marker="o")
            plt.title("Зависимость времени от кол-ва потоков")
            plt.ylabel("Время в секундах")
            plt.xlabel("Кол-во потоков")
            plt.savefig(self.path_test)

        else:
            MessageBox(self, "No cards")

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
