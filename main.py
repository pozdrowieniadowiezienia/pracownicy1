import os
import re
import sys

from PyQt6.QtWidgets import QDialog, QApplication, QMessageBox

from layout import Ui_Dialog


class MyForm(QDialog):

    def read_from_file(self):
        self.ui.employeesList.clear()
        with open("./employees.txt", "r") as text_file:
            for item in text_file:
                item_sanitized = item.replace("\n", "")
                self.ui.employeesList.addItem(f"{item_sanitized}")

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.submit.clicked.connect(self.save)
        self.read_from_file()
        self.show()

    def is_valid_phone_number(self, phone_number):
        pattern = r"^[0-9]{9}$"
        return phone_number is not None and re.search(pattern, phone_number) is not None

    def is_valid_id(self, id):
        if id is None:
            return False
        weight = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        checksum = sum(int(id[i]) * weight[i] for i in range(10))
        print(checksum)
        checknum = checksum % 10
        print(checknum)
        if checknum == int(id[10]):
            return True
        else:
            return False

    def error_alert(self, msg):
        mb = QMessageBox()
        mb.setText(f"{msg}")
        mb.exec()
    def add_new_employee(self):
        if self.ui.nameEdit.text() is None:
            self.error_alert("Name cannot be empty!")
            return
        if self.ui.surname.text() is None:
            self.error_alert("Surname cannot be empty!")
            return
        name = self.ui.nameEdit.text()
        surname = self.ui.surname.text()
        self.ui.employeesList.addItem(f"{name} {surname}")


    def save_to_file(self):
        with open("./employees.txt", "a") as text_file:
            if os.stat("./employees.txt").st_size == 0:
                text_file.write(f"{self.ui.nameEdit.text()} {self.ui.surname.text()}")
            else:
                text_file.write(f"\n{self.ui.nameEdit.text()} {self.ui.surname.text()}")
        self.read_from_file()



    def save(self):
        if self.is_valid_phone_number(phone_number=self.ui.phoneNumber.text()):
            if self.is_valid_id(self.ui.id.text()):
                self.ui.result.setText("")
                self.add_new_employee()
                self.save_to_file()
            else:
                self.error_alert("ID is not valid!")
        else:
            self.error_alert("Phone number is not valid!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec())
