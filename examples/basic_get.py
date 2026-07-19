"""
examples/basic_get.py
Basic example: reading time from Oracle APEX RESTful API using a GET request.

This is the Python equivalent of the C++ ESP32/ESP8266 example:
    examples/ESP32/basic-read-time.ino

Usage:
    python examples/basic_get.py

Replace <your-schema> with your actual Oracle APEX schema name.
"""

from apex_restpy import ApexBridge

# -------------------------------------------------------------------
# 1. Configure your Oracle APEX schema
# -------------------------------------------------------------------
SCHEMA = "<your-schema>"
BASE_PATH = "/pls/apex"

# -------------------------------------------------------------------
# 2. Initialize ApexBridge
#    (equivalent of: ApexBridge apex = ApexBridge(schema, base_path, clientApex);)
# -------------------------------------------------------------------
bridge = ApexBridge(schema=SCHEMA, base_path=BASE_PATH)

# -------------------------------------------------------------------
# 3. (Optional) Set a Bearer token for authenticated endpoints
#    (equivalent of: apex.setToken("your-jwt-token");)
# -------------------------------------------------------------------
# bridge.set_token("your-jwt-token")

# -------------------------------------------------------------------
# 4. Prepare the URL and send a GET request
#    Builds: /pls/apex/<your-schema>/time/now
#    (equivalent of: apex.prepareURL("time", "now"); apex.sendRequest();)
# -------------------------------------------------------------------
bridge.prepare_url("time", "now")
response = bridge.send_request("GET")

# -------------------------------------------------------------------
# 5. Print the results
#    (equivalent of: Serial.println(doc["full_timestamp"].as<String>());)
# -------------------------------------------------------------------
print("Full timestamp:", response.get("full_timestamp"))
print("Year:", response.get("year"))
