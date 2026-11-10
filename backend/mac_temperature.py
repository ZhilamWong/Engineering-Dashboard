import json
import subprocess
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


API_URL = "http://127.0.0.1:8000/sensors"
SAMPLE_INTERVAL_SECONDS = 60


while True:
    try:
        result = subprocess.run(
            ["macmon", "pipe", "-s", "1"],
            capture_output=True,
            text=True,
            check=True,
        )

        metrics = json.loads(result.stdout)
        temperature = metrics["temp"]["cpu_temp_avg"]

        if temperature is None:
            raise RuntimeError("macmon did not return a CPU temperature")

        payload = {"temperature": float(temperature)}

        request = Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            print("Saved temperature reading:", response.read().decode("utf-8"))

    except (
        URLError,
        subprocess.CalledProcessError,
        json.JSONDecodeError,
        KeyError,
        RuntimeError,
    ) as error:
        print(f"Could not save temperature reading: {error}")

    time.sleep(SAMPLE_INTERVAL_SECONDS)