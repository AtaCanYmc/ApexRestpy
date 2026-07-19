# exceptions.py
# Created by Ata Can Yaymacı
# Python adaptation of ApexBridge C++ library


class ApexConnectionError(Exception):
    """
    Raised when a connection to the Oracle APEX host cannot be established,
    or when an HTTP request fails (network error, timeout, etc.).
    """

    pass


class ApexResponseError(Exception):
    """
    Raised when the APEX API returns an error response (non-2xx status code)
    or when the response body cannot be decoded as JSON.
    """

    pass
