from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy


from database import db, init_db, Decks, Users, Cards

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flashcards'  # Poprawiony URL
app.secret_key = 'ZAQ!2wsx'

init_db(app)

# Aplikacja
@app.route('/')
def auth():
    if session.get('id'):
        return redirect(url_for('dashboard'))
    return render_template('auth.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password or not first_name or not last_name:
            flash('Błąd dodania do bazy danych. Spróbuj ponownie')
            return redirect(url_for('auth'))  
        
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Adres email jest już zajęty')
            return redirect(url_for('form'))
        
        user = Users(
            first_name = first_name,
            last_name = last_name,
            email = email,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash('Zarejestorano pomyślnie')
        return redirect(url_for("auth")) 
    flash("Coś poszło nie tak. Spróbuj ponownie")
    return redirect(url_for("auth"))

@app.route('/account')
def account():
    if session.get('id'):
        return render_template('account.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Coś poszło nie tak. Spróbuj ponownie')
            return redirect(url_for('auth'))

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Nie prawidłowe hasło lub email')
            return redirect(url_for('auth'))
    return redirect(url_for('auth'))

@app.route('/dashboard')
def dashboard():
    if session.get('id'):
        decks = Decks.query.filter_by(id_user=session['id']).all()
        deck_count = Decks.query.filter_by(id_user=session['id']).count()
        user = Users.query.filter_by(id=session['id']).first()
        decks_data = []
        for deck in decks:
            card_count = Cards.query.filter_by(id_deck=deck.id).count()
            decks_data.append({
                'id': deck.id,
                'name': deck.name,
                'description': deck.description,
                'card_count': card_count
            })
        return render_template('dashboard.html', decks=decks_data, deck_count=deck_count, user=user)
    else:
        return redirect(url_for('auth'))

@app.route('/createDeck', methods=['POST'])
def createDeck():
    if request.method == 'POST' and session.get('id'):
        return render_template('createDeck.html')
    else:
        return redirect(url_for('dashboardd'))

@app.route('/addDeck', methods=["POST"])
def addDeck():
    if request.method == "POST" and session.get('id'):
        name = request.form.get('name')
        description = request.form.get('description')
        deck = Decks (
            id_user=session.get('id'),
            name=name,
            description=description
        )
        db.session.add(deck)
        db.session.commit()

        front = request.form.getlist('front')
        back = request.form.getlist('back')

        for term, definition in zip(front, back):
            card = Cards(
                id_deck=deck.id, 
                front=term,
                back=definition
            )
            db.session.add(card)

        db.session.commit()
        
        return redirect(url_for('dashboard'))

@app.route('/deck/<deck_id>')
def deck(deck_id):
    if session.get('id'):
        cards = Cards.query.filter_by(id_deck=deck_id).all()
        return render_template('deck.html', deck_id=deck_id, cards=cards)
    flash('')

if __name__ == '__main__':
    app.run(debug=True)
