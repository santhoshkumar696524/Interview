"""Module for handling authentication credentials."""
import os
import json


def get_auth_creds():
    """Gets the auth creds from a file."""

    file_path = os.path.join(os.path.dirname(__file__), "auth_creds.json")
    with open(file_path, "r", encoding="utf-8") as file:
        auth_creds = json.load(file)

    return auth_creds

def save_auth_creds(auth_creds):
    """Saves the auth creds to a file."""
    
    file_path = os.path.join(os.path.dirname(__file__), "auth_creds.json")
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(auth_creds, file)
