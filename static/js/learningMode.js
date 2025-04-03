document.addEventListener("DOMContentLoaded", async function () {
    const card = document.getElementById("card");
    const cardFront = card.querySelector(".card-front");
    const cardBack = card.querySelector(".card-back");
    const knowBtn = document.getElementById("know-btn");
    const dontKnowBtn = document.getElementById("dont-know-btn");
    const resetKnownBtn = document.getElementById("reset-known-btn");
    const knownCountSpan = document.getElementById("known-count");

    let cards = [];
    let currentIndex = 0;
    let knownCount = parseInt(knownCountSpan.textContent);

    const deckId = card.dataset.deckId;

    async function fetchCards() {
        try {
            const response = await fetch(`/api/deck/${deckId}/cards`);
            if (!response.ok) {
                throw new Error('Błąd podczas pobierania danych z API');
            }
            cards = await response.json();
            updateKnownCount();
        } catch (error) {
            console.error('Błąd:', error);
            cards = [];
        }
    }

    function updateKnownCount() {
        knownCountSpan.textContent = knownCount;
    }

    function showCard(index) {
        if (index < cards.length) {
            cardFront.textContent = cards[index].front;
            cardBack.textContent = cards[index].back;
            knowBtn.dataset.cardId = cards[index].id;
        } else {
            cardFront.textContent = "Koniec kart!";
            cardBack.textContent = "";
            knowBtn.disabled = true;
            dontKnowBtn.disabled = true;
            location.reload()
        }
    }

    async function markCardAsKnown(cardId, knownStatus) {
        try {
            const response = await fetch(`/api/card/${cardId}/update`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ known: knownStatus })
            });

            if (!response.ok) {
                throw new Error("Błąd podczas aktualizacji statusu karty");
            }

            // const result = await response.json();
            // console.log("Odpowiedź serwera:", result);

            if (knownStatus) {
                knownCount++;
            }
            updateKnownCount();
        } catch (error) {
            console.error("Błąd:", error);
        }
    }

    async function resetAllCardsToUnknown() {
        try {
            const response = await fetch(`/api/deck/${deckId}/reset`, {
                method: "POST"
            });

            if (!response.ok) {
                throw new Error("Błąd podczas resetowania kart");
            }

            cards.forEach(card => card.known = false);
            knownCount = 0;
            updateKnownCount();
            location.reload()
        } catch (error) {
            console.error("Błąd:", error);
        }
    }

    async function handleCardFlipAndNext() {
        card.classList.remove("flipped");
        await new Promise(resolve => setTimeout(resolve, 550));
        currentIndex++;
        showCard(currentIndex);
    }

    card.addEventListener("click", function () {
        card.classList.toggle("flipped");
    });

    knowBtn.addEventListener("click", () => {
        const cardId = knowBtn.dataset.cardId;
        markCardAsKnown(cardId, true);
        handleCardFlipAndNext();
    });

    dontKnowBtn.addEventListener("click", () => {
        const cardId = knowBtn.dataset.cardId;
        markCardAsKnown(cardId, false);
        handleCardFlipAndNext();
    });

    resetKnownBtn.addEventListener("click", async () => {
        await resetAllCardsToUnknown();
        currentIndex = 0;
        showCard(currentIndex);
    });

    await fetchCards();
    showCard(currentIndex);
});
