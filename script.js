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

    // Use Dictionary API
    const apiUrl = `https://api.dictionaryapi.dev/api/v2/entries/en/${fetchWord}`;

    fetch(apiUrl)
    .then(response => {
        console.log('Fetching word details from:', apiUrl);  // Log the API URL
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('API response data:', data);  // Log the response data
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
