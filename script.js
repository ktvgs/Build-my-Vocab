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

function fetchWordDetails() {
    const fetchWord = document.getElementById('fetchWord').value;

    const apiUrl = `https://api.dictionaryapi.dev/api/v2/entries/en/${fetchWord}`;

    fetch(apiUrl)
    .then(response => {
        console.log('Fetching word details from:', apiUrl);  
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('API response data:', data);  
        if (data.title === "No Definitions Found") {
            throw new Error("No definitions found for this word.");
        }

        const meanings = data[0].meanings.map(meaning => meaning.definitions[0].definition).join('; ');
        const sentence = data[0].meanings[0].definitions[0].example || 'No example available';

        document.getElementById('fetchedMeaning').textContent = meanings;
        document.getElementById('fetchedSentence').textContent = sentence;
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error fetching word details: ' + error.message);
    });
}

function testYourKnowledge() {
    fetch('/get_random_word')
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            const userMeaning = prompt(`What is the meaning of the word "${data.word}"?`);
            const correctMeanings = data.meanings;

            if (correctMeanings.includes(userMeaning)) {
                alert('Correct!');
            } else {
                alert(`Incorrect! The correct meanings are: ${correctMeanings.join(', ')}`);
            }
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error fetching random word: ' + error.message);
    });
}
