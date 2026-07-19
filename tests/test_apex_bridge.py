"""
tests/test_apex_bridge.py
Unit tests for ApexBridge — the Python adaptation of the ApexBridge C++ library.

Tests use unittest.mock to mock HTTP responses so no real network connection
is required. Each test mirrors a specific behaviour from the original C++ code.
"""

import unittest
from unittest.mock import MagicMock

from apex_restpy import ApexBridge
from apex_restpy.exceptions import ApexConnectionError, ApexResponseError


class TestPrepareUrl(unittest.TestCase):
    """Tests for prepare_url() — mirrors C++ prepareURL() method."""

    def setUp(self):
        self.bridge = ApexBridge(schema="testschema", base_path="/pls/apex")

    def test_prepare_url_returns_correct_path(self):
        url = self.bridge.prepare_url("time", "now")
        self.assertEqual(url, "/pls/apex/testschema/time/now")

    def test_prepare_url_stores_as_last_endpoint(self):
        self.bridge.prepare_url("sensor", "data")
        self.assertEqual(self.bridge.last_endpoint, "/pls/apex/testschema/sensor/data")

    def test_prepare_url_with_custom_schema(self):
        url = self.bridge.prepare_url("time", "now", schema="otherschema")
        self.assertEqual(url, "/pls/apex/otherschema/time/now")

    def test_prepare_url_overrides_previous_endpoint(self):
        self.bridge.prepare_url("module1", "resource1")
        self.bridge.prepare_url("module2", "resource2")
        self.assertEqual(self.bridge.last_endpoint, "/pls/apex/testschema/module2/resource2")


class TestAddParameter(unittest.TestCase):
    """Tests for add_parameter() — mirrors C++ addParameter() methods."""

    def setUp(self):
        self.bridge = ApexBridge(schema="testschema", base_path="/pls/apex")
        self.bridge.prepare_url("sensor", "data")

    def test_add_first_parameter_uses_question_mark(self):
        self.bridge.add_parameter("id", "123")
        self.assertIn("?id=123", self.bridge.last_endpoint)

    def test_add_second_parameter_uses_ampersand(self):
        self.bridge.add_parameter("id", "123")
        self.bridge.add_parameter("type", "temp")
        self.assertIn("&type=temp", self.bridge.last_endpoint)

    def test_add_parameter_to_custom_url(self):
        url = "/pls/apex/testschema/items/list"
        result = self.bridge.add_parameter("active", "true", url=url)
        self.assertEqual(result, "/pls/apex/testschema/items/list?active=true")

    def test_add_parameter_to_custom_url_already_has_query(self):
        url = "/pls/apex/testschema/items/list?status=new"
        result = self.bridge.add_parameter("limit", "10", url=url)
        self.assertIn("&limit=10", result)

    def test_add_parameter_does_not_modify_custom_url_endpoint(self):
        """When url argument is provided, _last_endpoint should not change."""
        original = self.bridge.last_endpoint
        custom = "/some/other/path"
        self.bridge.add_parameter("foo", "bar", url=custom)
        self.assertEqual(self.bridge.last_endpoint, original)


class TestAddPath(unittest.TestCase):
    """Tests for add_path() — mirrors C++ addPath() methods."""

    def setUp(self):
        self.bridge = ApexBridge(schema="testschema", base_path="/pls/apex")
        self.bridge.prepare_url("items", "list")

    def test_add_path_appends_to_last_endpoint(self):
        self.bridge.add_path("active")
        self.assertEqual(self.bridge.last_endpoint, "/pls/apex/testschema/items/list/active")

    def test_add_path_to_custom_url(self):
        url = "/pls/apex/testschema/items/list"
        result = self.bridge.add_path("archived", url=url)
        self.assertEqual(result, "/pls/apex/testschema/items/list/archived")

    def test_add_path_does_not_modify_custom_url_endpoint(self):
        """When url argument is provided, _last_endpoint should not change."""
        original = self.bridge.last_endpoint
        self.bridge.add_path("extra", url="/some/path")
        self.assertEqual(self.bridge.last_endpoint, original)


