# apex_app.py
# Created by Ata Can Yaymacı
# Python adaptation of ApexBridge C++ library

from dataclasses import dataclass


@dataclass
class ApexApp:
    """
    Represents the Oracle APEX application configuration.

    This is the Python equivalent of the C++ ApexApp struct:
        struct ApexApp {
            String schema;
            String token = "";
            String base_path = "/pls/apex";
        };

    Attributes:
        schema (str): The APEX workspace schema name.
        token (str): Bearer token for authentication. Empty string if not needed.
        base_path (str): Base path prefix for all APEX REST endpoints.
    """
    schema: str
    token: str = ""
    base_path: str = "/pls/apex"
