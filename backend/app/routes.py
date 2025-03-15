from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegistrationForm, BondForm, BondTransactionForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Bond, BondTransactions
from flask import request
from urllib.parse import urlsplit
from datetime import datetime

@app.route('/')
@app.route('/index')
#@login_required
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/unregister', methods=['GET'])
def unregister():
    if current_user.is_authenticated:
        flash('Congratulations, you are now a unregistered user!')
        user = db.session.scalar(sa.select(User).where(
            User.id == current_user.get_id()))
        if user is not None:
            User.query.filter_by(id=user.id).delete()
            db.session.commit()
            logout_user()
    return redirect(url_for('index'))

@app.route('/users', methods=['GET'])
def users():
    # trigger exception
    #users = db.session.scalar(sa.select(User))
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('user.html', user=user)

@app.route('/bond/create', methods=['GET', 'POST'])
def add_bond():
    form = BondForm()
    if form.validate_on_submit():
        bond = Bond(type=form.type.data, ticker=form.ticker.data, currency=form.currency.data, 
                                broker=form.broker.data, period=form.period.data, enddate=form.enddate.data, 
                                interest=form.interest.data)
        db.session.add(bond)
        db.session.commit()
        flash('Felicitari, ai inregistrat Titlu de stat!')
        return redirect(url_for('index'))
    return render_template('add_bond.html', title='Adauga Bond de stat', form=form)

def search_titlu_by_ticker(ticker):
    query = sa.select(Bond).where(Bond.ticker == ticker)
    titlu = db.session.scalars(query).first()
    return titlu

@app.route('/bond/<ticker>/edit', methods=['GET', 'POST'])
def edit_bond(ticker):
    emisiune = search_titlu_by_ticker(ticker)
    if emisiune:
        form = BondForm(formdata=request.form, obj=emisiune)
        if form.validate_on_submit():
            titluStat = Bond(type=form.type.data, ticker=form.ticker.data, currency=form.currency.data, 
                                    broker=form.broker.data, period=form.period.data, enddate=form.enddate.data, 
                                    interest=form.interest.data)
            
            emisiune.type = titluStat.type
            emisiune.ticker = titluStat.ticker
            emisiune.currency = titluStat.currency
            emisiune.broker = titluStat.broker
            emisiune.period = titluStat.period
            emisiune.enddate = titluStat.enddate
            emisiune.interest = titluStat.interest

            db.session.commit()
            flash('Felicitari, ai editat Bond de stat!')
            return redirect(url_for('index'))
        return render_template('edit_bond.html', title='Editeaza Bond de stat', form=form)
    else:
        return 'Error loading #{id}'.format(id=ticker)

@app.route('/bond', methods=['GET'])
def bond():
    # trigger exception
    #users = db.session.scalar(sa.select(User))
    bonds = Bond.query.all()
    return render_template('bonds.html', Bond=bonds)

@app.route('/add_transaction_bond', methods=['GET', 'POST'])
def add_transaction_bond():
    form = BondTransactionForm()
    if form.validate_on_submit():
        query = sa.select(Bond).where(Bond.ticker == form.ticker.data.strip())
        titlu = db.session.scalars(query).first()
        #print("date: %s %s" % (form.date.data, type(form.date.data) ))
        #print("date: %s %s" % (datetime.fromisoformat(form.date.data), type(datetime.fromisoformat(form.date.data)) ))

        #if titlu is None:
        #   flash("Nu exista titlu inregistrat in DB cu ticker: %s" % (form.ticker.data.strip()))
        #   return render_template('add_transaction_bond.html', title='Adauga transaction Bond de stat', form=BondTransactionForm())

        titluStat = BondTransactions(date=datetime.fromisoformat(form.date.data), operation=form.operation.data, value=form.amount.data, bond=titlu)
        db.session.add(titluStat)
        db.session.commit()
        flash('Felicitari, ai inregistrat tranzactie Bond de stat!')
        return redirect(url_for('index'))
    return render_template('add_transaction_bond.html', title='Adauga transaction Bond de stat', form=form)

@app.route('/transaction_bond', methods=['GET'])
def transaction_Bond():
    # trigger exception
    #users = db.session.scalar(sa.select(User))
    transaction_Bond = BondTransactions.query.all()
    
    return render_template('transaction_bond.html', transaction_Bond=transaction_Bond)
