function toggleCard(card) {
  card.classList.toggle("active");

  // Untuk menutup kartu lain jika yang satu diklik
  var cards = document.querySelectorAll('.card');
  cards.forEach(function (c) {
    if (c !== card && c.classList.contains('active')) {
      c.classList.remove('active');
    }
  });
}