class TestSetToken(unittest.TestCase):
    """Tests for set_token() — mirrors C++ setToken() method."""

    def test_token_is_stored(self):
        bridge = ApexBridge(schema="test")
        bridge.set_token("my-secret-token")
        self.assertEqual(bridge._app.token, "my-secret-token")

    def test_empty_token_not_added_to_headers(self):
        bridge = ApexBridge(schema="test")
        headers = bridge._build_headers()
        self.assertNotIn("Authorization", headers)

    def test_token_added_to_headers_when_set(self):
        bridge = ApexBridge(schema="test")
        bridge.set_token("my-secret-token")
        headers = bridge._build_headers()
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], "Bearer my-secret-token")

    def test_single_char_token_not_added(self):
        """Mirrors C++ behaviour: token.length() > 1 required."""
        bridge = ApexBridge(schema="test")
        bridge.set_token("x")
        headers = bridge._build_headers()
        self.assertNotIn("Authorization", headers)


class TestSendRequestGet(unittest.TestCase):
    """Tests for send_request() with GET — mirrors C++ sendGet() behaviour."""

    def setUp(self):
        self.mock_session = MagicMock()
        self.bridge = ApexBridge(
            schema="testschema", base_path="/pls/apex", session=self.mock_session
        )
        self.bridge.prepare_url("time", "now")

    def _make_mock_response(self, json_data: dict, status_code: int = 200):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        return mock_resp

    def test_get_uses_last_endpoint(self):
        self.mock_session.get.return_value = self._make_mock_response(
            {"full_timestamp": "2025-01-01T00:00:00"}
        )
        self.bridge.send_request("GET")
        self.mock_session.get.assert_called_once()
        call_url = self.mock_session.get.call_args[0][0]
        self.assertIn("testschema/time/now", call_url)

    def test_get_returns_parsed_json(self):
        expected = {"full_timestamp": "2025-01-01", "year": 2025}
        self.mock_session.get.return_value = self._make_mock_response(expected)
        result = self.bridge.send_request()
        self.assertEqual(result, expected)

    def test_get_with_explicit_url(self):
        self.mock_session.get.return_value = self._make_mock_response({"ok": True})
        self.bridge.send_request("GET", url="/pls/apex/testschema/custom/path")
        call_url = self.mock_session.get.call_args[0][0]
        self.assertIn("custom/path", call_url)

    def test_get_includes_auth_header_when_token_set(self):
        self.bridge.set_token("test-token-xyz")
        self.mock_session.get.return_value = self._make_mock_response({})
        self.bridge.send_request("GET")
        call_headers = self.mock_session.get.call_args[1]["headers"]
        self.assertEqual(call_headers["Authorization"], "Bearer test-token-xyz")

    def test_get_no_auth_header_without_token(self):
        self.mock_session.get.return_value = self._make_mock_response({})
        self.bridge.send_request("GET")
        call_headers = self.mock_session.get.call_args[1]["headers"]
        self.assertNotIn("Authorization", call_headers)


class TestSendRequestPost(unittest.TestCase):
    """Tests for send_request() with POST — mirrors C++ sendPost() behaviour."""

    def setUp(self):
        self.mock_session = MagicMock()
        self.bridge = ApexBridge(
            schema="testschema", base_path="/pls/apex", session=self.mock_session
        )
        self.bridge.prepare_url("sensor", "data")

    def _make_mock_response(self, json_data: dict, status_code: int = 201):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        return mock_resp

    def test_post_sends_payload_as_json(self):
        self.mock_session.post.return_value = self._make_mock_response({"id": 1})
        payload = {"sensor_id": "42", "value": 23.5}
        self.bridge.send_request("POST", payload=payload)
        call_kwargs = self.mock_session.post.call_args[1]
        self.assertEqual(call_kwargs["json"], payload)

    def test_post_returns_parsed_json(self):
        expected = {"id": 42, "status": "created"}
        self.mock_session.post.return_value = self._make_mock_response(expected)
        result = self.bridge.send_request("POST", payload={"x": 1})
        self.assertEqual(result, expected)

    def test_post_without_payload_sends_empty_dict(self):
        self.mock_session.post.return_value = self._make_mock_response({})
        self.bridge.send_request("POST")
        call_kwargs = self.mock_session.post.call_args[1]
        self.assertEqual(call_kwargs["json"], {})


