document.addEventListener("DOMContentLoaded", function () {
    const addCardBtn = document.getElementById("add-card-btn");
    const cardsContainer = document.getElementById("cards_container");

    function createCard() {
        const newCard = document.createElement("div");
        newCard.className = "card-content";
        newCard.innerHTML = `
            <div class="container my-4 p-4 bg-secondary text-white rounded js-added-card">
                <div class="row g-3 align-items-center">
                    <div class="col-12 col-md-5">
                        <input type="text" class="form-control focus-ring border" name="front" placeholder="Pojęcie" required
                            style="--bs-focus-ring-color: var(--bs-warning-bg-subtle);">
                    </div>
                    <div class="col-12 col-md-5">
                        <input type="text" class="form-control focus-ring border" name="back" placeholder="Definicja" required
                            style="--bs-focus-ring-color: var(--bs-warning-bg-subtle);">
                    </div>
                    <div class="col-12 col-md-2 text-center">
                        <button type="button" class="btn btn-danger remove-card">
                            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3">
                                <path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
        cardsContainer.appendChild(newCard);
        updateRemoveButtonsState();
    }

    function updateRemoveButtonsState() {
        const removeButtons = cardsContainer.querySelectorAll(".remove-card");
        removeButtons.forEach(button => {
            button.disabled = cardsContainer.children.length === 1;
        });
    }

    if (addCardBtn && cardsContainer) {
        // Dodanie pierwszego segmentu karty przy ładowaniu strony
        if (cardsContainer.children.length === 0) {
            createCard();
        }

        // Obsługa przycisku dodawania nowych kart
        addCardBtn.addEventListener("click", createCard);

        // Obsługa usuwania kart
        cardsContainer.addEventListener("click", function (event) {
            if (event.target.closest(".remove-card")) {
                const cardElement = event.target.closest(".card-content");
                if (cardElement) {
                    cardElement.remove();
                    updateRemoveButtonsState();
                }
            }
        });

        // Aktualizacja stanu przycisków usuwania przy ładowaniu strony
        updateRemoveButtonsState();
    }
});
