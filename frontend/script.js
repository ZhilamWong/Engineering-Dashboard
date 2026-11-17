let temperatureChart;

async function updateTemperature() {
    const response = await fetch("http://127.0.0.1:8000/sensors");

    if (!response.ok) {
        throw new Error(`Temperature request failed: ${response.status}`);
    }

    const data = await response.json();

    document.getElementById("temperature").textContent =
        `${data.temperature.toFixed(1)} °C`;
}

async function updateTemperatureHistory() {
    const response = await fetch(
        "http://127.0.0.1:8000/sensors/history"
    );

    if (!response.ok) {
        throw new Error(`Temperature history request failed: ${response.status}`);
    }

    const readings = await response.json();

    if (readings.length === 0) {
        return;
    }

    const labels = readings.map(reading =>
        new Date(reading.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        })
    );
    const values = readings.map(reading => reading.temperature);

    if (temperatureChart) {
        temperatureChart.data.labels = labels;
        temperatureChart.data.datasets[0].data = values;
        temperatureChart.update();
    } else {
        temperatureChart = new Chart(
            document.getElementById("temperature-chart"),
            {
                type: "line",
                data: {
                    labels,
                    datasets: [{
                        label: "CPU temperature",
                        data: values,
                        borderColor: "#ea580c",
                        backgroundColor: "#ea580c1f",
                        fill: true,
                        tension: 0.25,
                        pointRadius: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 8
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Temperature (°C)"
                            }
                        }
                    }
                }
            }
        );
    }
}

function refreshTemperature() {
    updateTemperature().catch(error => {
        console.error("Could not load temperature:", error);
    });
}

function refreshTemperatureHistory() {
    updateTemperatureHistory().catch(error => {
        console.error("Could not load temperature history:", error);
    });
}

async function updateBattery() {
    const response = await fetch("http://127.0.0.1:8000/battery");

    if (!response.ok) {
        throw new Error(`Battery request failed: ${response.status}`);
    }

    const data = await response.json();

    document.getElementById("battery-charge").textContent =
        `${data.charge_percent.toFixed(0)}%`;

    document.getElementById("battery-status").textContent =
        data.is_charging ? "Charging" : "Not charging";
}


let batteryChart;

async function updateBatteryHistory() {
    const response = await fetch("http://127.0.0.1:8000/battery/history");

    if (!response.ok) {
        throw new Error(`Battery history request failed: ${response.status}`);
    }

    const readings = await response.json();

    const labels = readings.map(reading =>
        new Date(reading.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        })
    );
    const values = readings.map(reading => reading.charge_percent);

    if (batteryChart) {
        batteryChart.data.labels = labels;
        batteryChart.data.datasets[0].data = values;
        batteryChart.update();
    } else {
        batteryChart = new Chart(document.getElementById("battery-chart"), {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Battery charge",
                    data: values,
                    borderColor: "#2563eb",
                    backgroundColor: "#2563eb1f",
                    fill: true,
                    stepped: true,
                    pointRadius: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { autoSkip: true, maxTicksLimit: 8 }
                    },
                    y: {
                        min: 0,
                        max: 100,
                        title: { display: true, text: "Charge (%)" }
                    }
                }
            }
        });
    }

    const trend = document.getElementById("battery-trend");

    if (readings.length < 2) {
        trend.textContent = "Collecting readings…";
        return;
    }

    const first = readings[0];
    const last = readings[readings.length - 1];
    const elapsedHours =
        (new Date(last.timestamp) - new Date(first.timestamp)) / 3600000;

    if (elapsedHours < 0.25) {
        trend.textContent =
            "Collecting data; the rate estimate needs at least 15 minutes.";
        return;
    }

    const changePerHour =
        (last.charge_percent - first.charge_percent) / elapsedHours;
    const sign = changePerHour > 0 ? "+" : "";

    trend.textContent =
        `Average battery change: ${sign}${changePerHour.toFixed(1)} percentage points per hour`;
}

function refreshBatteryHistory() {
    updateBatteryHistory().catch(error => {
        console.error("Could not load battery history:", error);
    });
}

async function updateApiStatus() {
    const dot = document.getElementById("api-status-dot");
    const text = document.getElementById("api-status-text");
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);

    try {
        const response = await fetch("http://127.0.0.1:8000/", {
            cache: "no-store",
            signal: controller.signal
        });

        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }

        dot.classList.remove("offline", "checking");
        dot.classList.add("online");
        text.textContent = "API Online";
    } catch {
        dot.classList.remove("online", "checking");
        dot.classList.add("offline");
        text.textContent = "API Offline";
    } finally {
        clearTimeout(timeoutId);
    }
}

refreshTemperature();
setInterval(refreshTemperature, 60000);

refreshTemperatureHistory();
setInterval(refreshTemperatureHistory, 60000);

updateBattery();
setInterval(updateBattery, 60000);

refreshBatteryHistory();
setInterval(refreshBatteryHistory, 60000);

updateApiStatus();
setInterval(updateApiStatus, 10000);