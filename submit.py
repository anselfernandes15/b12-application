import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
import os


def main():
    # Build payload
    payload = {
        "action_run_link": os.environ["ACTION_RUN_LINK"],
        "email": "anselfernandes25@gmail.com",
        "name": "Ansel Fernandes",
        "repository_link": os.environ["REPOSITORY_LINK"],
        "resume_link": "https://www.linkedin.com/in/anselfernandes",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"
    }

    # Serialize with compact separators and sorted keys
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    body_bytes = body.encode("utf-8")

    # Compute HMAC-SHA256 signature
    signing_secret = os.environ.get("SIGNING_SECRET", "hello-there-from-b12")
    hex_digest = hmac.new(
        signing_secret.encode("utf-8"),
        body_bytes,
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={hex_digest}"
    }

    # POST to B12
    response = requests.post(
        "https://b12.io/apply/submission",
        data=body_bytes,
        headers=headers
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print(f"Receipt: {data['receipt']}")
        else:
            print("Submission was not successful")
    else:
        print(f"Error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    main()
