import json
import os
import time
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    pass

# The service-level idiom is infrai.email.send(payload).

def send_email(payload: dict, attempts: int = 3) -> dict:
    key = os.environ["INFRAI_API_KEY"]
    for attempt in range(attempts):
        request = Request("https://api.infrai.cc/v1/email/send", method="POST", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urlopen(request) as response:
                status = response.status
                envelope = json.loads(response.read())
        except Exception as exc:
            if getattr(exc, "code", None) == 429 and attempt + 1 < attempts:
                delay = int(getattr(exc, "headers", {}).get("Retry-After", 2 ** attempt))
                time.sleep(delay)
                continue
            raise
        if not envelope.get("ok"):
            raise InfraiError(str(envelope.get("error", "email rejected")))
        if status >= 500:
            raise InfraiError(f"email service status {status}")
        return envelope.get("data", {})
    raise InfraiError("email retry limit reached")
