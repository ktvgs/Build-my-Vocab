// script.js
document.getElementById('vocabForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const word = document.getElementById('word').value;
    const meaning = document.getElementById('meaning').value;
    const sentence = document.getElementById('sentence').value;

    const data = { word, meaning, sentence };

    fetch('/add_word', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Word added successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
