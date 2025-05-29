function speakText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}

async function getCo2Prediction(co2Data) {
    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ co2_levels: co2Data })
        });

        const result = await response.json();

        if (response.ok) {
            // Update the table cells with the prediction results
            document.getElementById("co2PpmValue").textContent = result[0].co2_ppm.toFixed(2);
            document.getElementById("co2PercentageValue").textContent = result[0].co2_percentage.toFixed(2) + "%";
            document.getElementById("co2LevelValue").textContent = result[0].co2_level;
            // Optionally, hide the output pre or clear it
            document.getElementById("output").textContent = "";
            speakText(`Carbon Dioxide Level is ${result[0].co2_level}. Carbon Dioxide in PPM level is ${result[0].co2_ppm.toFixed(2)}, which is ${result[0].co2_percentage.toFixed(2)} percent.`);
        } else {
            console.error("Error:", result.error);
            document.getElementById("output").textContent = result.error;
        }
    } catch (error) {
        console.error("Failed to fetch prediction:", error);
        document.getElementById("output").textContent = "Failed to fetch prediction.";
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
