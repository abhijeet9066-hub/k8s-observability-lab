import random
import time
import httpx

BASE = "http://localhost:8000"

with httpx.Client(timeout=5.0) as client:
    for i in range(300):
        delay = random.choices([25, 80, 250, 900], [70, 20, 8, 2], k=1)[0]
        fail = random.random() < 0.06
        try:
            client.get(f"{BASE}/work", params={"delay_ms": delay, "fail": str(fail).lower()})
            if i % 5 == 0:
                client.post(f"{BASE}/checkout")
        except httpx.HTTPError:
            pass
        time.sleep(0.05)
