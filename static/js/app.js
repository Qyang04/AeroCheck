// fetch('http://127.0.0.1:5000/api/status')
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('app').innerText = data.message;
//     })
//     .catch(error => console.error('Error fetching data:', error));
fetch('/api/status')
    .then(response => response.json())
    .then(data => {
        document.getElementById('app').innerText = data.message;
    })
    .catch(error => console.error('Error fetching data:', error));
    