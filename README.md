# 📚 FlashCards App – Nauka Fiszek Online

Prosta aplikacja webowa do nauki fiszek – prosta, szybka i bez zbędnych bajerów. Umożliwia tworzenie własnych zestawów, przeglądanie kart i tryb nauki oparty na znajomości pojęć.

🔗 **Zobacz demo:** [Kliknij tutaj, żeby przetestować](https://demo-nfi6.onrender.com/)
Poniżej znajduje się tekst który możemy zaimportować jako json :) 

---

## ✨ Funkcje

- ✅ Rejestracja i logowanie użytkowników
- ✅ Tworzenie własnych zestawów fiszek (z opisem)
- ✅ Dodawanie i usuwanie kart
- ✅ Tryb przeglądania oraz tryb nauki (tylko nieznane)
- ✅ System zapamiętywania znanych/nieznanych fiszek
- ✅ Responsywny design (działa na telefonie!)

---

## 🛠️ Technologie

- **Backend**: Python + Flask + SQLAlchemy  
- **Frontend**: HTML + CSS + Bootstrap + JS  
- **Baza danych**: SQLite (do testów) / MySQL (do produkcji)  
- **Autoryzacja**: Sesje i tokeny  

---

## 🚀 Uruchomienie lokalnie

```bash
git clone https://github.com/twoj-user/flashcards-app.git
cd flashcards-app
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

```json
{
    "deck_name": "Angielski – podstawowe pojęcia",
    "deck_description": "25 najczęściej używanych angielskich słów i zwrotów",
    "cards": [
        {
            "front": "hello",
            "back": "cześć"
        },
        {
            "front": "goodbye",
            "back": "do widzenia"
        },
        {
            "front": "please",
            "back": "proszę"
        },
        {
            "front": "thank you",
            "back": "dziękuję"
        },
        {
            "front": "yes",
            "back": "tak"
        },
        {
            "front": "no",
            "back": "nie"
        },
        {
            "front": "sorry",
            "back": "przepraszam"
        },
        {
            "front": "excuse me",
            "back": "przepraszam (zaczepienie)"
        },
        {
            "front": "how are you?",
            "back": "jak się masz?"
        },
        {
            "front": "I'm fine",
            "back": "wszystko w porządku"
        },
        {
            "front": "what's your name?",
            "back": "jak masz na imię?"
        },
        {
            "front": "my name is...",
            "back": "mam na imię..."
        },
        {
            "front": "where is...",
            "back": "gdzie jest..."
        },
        {
            "front": "how much?",
            "back": "ile to kosztuje?"
        },
        {
            "front": "I don't understand",
            "back": "nie rozumiem"
        },
        {
            "front": "can you help me?",
            "back": "czy możesz mi pomóc?"
        },
        {
            "front": "I need...",
            "back": "potrzebuję..."
        },
        {
            "front": "I like it",
            "back": "podoba mi się to"
        },
        {
            "front": "I don't know",
            "back": "nie wiem"
        },
        {
            "front": "maybe",
            "back": "może"
        },
        {
            "front": "always",
            "back": "zawsze"
        },
        {
            "front": "never",
            "back": "nigdy"
        },
        {
            "front": "sometimes",
            "back": "czasami"
        },
        {
            "front": "today",
            "back": "dzisiaj"
        },
        {
            "front": "tomorrow",
            "back": "jutro"
        }
    ]
}
