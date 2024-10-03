/* JavaScript para aumentar e diminuir o tamanho da fonte*/
const increaseFontBtn = document.getElementById('increaseFont');
const decreaseFontBtn = document.getElementById('decreaseFont');
const body = document.querySelector('body');

let fontSize = 16; // Tamanho inicial da fonte em pixels

increaseFontBtn.addEventListener('click', () => {
    if (fontSize < 22) { // Limite máximo de 22px
        fontSize += 2;
        body.style.fontSize = fontSize + 'px';
    }
});

decreaseFontBtn.addEventListener('click', () => {
    if (fontSize > 16) { // Limite mínimo de 16px
        fontSize -= 2;
        body.style.fontSize = fontSize + 'px';
    }
});

/*Dark Mode*/
document.getElementById('invertColors').addEventListener('click', function() {
    document.body.classList.toggle('inverted-colors');
  });