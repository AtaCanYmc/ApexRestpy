# ApexRestpy

ApexRestpy is a lightweight Python library designed to seamlessly interact with Oracle APEX RESTful services. It is the Python adaptation of the [ApexBridge](https://github.com/AtaCanYmc/ApexBridge) C++ Arduino library, bringing the same simple and clean API to standard Python environments (servers, Raspberry Pi, scripts, automation, etc.).

## ✨ Features
- 🔗 **Seamless API Communication**: Easily interact with Oracle APEX RESTful services.
- 🔒 **Secure Connections**: HTTPS with automatic SSL certificate validation via `certifi`.
- 🔑 **Token-Based Authentication**: Handles Bearer token authentication.
- 🛠 **Built-in URL Management**: Automatically constructs request URLs based on schema, module, and resources.
- ⚡ **Full HTTP Support**: GET, POST, PUT, PATCH, and DELETE methods.
- 🐍 **Pythonic API**: `snake_case` methods, dataclasses, type hints, and standard `logging`.

## 📦 Installation

```bash
pip install apex-restpy
```

Or install directly from source:

```bash
git clone https://github.com/AtaCanYmc/ApexRestpy.git
cd ApexRestpy
pip install -e .
```

## 🔧 Dependencies
- [`requests`](https://docs.python-requests.org/) — HTTP client library.

## 🚀 Getting Started

### 1️⃣ Import the Library
```python
from apex_restpy import ApexBridge
```

### 2️⃣ Initialize ApexBridge
```python
schema = "<your-schema>"
base_path = "/pls/apex"
bridge = ApexBridge(schema=schema, base_path=base_path)
```

### 3️⃣ (Optional) Set an Authentication Token
```python
bridge.set_token("your-jwt-token")
```

### 4️⃣ Prepare a URL
```python
# Builds: /pls/apex/<schema>/time/now
bridge.prepare_url("time", "now")
```

### 5️⃣ Send a Request
```python
response = bridge.send_request("GET")
print(response["full_timestamp"])
print(response["year"])
```

## 📖 API Reference

### `ApexBridge(schema, base_path="/pls/apex", host="apex.oracle.com", timeout=10.0, debug=False)`
Initializes the bridge with your APEX workspace configuration.

### `set_token(token: str)`
Sets the Bearer authentication token for all subsequent requests.

### `prepare_url(module: str, resource: str, schema: str | None = None) -> str`
Builds the full APEX REST path (`<base_path>/<schema>/<module>/<resource>`) and stores it as the active endpoint.

### `add_parameter(param: str, value: str, url: str | None = None) -> str`
Appends a query parameter (`?param=value` or `&param=value`) to the active endpoint or a given URL.

### `add_path(path: str, url: str | None = None) -> str`
Appends an additional path segment to the active endpoint or a given URL.

### `send_request(method="GET", payload=None, url=None) -> dict`
Sends an HTTP request to the active endpoint (or a given URL). Returns the parsed JSON response as a `dict`.

Supported methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

## 🛠 Example Use Cases

### GET Request
```python
from apex_restpy import ApexBridge

bridge = ApexBridge(schema="myschema")
bridge.set_token("your-jwt-token")
bridge.prepare_url("sensor", "data")
bridge.add_parameter("id", "123")
response = bridge.send_request("GET")
print(response["status"])
```

### POST Request
```python
from apex_restpy import ApexBridge

bridge = ApexBridge(schema="myschema")
bridge.set_token("your-jwt-token")
bridge.prepare_url("sensor", "data")

payload = {"sensor_id": "42", "temperature": 23.5}
response = bridge.send_request("POST", payload=payload)
print(response)
```

### Chaining Parameters and Paths
```python
bridge.prepare_url("items", "list")
bridge.add_parameter("status", "active")
bridge.add_parameter("limit", "10")
bridge.add_path("summary")
# Resulting endpoint: /pls/apex/myschema/items/list/summary?status=active&limit=10
response = bridge.send_request()
```

## 🔄 Comparison with C++ ApexBridge

| C++ (Arduino)                         | Python (ApexRestpy)                      |
|---------------------------------------|------------------------------------------|
| `ApexBridge(schema, basePath, client)`| `ApexBridge(schema, base_path)`          |
| `apex.setToken(token)`                | `bridge.set_token(token)`                |
| `apex.prepareURL(module, resource)`   | `bridge.prepare_url(module, resource)`   |
| `apex.addParameter(param, value)`     | `bridge.add_parameter(param, value)`     |
| `apex.addPath(path)`                  | `bridge.add_path(path)`                  |
| `apex.sendRequest("GET")`             | `bridge.send_request("GET")`             |
| `DynamicJsonDocument` (ArduinoJson)   | `dict` (built-in Python)                 |
| Manual SSL certificate embedding      | Automatic via `requests` + `certifi`     |
| `Serial.println(...)` debug           | Python `logging` module                  |

## 🧪 Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.

## 📬 Contact & Support
- **Author**: Ata Can Yaymacı
- **Medium**: [@atacanymc](https://medium.com/@atacanymc)
- **GitHub**: [AtaCanYmc](https://github.com/AtaCanYmc)
- **C++ Original**: [ApexBridge](https://github.com/AtaCanYmc/ApexBridge)

If you find this library useful, consider giving it a ⭐ on GitHub!

---

🐍 *Happy coding with ApexRestpy!*
