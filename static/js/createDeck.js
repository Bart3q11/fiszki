document.addEventListener("DOMContentLoaded", function () {
    const addCardBtn = document.querySelector('#add-card-btn');
    const cardsContainer = document.querySelector('#cards_container');
    let i = 0;

    function card() {
        i += 1;
        let addCard = document.createElement('div');
        addCard.className = "container my-4 p-4 bg-secondary text-white rounded js-added-card";
        addCard.id = `card-${i}`;
        addCard.innerHTML = `
            <div class="row g-3 align-items-center">
                <div class="col-12 col-md-5">
                    <input type="text" class="form-control focus-ring border" name="front" placeholder="Pojęcie" required style="--bs-focus-ring-color: var(--bs-warning-bg-subtle);">
                </div>
                <div class="col-12 col-md-5">
                    <input type="text" class="form-control focus-ring border" name="back" placeholder="Definicja" required style="--bs-focus-ring-color: var(--bs-warning-bg-subtle);">
                </div>
                <div class="col-12 col-md-2 text-center">
                    <button type="button" class="btn btn-danger remove-card" data-id="card-${i}">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px"
                            fill="#e3e3e3">
                            <path
                                d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z" />
                        </svg>
                    </button>
                </div>
            </div>
        `;

        cardsContainer.appendChild(addCard);
        updateDeleteButtons();
    }

    function deleteCard(event) {
        let cardId = event.currentTarget.getAttribute("data-id");
        let cardElement = document.getElementById(cardId);

        if (cardElement) {
            cardElement.remove();
        }

        updateDeleteButtons();
    }

    function updateDeleteButtons() {
        let removeButtons = document.querySelectorAll(".remove-card");

        if (removeButtons.length === 1) {
            removeButtons[0].disabled = true;
        } else {
            removeButtons.forEach(btn => btn.disabled = false);
        }

        removeButtons.forEach(btn => {
            btn.removeEventListener("click", deleteCard);
            btn.addEventListener("click", deleteCard);
        });
    }

    card();
    addCardBtn.addEventListener("click", card);
});
