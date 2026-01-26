import html
import os
from typing import Any

import requests

BASE_URL = "https://api.api-ninjas.com/v1/animals"
TIMEOUT_SECONDS = 10
OUTPUT_FILE = "animals.html"
ENV_KEY_NAME = "API_NINJAS_KEY"
DEFAULT_ANIMAL = "Fox"


def normalize_animal_name(raw: str) -> str:
    """Normalize user input for animal name (strip only, keep case for display)."""
    return raw.strip()


def get_api_key() -> str:
    """Read API key from environment and validate it exists."""
    api_key = os.getenv(ENV_KEY_NAME)
    if not api_key:
        raise RuntimeError(f"Missing {ENV_KEY_NAME} environment variable.")
    return api_key


def fetch_animals(animal_name: str) -> list[dict]:
    """Fetch animal data from API Ninjas Animals endpoint for the given name."""
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


def prompt_animal_name() -> str:
    """Ask user for an animal name; empty input falls back to DEFAULT_ANIMAL."""
    while True:
        raw = input(f'Enter a name of an animal (default: "{DEFAULT_ANIMAL}"): ')
        animal_name = normalize_animal_name(raw)

        if animal_name:
            return animal_name

        return DEFAULT_ANIMAL


def safe_get(mapping: dict, key: str, default: str = "n/a") -> str:
    """Get a string value from a dict safely."""
    value = mapping.get(key, default)
    if value is None:
        return default
    return str(value)


def build_animal_section(animal: dict) -> str:
    """Build one HTML block for a single animal result."""
    name = html.escape(safe_get(animal, "name", "Unknown"))
    taxonomy = animal.get("taxonomy") if isinstance(animal.get("taxonomy"), dict) else {}
    characteristics = (
        animal.get("characteristics")
        if isinstance(animal.get("characteristics"), dict)
        else {}
    )
    locations = animal.get("locations") if isinstance(animal.get("locations"), list) else []

    taxonomy_lines = [
        f"<li><b>Kingdom:</b> {html.escape(safe_get(taxonomy, 'kingdom'))}</li>",
        f"<li><b>Phylum:</b> {html.escape(safe_get(taxonomy, 'phylum'))}</li>",
        f"<li><b>Class:</b> {html.escape(safe_get(taxonomy, 'class'))}</li>",
        f"<li><b>Order:</b> {html.escape(safe_get(taxonomy, 'order'))}</li>",
        f"<li><b>Family:</b> {html.escape(safe_get(taxonomy, 'family'))}</li>",
        f"<li><b>Genus:</b> {html.escape(safe_get(taxonomy, 'genus'))}</li>",
        f"<li><b>Scientific name:</b> {html.escape(safe_get(taxonomy, 'scientific_name'))}</li>",
    ]

    locations_text = ", ".join(html.escape(str(loc)) for loc in locations) if locations else "n/a"

    characteristics_lines = []
    for key in ["diet", "lifespan", "habitat", "predators", "top_speed", "weight"]:
        if key in characteristics:
            characteristics_lines.append(
                f"<li><b>{html.escape(key)}:</b> {html.escape(safe_get(characteristics, key))}</li>"
            )

    if not characteristics_lines:
        characteristics_lines.append("<li>n/a</li>")

    return f"""
    <section class="card">
      <h2>{name}</h2>

      <h3>Taxonomy</h3>
      <ul>
        {''.join(taxonomy_lines)}
      </ul>

      <h3>Locations</h3>
      <p>{locations_text}</p>

      <h3>Characteristics</h3>
      <ul>
        {''.join(characteristics_lines)}
      </ul>
    </section>
    """


def build_html_page(animal_name: str, animals: list[dict], error_message: str | None = None) -> str:
    """Build final HTML page."""
    safe_query = html.escape(animal_name)

    if error_message:
        content = f'<h2 class="error">{html.escape(error_message)}</h2>'
    elif not animals:
        content = f'<h2 class="error">The animal "{safe_query}" doesn\'t exist.</h2>'
    else:
        sections = "\n".join(build_animal_section(animal) for animal in animals)
        content = f"""
        <h2>Results for "{safe_query}"</h2>
        <p>Found {len(animals)} result(s).</p>
        {sections}
        """

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Animals</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 24px; }}
      .card {{ border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin: 16px 0; }}
      .error {{ color: #b00020; }}
      h1 {{ margin-bottom: 8px; }}
      h2 {{ margin-top: 0; }}
      ul {{ margin-top: 8px; }}
    </style>
  </head>
  <body>
    <h1>Animals API Results</h1>
    {content}
  </body>
</html>
"""


def write_html_file(html_text: str, filename: str = OUTPUT_FILE) -> None:
    """Write HTML to disk."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_text)


def main() -> None:
    """CLI entrypoint: ask for animal name, fetch via API, generate HTML."""
    animal_name = prompt_animal_name()

    try:
        animals = fetch_animals(animal_name)
        page = build_html_page(animal_name, animals)
    except RuntimeError as exc:
        page = build_html_page(animal_name, [], error_message=str(exc))

    write_html_file(page)
    print(f"Website was successfully generated to the file {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
