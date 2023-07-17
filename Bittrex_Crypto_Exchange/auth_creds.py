"""Module for handling authentication credentials."""
import os
import json


def get_auth_creds():
    """Gets the auth creds from a file."""

    file_path = os.path.join(os.path.dirname(__file__), "auth_creds.json")
    with open(file_path, "r", encoding="utf-8") as file:
        auth_creds = json.load(file)

    return auth_creds
