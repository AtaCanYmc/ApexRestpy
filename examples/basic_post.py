"""
examples/basic_post.py
Basic example: sending sensor data to Oracle APEX RESTful API using a POST request.

Usage:
    python examples/basic_post.py

Replace <your-schema> with your actual Oracle APEX schema name, and
<your-jwt-token> with a valid Bearer token if your endpoint requires authentication.
"""

from apex_restpy import ApexBridge

# -------------------------------------------------------------------
# 1. Configure your Oracle APEX schema
# -------------------------------------------------------------------
SCHEMA = "<your-schema>"
BASE_PATH = "/pls/apex"
TOKEN = "<your-jwt-token>"

# -------------------------------------------------------------------
# 2. Initialize ApexBridge and set authentication token
# -------------------------------------------------------------------
bridge = ApexBridge(schema=SCHEMA, base_path=BASE_PATH)
bridge.set_token(TOKEN)

# -------------------------------------------------------------------
# 3. Prepare the URL
#    Builds: /pls/apex/<your-schema>/sensor/data
# -------------------------------------------------------------------
bridge.prepare_url("sensor", "data")

# -------------------------------------------------------------------
# 4. Build the JSON payload and send a POST request
#    (equivalent of: apex.sendRequest(payload, "POST");)
# -------------------------------------------------------------------
payload = {
    "sensor_id": "42",
    "temperature": 23.5,
    "humidity": 65.0,
    "unit": "celsius",
}

response = bridge.send_request("POST", payload=payload)

# -------------------------------------------------------------------
# 5. Print the response
# -------------------------------------------------------------------
print("Response:", response)
print("Status:", response.get("status"))
print("Created ID:", response.get("id"))
