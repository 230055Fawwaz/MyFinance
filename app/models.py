# Skema SQLite

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Enum('income', 'expense'), nullable=False)  # Fix 1: removed name='category_types'
    subcategories = db.relationship('SubCategory', backref='category', lazy=True)

class SubCategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    nama = db.Column(db.String(20), nullable=False)

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text)

    # Tambahkan 2 baris ini agar mudah diakses via Jinja2:
    account = db.relationship('Account', backref='transactions')
    subcategory = db.relationship('SubCategory', backref='transactions')

class Transfer(db.Model):
    __tablename__ = 'transfers'
    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    fee = db.Column(db.Numeric(10, 2), default=0.00)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text)

    # Fix 2: explicit foreign_keys to resolve ambiguity on self-referencing table
    from_account = db.relationship('Account', foreign_keys=[from_account_id])
    to_account = db.relationship('Account', foreign_keys=[to_account_id])