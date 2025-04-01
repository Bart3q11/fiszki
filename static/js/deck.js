document.addEventListener("DOMContentLoaded", () => {
    const deck = document.querySelectorAll('.deck')
    deck.forEach((e) => {
        e.addEventListener('click', () => {
            window.location.href = `/deck/${e.dataset.deckId}`
        });
    })

    const modal = document.getElementById('id01');
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});