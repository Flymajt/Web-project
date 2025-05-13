from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QListWidget,
    QListWidgetItem
)
import os
import json
import string


class Admin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Toney Admin App")
        self.rozlozeni = QVBoxLayout()
        self.setLayout(self.rozlozeni)

        self.users_button = QPushButton("To Users")
        self.users_button.clicked.connect(self.openUsers)
        self.rozlozeni.addWidget(self.users_button)

    def openUsers(self):
        self.detail_window = UserSelect()
        self.detail_window.show()

class UserDetail(QWidget):
    def __init__(self, name, role, password, id):
        super().__init__()
        self.name = name
        self.role = role
        self.password = password
        self.id = id
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.name)

        layout = QVBoxLayout()

        id_label = QLabel(f"UUID: {self.id}")
        layout.addWidget(id_label)

        username_label = QLabel(f"Role: {self.role}")
        layout.addWidget(username_label)

        password_label = QLabel(f"Password: {self.password}")
        layout.addWidget(password_label)

        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class UserSelect(QWidget):
    def __init__(self):
        super().__init__()

        self.data_path = "./static/data/"
        self.users = self.load_user(self.data_path+"users.json")

        self.setWindowTitle("Toney Admin App - Users")
        self.rozlozeni = QVBoxLayout()
        self.setLayout(self.rozlozeni)

        # name_label = QLabel("Name:")
        # self.name_input = QLineEdit()
        #self.rozlozeni.addWidget(name_label)
        #self.rozlozeni.addWidget(self.name_input)

        #ing_label = QLabel("Password:")
        #self.ing_input = QLineEdit()
        #self.rozlozeni.addWidget(ing_label)
        #self.rozlozeni.addWidget(self.ing_input)

        #rec_label = QLabel("role:")
        #self.rec_input = QLineEdit()
        #self.rozlozeni.addWidget(rec_label)
        #self.rozlozeni.addWidget(self.rec_input)

        #self.add_button = QPushButton("Add User")
        #self.add_button.clicked.connect(self.save_user)
        #self.rozlozeni.addWidget(self.add_button)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.show_detail)
        self.refresh_user_list(self.users)
        self.rozlozeni.addWidget(self.list_widget)

    def load_user(self, path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_user(self):
        nazev = self.name_input.text()
        ing = self.ing_input.text()
        rec = self.rec_input.text()
        if not nazev or not ing or not rec:
            QMessageBox.warning(self, "Chyba", "Zadejte název, ingredience a postup.")
            return
        if len(ing) < 20 or len(rec) < 20:
            QMessageBox.warning(self, "Chyba",
                                "Ingredience nebo postup jsou kratší než 20 znaků")
            return
        self.name_input.setText("")
        self.ing_input.setText("")
        self.rec_input.setText("")
        recept = {"name": nazev, "ingredients": ing, "recipe": rec}
        self.recipes.append(recept)
        with open(self.rec_path, "w") as f:
            json.dump(self.recipes, f)
        self.refresh_recipe_list(self.recipes)

    def refresh_user_list(self, recipes):
        self.list_widget.clear()
        for r in recipes:
            name = r["username"]
            item = QListWidgetItem(name)
            self.list_widget.addItem(item)

    def show_detail(self, item):
        name = item.text()
        role = None
        password = None
        uuid = None

        for entry in self.users:
            if entry["username"] == name:
                role = entry["role"]
                password = entry["password"]
                uuid = entry["id"]
                break

        if role is not None and password is not None:
            self.detail_window = UserDetail(name, role, password, uuid)
            self.detail_window.show()
        else:
            QMessageBox.warning(self, "Chyba", f"Recept s názvem {name} nebyl nalezen.")

app = QApplication([])
okno = Admin()
okno.show()
app.exec()