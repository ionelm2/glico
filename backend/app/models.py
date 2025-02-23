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
    
class TitluriStat(db.Model):
    #__tablename__ = "titluri_Stat1"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(20))      # Fidelis/ Tezaur
    # index used to speed up DB queries
    ticker: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=True)
    currency: so.Mapped[str] = so.mapped_column(sa.String(20))  # EUR/ RON/ USD
    broker: so.Mapped[str] = so.mapped_column(sa.String(20))    # Trezorerie/ Tradeville/ XTB
    period: so.Mapped[int] = so.mapped_column()
    enddate: so.Mapped[datetime] = so.mapped_column()
    interest: so.Mapped[float] = so.mapped_column()             # Dobanda (e.g., 6.32)
    tranzactii: so.WriteOnlyMapped['TranzactiiTitluri'] = so.relationship(back_populates='titlu_stat')

    def __repr__(self):
        return '<Emisiune ticker={}, dobanda={}%>'.format(self.ticker, self.interest)

class TranzactiiTitluri(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime] = so.mapped_column()
    #ticker: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=True)
    operation: so.Mapped[str] = so.mapped_column(sa.String(20))  # EUR/ RON/ USD
    value: so.Mapped[str] = so.mapped_column(sa.String(20))    # Trezorerie/ Tradeville/ XTB
    titluriStat_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(TitluriStat.id), index=True)
    titlu_stat: so.Mapped[TitluriStat] = so.relationship(back_populates='tranzactii')
    
    def __repr__(self):
        return '<Tranzactie {}>'.format(self.ticker, self.value)
    
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))