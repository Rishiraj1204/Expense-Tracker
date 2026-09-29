from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from .budget import Budget
from .category import Category
from .expense import Expense
from .income import Income
from .notification import Notification
from .user import User

__all__ = [
    "db",
    "User",
    "Category",
    "Expense",
    "Income",
    "Budget",
    "Notification",
]
