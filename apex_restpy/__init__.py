# __init__.py
# Created by Ata Can Yaymacı
# Python adaptation of ApexBridge C++ library

"""
apex_restpy — Python library for Oracle APEX RESTful API communication.

A Python adaptation of the ApexBridge C++ Arduino library, designed for
standard Python environments (servers, Raspberry Pi, scripts, etc.).

Quick start::

    from apex_restpy import ApexBridge

    bridge = ApexBridge(schema="myschema")
    bridge.set_token("my-jwt-token")
    bridge.prepare_url("time", "now")
    response = bridge.send_request()
    print(response["full_timestamp"])
"""

from .apex_app import ApexApp
from .apex_bridge import ApexBridge
from .exceptions import ApexConnectionError, ApexResponseError

__all__ = [
    "ApexBridge",
    "ApexApp",
    "ApexConnectionError",
    "ApexResponseError",
]

__version__ = "1.0.0"
__author__ = "Ata Can Yaymacı"
__email__ = "atacanymc@gmail.com"
