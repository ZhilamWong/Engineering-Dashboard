function updateSensors() {
    const temperature = (20 + Math.random() * 40).toFixed(1);
    const voltage = (11.5 + Math.random() * 1.5).toFixed(2);
    const current = (1 + Math.random() * 4).toFixed(2);

    document.getElementById("temperature").textContent =
        `${temperature} °C`;

    document.getElementById("voltage").textContent =
        `${voltage} V`;

    document.getElementById("current").textContent =
        `${current} A`;
}

updateSensors();

setInterval(updateSensors, 2000);