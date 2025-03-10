from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegistrationForm, TitluriForm, TranzactiiTitluriForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, TitluriStat, TranzactiiTitluri
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

@app.route('/adauga_titluri', methods=['GET', 'POST'])
def adauga_titluri():
    form = TitluriForm()
    if form.validate_on_submit():
        titluStat = TitluriStat(type=form.type.data, ticker=form.ticker.data, currency=form.currency.data, 
                                broker=form.broker.data, period=form.period.data, enddate=form.enddate.data, 
                                interest=form.interest.data)
        db.session.add(titluStat)
        db.session.commit()
        flash('Felicitari, ai inregistrat titluri de stat!')
        return redirect(url_for('index'))
    return render_template('adauga_titluri.html', title='Adauga Titluri de stat', form=form)

def search_titlu_by_ticker(ticker):
    query = sa.select(TitluriStat).where(TitluriStat.ticker == ticker)
    titlu = db.session.scalars(query).first()
    return titlu

@app.route('/edit_titluri/<ticker>', methods=['GET', 'POST'])
def edit_titluri(ticker):
    emisiune = search_titlu_by_ticker(ticker)
    if emisiune:
        form = TitluriForm(formdata=request.form, obj=emisiune)
        if form.validate_on_submit():
            titluStat = TitluriStat(type=form.type.data, ticker=form.ticker.data, currency=form.currency.data, 
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
            flash('Felicitari, ai editat titluri de stat!')
            return redirect(url_for('index'))
        return render_template('edit_titluri.html', title='Editeaza Titluri de stat', form=form)
    else:
        return 'Error loading #{id}'.format(id=ticker)

@app.route('/titluri', methods=['GET'])
def titluri():
    # trigger exception
    #users = db.session.scalar(sa.select(User))
    titluri = TitluriStat.query.all()
    return render_template('titluri.html', titluri=titluri)

@app.route('/adauga_tranzactie_titluri', methods=['GET', 'POST'])
def adauga_tranzactie_titluri():
    form = TranzactiiTitluriForm()
    if form.validate_on_submit():
        query = sa.select(TitluriStat).where(TitluriStat.ticker == form.ticker.data.strip())
        titlu = db.session.scalars(query).first()
        #print("date: %s %s" % (form.date.data, type(form.date.data) ))
        #print("date: %s %s" % (datetime.fromisoformat(form.date.data), type(datetime.fromisoformat(form.date.data)) ))

        #if titlu is None:
        #   flash("Nu exista titlu inregistrat in DB cu ticker: %s" % (form.ticker.data.strip()))
        #   return render_template('adauga_tranzactie_titluri.html', title='Adauga Tranzactii Titluri de stat', form=TranzactiiTitluriForm())

        titluStat = TranzactiiTitluri(date=datetime.fromisoformat(form.date.data), operation=form.operation.data, value=form.valoare.data, titlu_stat=titlu)
        db.session.add(titluStat)
        db.session.commit()
        flash('Felicitari, ai inregistrat tranzactie titluri de stat!')
        return redirect(url_for('index'))
    return render_template('adauga_tranzactie_titluri.html', title='Adauga Tranzactii Titluri de stat', form=form)

@app.route('/tranzactii_titluri', methods=['GET'])
def tranzactii_titluri():
    # trigger exception
    #users = db.session.scalar(sa.select(User))
    tranzactii_titluri = TranzactiiTitluri.query.all()
    
    return render_template('tranzactii_titluri.html', tranzactii_titluri=tranzactii_titluri)
