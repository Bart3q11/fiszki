document.addEventListener("DOMContentLoaded", function () {
    const login = document.querySelector('#login');
    const login_btn = document.querySelector('#login-btn');
    const signup = document.querySelector('#signup');
    const signup_btn = document.querySelector('#signup-btn');

    signup.style.display = 'none';
    login.style.display = 'block';

    login_btn.addEventListener("click", function () {
        login.style.display = "block";
        signup.style.display = "none";
    });

    signup_btn.addEventListener("click", function () {
        login.style.display = "none";
        signup.style.display = "block";
    });

    const passwordInput = document.getElementById("signup-password"); // Pole "Hasło"
    const rePasswordInput = document.getElementById("re-password"); // Pole "Powtórz hasło"

    signup.addEventListener("submit", function (event) {
        // Sprawdzenie, czy hasła są zgodne
        if (passwordInput.value !== rePasswordInput.value) {
            event.preventDefault(); // Zatrzymanie wysyłania formularza
            alert("Hasła nie są zgodne!"); // Wyświetlenie komunikatu błędu
        }
    });
});




