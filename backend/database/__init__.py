from .config import *
from .database import *
from .donation import *
from .project import *
from .user import *


def create_tables():
    if Config.DROP_DB:
        DonationsTable.create_table()
        ProjectsTable.create_table()
        UsersTable.create_table()
