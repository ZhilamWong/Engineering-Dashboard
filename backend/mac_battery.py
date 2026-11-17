import json
import re
import subprocess
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


API_URL = "http://127.0.0.1:8000/battery"
SAMPLE_INTERVAL_SECONDS = 60


while True:
    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True,
            text=True,
            check=True,
        )

        battery_output = result.stdout
        charge_match = re.search(r"(\d+)%", battery_output)

        if charge_match is None:
            raise RuntimeError(
                f"Could not find battery percentage in:\n{battery_output}"
            )

        payload = {
            "charge_percent": float(charge_match.group(1)),
            "is_charging": "; charging;" in battery_output,
        }

        request = Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=5) as response:
            print("Saved battery reading:", response.read().decode("utf-8"))

    except (URLError, subprocess.CalledProcessError, RuntimeError) as error:
        print(f"Could not save battery reading: {error}")

    time.sleep(SAMPLE_INTERVAL_SECONDS)