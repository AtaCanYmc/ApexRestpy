# apex_bridge.py
# Created by Ata Can Yaymacı
# Python adaptation of ApexBridge C++ library

import logging
from typing import Optional, cast

import requests

from .apex_app import ApexApp
from .exceptions import ApexConnectionError, ApexResponseError

# Default APEX host constants (mirrors C++ #define values)
APEX_HOST = "apex.oracle.com"
APEX_PORT = 443
APEX_BASE_URL = f"https://{APEX_HOST}"

logger = logging.getLogger(__name__)


class ApexBridge:
    """
    Python adaptation of the ApexBridge C++ Arduino library.

    Provides a simple interface for communicating with Oracle APEX RESTful
    services over HTTPS. Supports Bearer token authentication, URL construction,
    and GET / POST / PUT / PATCH / DELETE HTTP methods.

    C++ equivalent:
        class ApexBridge {
            ApexBridge(String schema, String base_path, Client &client);
            ...
        };

    Usage::

        bridge = ApexBridge(schema="myschema", base_path="/pls/apex")
        bridge.set_token("my-jwt-token")
        bridge.prepare_url("time", "now")
        response = bridge.send_request()
        print(response["full_timestamp"])

    Args:
        schema (str): The APEX workspace schema name.
        base_path (str): Base path for APEX endpoints. Default: ``"/pls/apex"``.
        host (str): Oracle APEX host. Default: ``"apex.oracle.com"``.
        timeout (float): Request timeout in seconds. Default: ``10.0``.
        debug (bool): Enable debug logging. Default: ``False``.
        session (requests.Session | None): Optional custom requests session.
            Useful for testing or custom SSL configuration.
    """

    def __init__(
        self,
        schema: str,
        base_path: str = "/pls/apex",
        host: str = APEX_HOST,
        timeout: float = 10.0,
        debug: bool = False,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._app = ApexApp(schema=schema, base_path=base_path)
        self._host = host
        self._base_url = f"https://{host}"
        self._timeout = timeout
        self._last_endpoint: str = ""
        self._session = session or requests.Session()

        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    # ------------------------------------------------------------------
    # Public API — mirrors the C++ ApexBridge public interface
    # ------------------------------------------------------------------

    def set_token(self, token: str) -> None:
        """
        Set the Bearer token for authenticated APEX requests.

        C++ equivalent: ``void ApexBridge::setToken(String token)``

        Args:
            token (str): JWT or OAuth Bearer token string.
        """
        self._app.token = token

    def prepare_url(
        self,
        module: str,
        resource: str,
        schema: Optional[str] = None,
    ) -> str:
        """
        Build the full APEX REST endpoint path and store it as the last endpoint.

        C++ equivalent:
            ``String ApexBridge::prepareURL(String module, String resource)``
            ``String ApexBridge::prepareURL(String schema, String module, String resource)``

        The constructed path follows the pattern:
            ``<base_path>/<schema>/<module>/<resource>``

        Args:
            module (str): APEX REST module name.
            resource (str): APEX REST resource name.
            schema (str | None): Override the default schema. Uses the instance
                schema when not provided.

        Returns:
            str: The constructed URL path (relative, without host).

        Example::

            bridge.prepare_url("time", "now")
            # -> "/pls/apex/myschema/time/now"
        """
        effective_schema = schema or self._app.schema
        url = f"{self._app.base_path}/{effective_schema}/{module}/{resource}"
        self._last_endpoint = url
        self._log(f"[APEX BRIDGE] Prepared URL: {url}")
        return url

    def add_parameter(self, param: str, value: str, url: Optional[str] = None) -> str:
        """
        Append a query parameter to the last endpoint (or a given URL).

        C++ equivalent:
            ``void ApexBridge::addParameter(String param, String value)``
            ``void ApexBridge::addParameter(String &url, String param, String value)``

        If ``url`` is provided, the parameter is appended to that URL and returned.
        Otherwise, the parameter is appended to the internal ``_last_endpoint``.

        Args:
            param (str): Query parameter name.
            value (str): Query parameter value.
            url (str | None): Optional URL to modify instead of the stored endpoint.

        Returns:
            str: The modified URL (with query parameter appended).

        Example::

            bridge.prepare_url("sensor", "data")
            bridge.add_parameter("id", "123")
            # _last_endpoint -> "/pls/apex/myschema/sensor/data?id=123"
        """
        if url is not None:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{param}={value}"
            return url
        else:
            separator = "&" if "?" in self._last_endpoint else "?"
            self._last_endpoint = f"{self._last_endpoint}{separator}{param}={value}"
            return self._last_endpoint

    def add_path(self, path: str, url: Optional[str] = None) -> str:
        """
        Append an additional path segment to the last endpoint (or a given URL).

        C++ equivalent:
            ``void ApexBridge::addPath(String path)``
            ``void ApexBridge::addPath(String &url, String path)``

        Args:
            path (str): Path segment to append.
            url (str | None): Optional URL to modify instead of the stored endpoint.

        Returns:
            str: The modified URL (with path appended).

        Example::

            bridge.prepare_url("items", "list")
            bridge.add_path("active")
            # _last_endpoint -> "/pls/apex/myschema/items/list/active"
        """
        if url is not None:
            url = f"{url}/{path}"
            return url
        else:
            self._last_endpoint = f"{self._last_endpoint}/{path}"
            return self._last_endpoint

    def send_request(
        self,
        method: str = "GET",
        payload: Optional[dict] = None,
        url: Optional[str] = None,
    ) -> dict[str, object]:
        """
        Send an HTTP request to the Oracle APEX REST endpoint.

        C++ equivalent:
            ``DynamicJsonDocument ApexBridge::sendRequest(const char* method)``
            ``DynamicJsonDocument ApexBridge::sendRequest(DynamicJsonDocument payload, const char* method)``
            ``DynamicJsonDocument ApexBridge::sendRequest(const char* url, DynamicJsonDocument payload, const char* method)``

        Uses the stored ``_last_endpoint`` when ``url`` is not provided.
        Supports GET, POST, PUT, PATCH, and DELETE methods.

        Args:
            method (str): HTTP method. One of ``"GET"``, ``"POST"``,
                ``"PUT"``, ``"PATCH"``, ``"DELETE"``. Default: ``"GET"``.
            payload (dict | None): JSON payload body for POST/PUT/PATCH requests.
            url (str | None): Override URL path (relative or absolute). Uses
                ``_last_endpoint`` when not provided.

        Returns:
            dict: Parsed JSON response body. Returns an empty dict ``{}`` on failure.

        Raises:
            ApexConnectionError: When the network request fails entirely.
            ApexResponseError: When the response cannot be decoded as JSON.

        Example::

            bridge.prepare_url("sensor", "data")
            bridge.add_parameter("id", "42")
            response = bridge.send_request("GET")
            print(response["value"])
        """
        target_url = url or self._last_endpoint
        full_url = self._build_full_url(target_url)
        method = method.upper()

        headers = self._build_headers()
        self._log(f"[APEX BRIDGE] {method} {full_url}")

        try:
            response = self._dispatch(method, full_url, headers, payload)
        except requests.exceptions.ConnectionError as exc:
            self._log(f"[APEX BRIDGE] Connection failed: {exc}")
            raise ApexConnectionError(f"Could not connect to {self._host}: {exc}") from exc
        except requests.exceptions.Timeout as exc:
            self._log(f"[APEX BRIDGE] Request timed out: {exc}")
            raise ApexConnectionError(f"Request timed out after {self._timeout}s: {exc}") from exc
        except requests.exceptions.RequestException as exc:
            self._log(f"[APEX BRIDGE] Request error: {exc}")
            raise ApexConnectionError(f"Request failed: {exc}") from exc

        self._log(f"[APEX BRIDGE] Response status: {response.status_code}")

        try:
            return cast(dict[str, object], response.json())
        except ValueError as exc:
            self._log(f"[APEX BRIDGE] JSON decode error: {exc}")
            raise ApexResponseError(
                f"Response body is not valid JSON (status {response.status_code}): {response.text[:200]}"
            ) from exc

    # ------------------------------------------------------------------
    # Private helpers — mirrors C++ private methods
    # ------------------------------------------------------------------

    def _dispatch(
        self,
        method: str,
        full_url: str,
        headers: dict,
        payload: Optional[dict],
    ) -> requests.Response:
        """
        Route the HTTP request to the appropriate internal send method.

        C++ equivalent: the ``if (strcmp(method, "GET") == 0) { ... }`` block
        inside ``ApexBridge::sendRequest``.

        Args:
            method (str): Uppercase HTTP method string.
            full_url (str): Fully qualified request URL.
            headers (dict): Request headers including Authorization if set.
            payload (dict | None): JSON payload for body-carrying methods.

        Returns:
            requests.Response: The raw HTTP response object.
        """
        if method == "GET":
            return self._send_get(full_url, headers)
        elif method == "POST":
            return self._send_post(full_url, headers, payload or {})
        elif method == "PUT":
            return self._send_put(full_url, headers, payload or {})
        elif method == "PATCH":
            return self._send_patch(full_url, headers, payload or {})
        elif method == "DELETE":
            return self._send_delete(full_url, headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method!r}")

    def _send_get(self, url: str, headers: dict) -> requests.Response:
        """
        Send a GET request.

        C++ equivalent: ``String ApexBridge::sendGet(const char* url)``

        Args:
            url (str): Full URL to request.
            headers (dict): HTTP headers.

        Returns:
            requests.Response: The HTTP response.
        """
        return self._session.get(url, headers=headers, timeout=self._timeout)

    def _send_post(self, url: str, headers: dict, payload: dict) -> requests.Response:
        """
        Send a POST request with a JSON body.

        C++ equivalent: ``String ApexBridge::sendPost(const char* url, DynamicJsonDocument payload)``

        Args:
            url (str): Full URL to post to.
            headers (dict): HTTP headers.
            payload (dict): JSON payload to send in the request body.

        Returns:
            requests.Response: The HTTP response.
        """
        return self._session.post(url, headers=headers, json=payload, timeout=self._timeout)

    def _send_put(self, url: str, headers: dict, payload: dict) -> requests.Response:
        """
        Send a PUT request with a JSON body.

        Args:
            url (str): Full URL.
            headers (dict): HTTP headers.
            payload (dict): JSON payload.

        Returns:
            requests.Response: The HTTP response.
        """
        return self._session.put(url, headers=headers, json=payload, timeout=self._timeout)

    def _send_patch(self, url: str, headers: dict, payload: dict) -> requests.Response:
        """
        Send a PATCH request with a JSON body.

        Args:
            url (str): Full URL.
            headers (dict): HTTP headers.
            payload (dict): JSON payload.

        Returns:
            requests.Response: The HTTP response.
        """
        return self._session.patch(url, headers=headers, json=payload, timeout=self._timeout)

    def _send_delete(self, url: str, headers: dict) -> requests.Response:
        """
        Send a DELETE request.

        Args:
            url (str): Full URL.
            headers (dict): HTTP headers.

        Returns:
            requests.Response: The HTTP response.
        """
        return self._session.delete(url, headers=headers, timeout=self._timeout)

    def _build_headers(self) -> dict:
        """
        Build the HTTP headers dict for a request.

        Mirrors the C++ behaviour of conditionally adding the Authorization header:
            if (app.token.length() > 1) {
                client->print("Authorization: Bearer ");
                client->println(app.token);
            }

        Returns:
            dict: Headers dict, including ``Authorization`` when a token is set.
        """
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if len(self._app.token) > 1:
            headers["Authorization"] = f"Bearer {self._app.token}"
        return headers

    def _build_full_url(self, path: str) -> str:
        """
        Prepend the base URL to a relative path when necessary.

        Args:
            path (str): Relative path (e.g. ``"/pls/apex/schema/mod/res"``)
                or absolute URL.

        Returns:
            str: Fully qualified HTTPS URL.
        """
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self._base_url}{path}"

    def _log(self, message: str) -> None:
        """
        Emit a debug log message.

        C++ equivalent:
            ``void ApexBridge::log(String message)`` (controlled by ``#ifdef BRIDGE_DEBUG``)

        Args:
            message (str): The message to log at DEBUG level.
        """
        logger.debug(message)

    # ------------------------------------------------------------------
    # Properties for read access
    # ------------------------------------------------------------------

    @property
    def last_endpoint(self) -> str:
        """The most recently prepared URL path."""
        return self._last_endpoint

    @property
    def schema(self) -> str:
        """The APEX schema configured for this bridge instance."""
        return self._app.schema

    @property
    def base_path(self) -> str:
        """The base path prefix used when constructing APEX URLs."""
        return self._app.base_path
