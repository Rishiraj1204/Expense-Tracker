from datetime import datetime

from . import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False, default="Expense")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="categories")
    expenses = db.relationship("Expense", back_populates="category", cascade="all, delete-orphan")
    budgets = db.relationship("Budget", back_populates="category", cascade="all, delete-orphan")
