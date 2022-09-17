from .database import Table, Row


class Project(Row):
    """
        Строка таблицы ProjectsTable
        id                  INT     NOT NULL    PK  AI  UNIQUE
        name                TEXT    NOT NULL
        description         TEXT    NOT NULL
        photo               TEXT    NOT NULL
        cost                INT     NOT NULL
        received            INT     NOT NULL
        author              TEXT    NOT NULL
        author_contacts     TEXT    NOT NULL
        executor            TEXT    NOT NULL
        executor_contacts   TEXT    NOT NULL
        other_info          TEXT    NOT NULL
        public              TEXT    NOT NULL
    """
    fields = ['id', 'name', 'description', 'photo', 'cost', 'received', 'author', 'author_contacts', 'executor',
              'executor_contacts', 'other_info', 'public']

    def __init__(self, row):
        Row.__init__(self, Project, row)

    def set_public(self, public):
        self.public = '1' if public else '0'

    def get_status(self):
        return 'Опубликовано' if self.public == '1' else 'Предложено'

    def is_public(self):
        return self.public == '1'


class ProjectsTable:
    table = "project"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(ProjectsTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        "description"	TEXT NOT NULL,
        "photo"	TEXT NOT NULL,
        "cost"	INTEGER NOT NULL,
        "received"	INTEGER NOT NULL,
        "author"	TEXT NOT NULL,
        "author_contacts"	TEXT NOT NULL,
        "executor"	TEXT NOT NULL,
        "executor_contacts"	TEXT NOT NULL,
        "other_info"	TEXT NOT NULL,
        "public"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(ProjectsTable.table, Project)

    @staticmethod
    def select(id: int) -> Project:
        return Table.select_one(ProjectsTable.table, Project, 'id', id)

    @staticmethod
    def select_last() -> Project:
        return Table.select_last(ProjectsTable.table, Project)

    @staticmethod
    def update(project: Project) -> None:
        return Table.update(ProjectsTable.table, project)

    @staticmethod
    def insert(project: Project) -> None:
        return Table.insert(ProjectsTable.table, project)

    @staticmethod
    def delete(project: Project) -> None:
        return Table.delete(ProjectsTable.table, project)