class TestSendRequestOtherMethods(unittest.TestCase):
    """Tests for PUT, PATCH, DELETE methods (Python-only additions)."""

    def setUp(self):
        self.mock_session = MagicMock()
        self.bridge = ApexBridge(
            schema="testschema", base_path="/pls/apex", session=self.mock_session
        )
        self.bridge.prepare_url("items", "list")

    def _make_mock_response(self, json_data: dict, status_code: int = 200):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        return mock_resp

    def test_put_request(self):
        self.mock_session.put.return_value = self._make_mock_response({"updated": True})
        result = self.bridge.send_request("PUT", payload={"name": "new"})
        self.mock_session.put.assert_called_once()
        self.assertEqual(result, {"updated": True})

    def test_patch_request(self):
        self.mock_session.patch.return_value = self._make_mock_response({"patched": True})
        result = self.bridge.send_request("PATCH", payload={"field": "value"})
        self.mock_session.patch.assert_called_once()
        self.assertEqual(result, {"patched": True})

    def test_delete_request(self):
        self.mock_session.delete.return_value = self._make_mock_response({"deleted": True})
        result = self.bridge.send_request("DELETE")
        self.mock_session.delete.assert_called_once()
        self.assertEqual(result, {"deleted": True})

    def test_unsupported_method_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.bridge.send_request("HEAD")


class TestErrorHandling(unittest.TestCase):
    """Tests for error handling — mirrors C++ connectApexClient() failure behaviour."""

    def setUp(self):
        self.mock_session = MagicMock()
        self.bridge = ApexBridge(
            schema="testschema", base_path="/pls/apex", session=self.mock_session
        )
        self.bridge.prepare_url("time", "now")

    def test_connection_error_raises_apex_connection_error(self):
        import requests as req

        self.mock_session.get.side_effect = req.exceptions.ConnectionError("refused")
        with self.assertRaises(ApexConnectionError):
            self.bridge.send_request("GET")

    def test_timeout_raises_apex_connection_error(self):
        import requests as req

        self.mock_session.get.side_effect = req.exceptions.Timeout("timed out")
        with self.assertRaises(ApexConnectionError):
            self.bridge.send_request("GET")

    def test_invalid_json_raises_apex_response_error(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("No JSON")
        mock_resp.text = "Not JSON content"
        self.mock_session.get.return_value = mock_resp
        with self.assertRaises(ApexResponseError):
            self.bridge.send_request("GET")


class TestBuildFullUrl(unittest.TestCase):
    """Tests for _build_full_url() internal helper."""

    def setUp(self):
        self.bridge = ApexBridge(schema="testschema", host="apex.oracle.com")

    def test_relative_path_gets_host_prepended(self):
        result = self.bridge._build_full_url("/pls/apex/schema/mod/res")
        self.assertEqual(result, "https://apex.oracle.com/pls/apex/schema/mod/res")

    def test_absolute_https_url_returned_unchanged(self):
        url = "https://custom.host.com/api/resource"
        result = self.bridge._build_full_url(url)
        self.assertEqual(result, url)

    def test_absolute_http_url_returned_unchanged(self):
        url = "http://localhost:8080/api/resource"
        result = self.bridge._build_full_url(url)
        self.assertEqual(result, url)


class TestProperties(unittest.TestCase):
    """Tests for read-only properties."""

    def test_schema_property(self):
        bridge = ApexBridge(schema="myschema")
        self.assertEqual(bridge.schema, "myschema")

    def test_base_path_property(self):
        bridge = ApexBridge(schema="myschema", base_path="/custom/path")
        self.assertEqual(bridge.base_path, "/custom/path")

    def test_last_endpoint_initially_empty(self):
        bridge = ApexBridge(schema="myschema")
        self.assertEqual(bridge.last_endpoint, "")

    def test_last_endpoint_after_prepare_url(self):
        bridge = ApexBridge(schema="myschema")
        bridge.prepare_url("mod", "res")
        self.assertEqual(bridge.last_endpoint, "/pls/apex/myschema/mod/res")


if __name__ == "__main__":
    unittest.main()
