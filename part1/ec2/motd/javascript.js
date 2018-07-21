var fortunes = [
    'Good things come to those who wait.',
    'Patience is a virtue.',
    'The early bird gets the worm.',
    'A wise man once said, everything in its own time and place.',
    'Fortune cookies rarely share fortunes.'
]

function newQuote() {
    var randomNumber = Math.floor(Math.random() * (quotes.length));
    document.getElementById('quoteDisplay').innerHTML = quotes[randomNumber];
}