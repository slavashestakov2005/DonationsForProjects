from datetime import datetime
from .database import Table, Row


class Donation(Row):
    """
        Строка таблицы DonationsTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        project         INT     NOT NULL
        name            TEXT    NOT NULL
        amount          INT     NOT NULL
        other_info      TEXT    NOT NULL
        status          INT     NOT NULL
        payment         INT     NOT NULL
        time            INT     NOT NULL
    """
    fields = ['id', 'project', 'name', 'amount', 'other_info', 'status', 'payment', 'time']
    REQUEST_SUBMITTED, PAID, NOT_PAID, ERROR = 0, 1, 2, 3
    STATUSES = ['Заявка подана', 'Оплачено', 'Не оплачено', 'Ошибка']

    def __init__(self, row):
        Row.__init__(self, Donation, row)

    def get_status(self):
        return Donation.STATUSES[self.status]

    def get_time(self):
        return datetime.fromtimestamp(self.time).strftime('%Y.%m.%d %H:%M:%S')


class DonationsTable:
    table = "donation"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(DonationsTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "project"	INTEGER NOT NULL,
        "name"	TEXT NOT NULL,
        "amount"	INTEGER NOT NULL,
        "other_info"	TEXT NOT NULL,
        "status"	INTEGER NOT NULL,
        "payment"	INTEGER NOT NULL,
        "time"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(DonationsTable.table, Donation)

    @staticmethod
    def select(id: int) -> Donation:
        return Table.select_one(DonationsTable.table, Donation, 'id', id)

    @staticmethod
    def select_last() -> Donation:
        return Table.select_last(DonationsTable.table, Donation)

    @staticmethod
    def select_by_project(project: int) -> list:
        return Table.select_list(DonationsTable.table, Donation, 'project', project)

    @staticmethod
    def update(donation: Donation) -> None:
        return Table.update(DonationsTable.table, donation)

    @staticmethod
    def insert(donation: Donation) -> None:
        return Table.insert(DonationsTable.table, donation)

    @staticmethod
    def delete(donation: Donation) -> None:
        return Table.delete(DonationsTable.table, donation)
