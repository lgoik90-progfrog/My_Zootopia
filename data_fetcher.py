import os
import requests

BASE_URL = "https://api.api-ninjas.com/v1/animals"
TIMEOUT_SECONDS = 10
ENV_KEY_NAME = "API_NINJAS_KEY"


def get_api_key() -> str:
    """Read API key from environment and validate it exists."""
    api_key = os.getenv(ENV_KEY_NAME)
    if not api_key:
        raise RuntimeError(f"Missing {ENV_KEY_NAME} environment variable.")
    return api_key


def fetch_data(animal_name: str) -> list[dict]:
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals (list[dict]).
    """
    api_key = get_api_key()

    params = {"name": animal_name}
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("Request timed out.") from exc
    except requests.exceptions.HTTPError as exc:
        status = getattr(response, "status_code", "n/a")
        raise RuntimeError(f"HTTP error: {status}") from exc
    except ValueError as exc:
        raise RuntimeError("Invalid JSON in response.") from exc

    if not isinstance(data, list):
        raise RuntimeError("Unexpected API response format (expected list).")

    return data
