from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import pyqtSignal, pyqtSlot


class LobbyUI(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        main_layout = QVBoxLayout()
        name_lb = QLabel('__name__')
        info_lb = QLabel('__info__')
        match_bt = QPushButton('Match / Cancel')
        stat_lb = QLabel('waiting for match...\nNow Player: 1/2')
        logout_bt = QPushButton('LogOut')  # set_Enable 사용

        main_layout.addWidget(name_lb)
        main_layout.addWidget(info_lb)
        main_layout.addWidget(match_bt)
        main_layout.addWidget(stat_lb)
        main_layout.addWidget(logout_bt)

        self.setLayout(main_layout)
        self.setWindowTitle('PyTris')
        self.resize(250, 300)
        self.show()


class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        main_layout = QVBoxLayout()

        input_layout = QGridLayout()
        id_lb = QLabel('UserName')
        pw_lb = QLabel('PassWord')
        id_le = QLineEdit()
        pw_le = QLineEdit()
        input_layout.addWidget(id_lb, 0, 0)
        input_layout.addWidget(id_le, 0, 1)
        input_layout.addWidget(pw_lb, 1, 0)
        input_layout.addWidget(pw_le, 1, 1)

        login_bt = QPushButton('Login')
        exit_bt = QPushButton('Exit')

        main_layout.addLayout(input_layout)
        main_layout.addWidget(login_bt)
        main_layout.addWidget(exit_bt)

        self.setLayout(main_layout)
        self.setWindowTitle('PyTris')
        self.resize(250, 300)
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    ui = LoginUI()
    app.exec()