function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}

async function getCo2Prediction(co2Data) {
    try {
        const response = await fetch("http://127.0.0.1:10000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ co2_levels: co2Data })
        });

        const result = await response.json();

        if (response.ok) {
            const co2Ppm = result[0].co2_ppm.toFixed(2);
            const co2Percentage = result[0].co2_percentage.toFixed(2);
            const co2Level = result[0].co2_level;

            document.getElementById("output").textContent = `Carbon Dioxide Level PPM: ${co2Ppm}\nCarbon Dioxide %: ${co2Percentage}\nCarbon Dioxide Level: ${co2Level}`;
            speakText(`Carbon Dioxide Level is ${co2Level}.and  Carbon Dioxide in  PPM level is ${co2Ppm}, which is ${co2Percentage} percent.`);
        } else {
            console.error("Error:", result.error);
        }
    } catch (error) {
        console.error("Failed to fetch prediction:", error);
    }
}

document.getElementById('co2Form').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    const inputField = document.getElementById('co2Input');
    const co2Levels = inputField.value.split(',').map(Number);

    if (co2Levels.some(isNaN)) {
        alert("Please enter valid numeric values separated by commas.");
        return;
    }

    await getCo2Prediction([co2Levels]);
    document.getElementById('result').classList.remove('hidden');
});

// New function to generate random CO2 levels
function generateRandomCo2Levels() {
    const randomLevels = Array.from({ length: 10 }, () => Math.floor(Math.random() * 1500) + 300); // Generates 10 random levels between 300 and 1500 ppm
    document.getElementById('co2Input').value = randomLevels.join(','); // Set the random levels to the input field

    // Automatically trigger form submission to get prediction
    document.getElementById('co2Form').dispatchEvent(new Event('submit'));
}

const backgrounds = [
    'img/background1.jpg',
    'img/background2.jpg',
    'img/background3.jpg',
    'img/background4.jpg'
];

let currentIndex = 0;

function changeBackground() {
    document.body.style.backgroundImage = `url('${backgrounds[currentIndex]}')`;
    currentIndex = (currentIndex + 1) % backgrounds.length;
}

setInterval(changeBackground, 10000);
changeBackground();

// Event listener for the "Auto-generate CO2 Levels" button
document.getElementById('generateBtn').addEventListener('click', generateRandomCo2Levels);
