"""
Website Generator: asks the user for an animal name, fetches animals via data_fetcher,
and generates animals.html using animals_template.html.
"""

from __future__ import annotations

from dotenv import load_dotenv

import data_fetcher


TEMPLATE_PATH = "animals_template.html"
OUTPUT_PATH = "animals.html"
DEFAULT_ANIMAL = "Fox"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def get_animal_name() -> str:
    """Prompt the user for an animal name. Use DEFAULT_ANIMAL if empty."""
    user_input = input(f'Enter a name of an animal (default: "{DEFAULT_ANIMAL}"): ').strip()
    return user_input or DEFAULT_ANIMAL


def load_template(path: str) -> str:
    """Load the HTML template from disk."""
    with open(path, "r", encoding="utf-8") as template_file:
        return template_file.read()


def write_html(path: str, html: str) -> None:
    """Write the generated HTML to disk."""
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.write(html)


def build_animal_cards_html(animals: list[dict], animal_name: str) -> str:
    """
    Build the HTML that replaces PLACEHOLDER.

    If no animals were found, return a friendly message.
    """
    if not animals:
        return f'<li class="cards__item"><h2>The animal "{animal_name}" doesn\'t exist.</h2></li>'

    cards: list[str] = []
    for animal in animals:
        name = animal.get("name", "Unknown")
        locations = ", ".join(animal.get("locations", [])) or "Unknown"

        cards.append(
            f"""
            <li class="cards__item">
                <h2 class="card__title">{name}</h2>
                <p class="card__text"><strong>Locations:</strong> {locations}</p>
            </li>
            """.strip()
        )

    return "\n".join(cards)


def main() -> None:
    load_dotenv()

    animal_name = get_animal_name()
    animals = data_fetcher.fetch_data(animal_name)

    template = load_template(TEMPLATE_PATH)
    animals_html = build_animal_cards_html(animals, animal_name)

    final_html = template.replace(PLACEHOLDER, animals_html)
    write_html(OUTPUT_PATH, final_html)

    print(f"Website was successfully generated to the file {OUTPUT_PATH}.")


if __name__ == "__main__":
    main()
