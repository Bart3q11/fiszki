# 📚 FlashCards App – Nauka Fiszek Online

Prosta aplikacja webowa do nauki fiszek – prosta, szybka i bez zbędnych bajerów. Umożliwia tworzenie własnych zestawów, przeglądanie kart i tryb nauki oparty na znajomości pojęć.

🔗 **Zobacz demo:** [Kliknij tutaj, żeby przetestować](https://demo-nfi6.onrender.com/)

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
