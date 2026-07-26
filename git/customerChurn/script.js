const button = document.getElementById("button")
const URL = 'http://127.0.0.1:5000'; 
let data = [200, 1, 1, 50, 4, 0.7000, 1, 0, 1, 0.5000, 1, 85.2136]



button.addEventListener('click', async() => {
        let prediction; 
        const response = await fetch(URL, {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => prediction=data)
        .then(data => console.log(prediction.prediction))
})
