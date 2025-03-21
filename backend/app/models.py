from datetime import datetime
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from app import db
from app import login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
class Bond(db.Model):
    #__tablename__ = "Bond_Stat1"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(20))      # Fidelis/ Tezaur
    # index used to speed up DB queries
    ticker: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=True)
    currency: so.Mapped[str] = so.mapped_column(sa.String(20))  # EUR/ RON/ USD
    broker: so.Mapped[str] = so.mapped_column(sa.String(20))    # Trezorerie/ Tradeville/ XTB
    period: so.Mapped[int] = so.mapped_column()
    enddate: so.Mapped[datetime] = so.mapped_column()
    interest: so.Mapped[float] = so.mapped_column()             # Dobanda (e.g., 6.32)
    transaction: so.WriteOnlyMapped['BondTransactions'] = so.relationship(back_populates='bond')

    def __repr__(self):
        return '<Bond ticker={}, interest={}%>'.format(self.ticker, self.interest)

class BondTransactions(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime] = so.mapped_column()
    #ticker: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=True)
    operation: so.Mapped[str] = so.mapped_column(sa.String(20))  # EUR/ RON/ USD
    value: so.Mapped[str] = so.mapped_column(sa.String(20))    # Trezorerie/ Tradeville/ XTB
    BondID: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Bond.id), index=True)
    bond: so.Mapped[Bond] = so.relationship(back_populates='transaction')
    
    def __repr__(self):
        return '<Transaction {}>'.format(self.ticker, self.value)
    
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))