async function updateSensors() {
    const response = await fetch("http://127.0.0.1:8000/sensors");
    const data = await response.json();

    document.getElementById("temperature").textContent =
        `${data.temperature.toFixed(1)} °C`;

    document.getElementById("voltage").textContent =
        `${data.voltage.toFixed(2)} V`;

    document.getElementById("current").textContent =
        `${data.current.toFixed(2)} A`;
}

updateSensors();

setInterval(updateSensors, 2000);