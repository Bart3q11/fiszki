from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db, init_db, Decks, Users, Cards
import json

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
            flash('Błąd dodania do bazy danych. Uzupełnij wszystkie pola i spróbuj ponownie.', 'danger')
            return redirect(url_for('auth'))  
        
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Adres email jest już zajęty. Wybierz inny adres email.', 'warning')
            return redirect(url_for('form'))
        
        user = Users(
            first_name = first_name,
            last_name = last_name,
            email = email,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash('Zarejestrowano pomyślnie. Możesz się teraz zalogować.', 'success')
        return redirect(url_for("auth")) 
    flash("Wystąpił błąd. Spróbuj ponownie później.", 'danger')
    return redirect(url_for("auth"))

@app.route('/account', methods=['GET', 'POST'])
def account():
    if not session.get('id'):
        flash('Musisz być zalogowany, aby uzyskać dostęp do tej strony.', 'warning')
        return redirect(url_for('auth'))

    user = Users.query.filter_by(id=session['id']).first()

    if request.method == 'POST':
        # Aktualizacja danych użytkownika
        first_name = request.form.get('first-name', '').strip()
        last_name = request.form.get('last-name', '').strip()
        email = request.form.get('email', '').strip()

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email and email != user.email:
            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                flash('Podany adres e-mail jest już zajęty. Wybierz inny.', 'danger')
                return redirect(url_for('account'))
            user.email = email

        # Zmiana hasła
        current_password = request.form.get('current-password', '').strip()
        new_password = request.form.get('new-password', '').strip()
        confirm_password = request.form.get('confirm-password', '').strip()

        if current_password or new_password or confirm_password:
            if not user.check_password(current_password):
                flash('Obecne hasło jest nieprawidłowe.', 'danger')
                return redirect(url_for('account'))

            if new_password != confirm_password:
                flash('Nowe hasło i potwierdzenie hasła muszą być takie same.', 'danger')
                return redirect(url_for('account'))

            if len(new_password) < 8 or not any(char.isdigit() for char in new_password) or not any(char.isupper() for char in new_password) or not any(char.islower() for char in new_password):
                flash('Nowe hasło musi mieć co najmniej 8 znaków, zawierać cyfrę, małą i dużą literę.', 'danger')
                return redirect(url_for('account'))

            user.set_password(new_password)

        db.session.commit()
        flash('Dane zostały pomyślnie zaktualizowane.', 'success')
        return redirect(url_for('account'))

    return render_template('account.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Wystąpił błąd. Spróbuj ponownie później.', 'danger')
            return redirect(url_for('auth'))

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Nieprawidłowe dane logowania. Sprawdź email i hasło.', 'danger')
            return redirect(url_for('auth'))
    return redirect(url_for('auth'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    response = redirect(url_for('auth'))
    response.set_cookie('session', '', expires=0)
    flash("Wylogowano pomyślnie. Do zobaczenia!", 'success')
    return response

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
        flash('Musisz być zalogowany, aby uzyskać dostęp do tej strony.', 'warning')
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
        deck = Decks(
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
        
        flash('Zestaw został pomyślnie dodany.', 'success')
        return redirect(url_for('dashboard'))

    flash('Nie udało się dodać zestawu. Spróbuj ponownie.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/deck/<deck_id>')
def deck(deck_id):
    if session.get('id'):
        deck = Decks.query.filter_by(id=deck_id, id_user=session['id']).first()
        if not deck:
            flash('Nie znaleziono zestawu lub brak uprawnień do jego wyświetlenia.', 'danger')
            return redirect(url_for("dashboard"))
        
        cards = Cards.query.filter_by(id_deck=deck_id).all()
        return render_template('deck.html', deck_id=deck_id, cards=cards)
    
    flash('Musisz być zalogowany, aby uzyskać dostęp do tej strony.', 'warning')
    return redirect(url_for("dashboard"))

@app.route('/deleteDeck', methods=["POST"])
def deleteDeck():
    deck_id = request.form.get('deck_id')
    if deck_id:
        deck = Decks.query.get(deck_id)
        if deck:
            db.session.delete(deck)
            db.session.commit()
            flash('Zestaw został usunięty pomyślnie.', 'success')
        else:
            flash('Nie znaleziono zestawu.', 'danger')
    else:
        flash('Nie podano ID zestawu. Spróbuj ponownie.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/editdeck/<deck_id>', methods=["POST"])
def editDeck(deck_id):
    deck = Decks.query.get(deck_id)
    if deck:
        cards = Cards.query.filter_by(id_deck=deck_id).all()
        return render_template('editDeck.html', deck=deck, cards=cards, deck_id=deck_id)
    else:
        flash('Nie znaleziono zestawu do edycji.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/updateDeck/<int:deck_id>', methods=['POST'])
def updateDeck(deck_id):
    if not session.get('id'):
        flash('Musisz być zalogowany, aby edytować zestawy.', 'warning')
        return redirect(url_for('dashboard'))

    # Pobranie zestawu użytkownika
    deck = Decks.query.filter_by(id=deck_id, id_user=session['id']).first()
    if not deck:
        flash('Nie znaleziono zestawu lub brak uprawnień do edycji.', 'danger')
        return redirect(url_for('dashboard'))

    # Aktualizacja nazwy i opisu zestawu
    deck.name = request.form.get('name', '').strip()
    deck.description = request.form.get('description', '').strip()

    if not deck.name or not deck.description:
        flash('Nazwa i opis zestawu nie mogą być puste. Uzupełnij dane i spróbuj ponownie.', 'warning')
        return redirect(url_for('dashboard'))

    # Pobranie istniejących kart
    existing_cards = {card.id: card for card in Cards.query.filter_by(id_deck=deck_id).all()}

    # Pobranie danych z formularza
    fronts = request.form.getlist('front')
    backs = request.form.getlist('back')

    for i, (front, back) in enumerate(zip(fronts, backs)):
        front, back = front.strip(), back.strip()
        if not front or not back:
            continue  # Ignorowanie pustych fiszek
        new_card = Cards(id_deck=deck_id, front=front, back=back)
        db.session.add(new_card)

    # Usunięcie kart, które użytkownik skasował w formularzu
    for card in existing_cards.values():
        db.session.delete(card)

    db.session.commit()

    flash('Zestaw został pomyślnie zaktualizowany.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/learningMode/<int:deck_id>', methods=["POST"])
def learningMode(deck_id):
    if session.get('id'):
        cart_count = Cards.query.filter_by(id_deck=deck_id).count()
        known_card = Cards.query.filter_by(id_deck=deck_id, known=1).count()
        return render_template('learningMode.html', deck_id=deck_id, cart_count=cart_count,known_card=known_card)
    else:
        flash('Musisz być zalogowany, aby korzystać z trybu nauki.', 'warning')
        return redirect(url_for('auth'))

@app.route('/api/deck/<int:deck_id>/cards', methods=['GET'])
def get_cards(deck_id):
    if not session.get('id'):
        return jsonify({"error": "Unauthorized"}), 401

    cards = Cards.query.filter_by(id_deck=deck_id, known=0).all()
    if not cards:
        return jsonify({"error": "Deck not found or no cards available"}), 404

    # Serializacja danych kart
    cards_data = [{"id": card.id, "front": card.front, "back": card.back, "known": card.known} for card in cards]
    return jsonify(cards_data), 200


@app.route('/api/deck/<int:deck_id>/reset', methods=['POST'])
def reset_deck_cards(deck_id):
    if not session.get('id'):
        return jsonify({"error": "Unauthorized"}), 401

    cards = Cards.query.filter_by(id_deck=deck_id).all()
    if not cards:
        return jsonify({"error": "Deck not found or no cards available"}), 404

    try:
        for card in cards:
            card.known = False
        db.session.commit()
        return jsonify({"message": "All cards reset to unknown"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to reset cards", "details": str(e)}), 500

@app.route('/api/card/<int:card_id>/update', methods=['POST'])
def update_card_status(card_id):
    if not session.get('id'):
        return jsonify({"error": "Unauthorized"}), 401

    card = Cards.query.get(card_id)
    if not card:
        return jsonify({"error": "Card not found"}), 404

    try:
        data = request.get_json()
        known_status = data.get("known", False)
        card.known = known_status
        db.session.commit()
        return jsonify({"message": "Card status updated successfully", "card_id": card_id, "known": card.known}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update card status", "details": str(e)}), 500

@app.route('/exportDeck/<int:deck_id>', methods=['GET'])
def exportDeck(deck_id):
    if not session.get('id'):
        flash('Musisz być zalogowany, aby eksportować zestawy.', 'warning')
        return redirect(url_for('auth'))

    deck = Decks.query.filter_by(id=deck_id, id_user=session['id']).first()
    if not deck:
        flash('Nie znaleziono zestawu lub brak uprawnień.', 'danger')
        return redirect(url_for('dashboard'))

    cards = Cards.query.filter_by(id_deck=deck_id).all()
    deck_data = {
        "deck_name": deck.name,
        "deck_description": deck.description,
        "cards": [{"front": card.front, "back": card.back} for card in cards]
    }

    # Serializacja JSON z polskimi znakami
    response = app.response_class(
        response=json.dumps(deck_data, ensure_ascii=False),  # ensure_ascii=False zachowuje polskie znaki
        status=200,
        mimetype='application/json'
    )
    response.headers['Content-Disposition'] = f'attachment; filename={deck.name}.json'
    return response

@app.route('/importDeck', methods=['POST'])
def importDeck():
    if not session.get('id'):
        flash('Musisz być zalogowany, aby importować zestawy.', 'warning')
        return redirect(url_for('auth'))

    file = request.files.get('file')
    if not file:
        flash('Nie wybrano pliku do importu.', 'danger')
        return redirect(url_for('dashboard'))

    try:
        data = json.load(file)
        name = data.get('deck_name', 'Nowy zestaw')
        description = data.get('deck_description', '')
        cards = data.get('cards', [])

        deck = Decks(
            id_user=session.get('id'),
            name=name,
            description=description
        )
        db.session.add(deck)
        db.session.commit()

        for card in cards:
            new_card = Cards(
                id_deck=deck.id,
                front=card.get('front', ''),
                back=card.get('back', '')
            )
            db.session.add(new_card)

        db.session.commit()
        flash('Zestaw został pomyślnie zaimportowany.', 'success')
    except Exception as e:
        flash(f'Wystąpił błąd podczas importu: {str(e)}', 'danger')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)