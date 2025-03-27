document.addEventListener("DOMContentLoaded", () => {
    const deck = document.querySelectorAll('.deck')
    deck.forEach((e) => {
        e.addEventListener('click', () => {
            window.location.href = `/deck/${e.dataset.deckId}`
        });
    })
})