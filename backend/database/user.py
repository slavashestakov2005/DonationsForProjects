from .database import Table, Row
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(Row, UserMixin):
    """
        Строка таблицы UsersTable
        id          INT     NOT NULL    PK  AI  UNIQUE
        login       TEXT    NOT NULL
        password    TEXT    NOT NULL
    """
    fields = ['id', 'login', 'password']

    def __init__(self, row):
        Row.__init__(self, User, row)

    def check_password(self, password) -> bool:
        if self.__is_none__:
            return False
        return check_password_hash(self.password, password)

    def set_password(self, password) -> None:
        if self.__is_none__:
            return
        self.password = generate_password_hash(password)


class UsersTable:
    table = "user"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(UsersTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "login"	TEXT NOT NULL,
        "password"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(UsersTable.table, User)

    @staticmethod
    def select(id: int) -> User:
        return Table.select_one(UsersTable.table, User, 'id', id)

    @staticmethod
    def select_by_login(login: str) -> User:
        return Table.select_one(UsersTable.table, User, 'login', login)

    @staticmethod
    def update(user: User) -> None:
        return Table.update(UsersTable.table, user)

    @staticmethod
    def insert(user: User) -> None:
        return Table.insert(UsersTable.table, user)

    @staticmethod
    def delete(user: User) -> None:
        return Table.delete(UsersTable.table, user)
