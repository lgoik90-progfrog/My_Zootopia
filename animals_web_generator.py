import json
from json import JSONDecodeError

DEBUG_PRINT = False


def load_data(file_path):
    """Loads a JSON file and returns the parsed data structure."""
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {file_path}")
        return []
    except PermissionError:
        print(f"Fehler: Keine Berechtigung für: {file_path}")
        return []
    except JSONDecodeError as exc:
        print(f"Fehler: Ungültiges JSON in {file_path}: {exc}")
        return []


def extract_animal_fields(animal):
    """Extracts the relevant fields for the HTML card from one animal dict."""
    if not isinstance(animal, dict):
        return None

    name = animal.get("name")

    characteristics = animal.get("characteristics", {})
    if not isinstance(characteristics, dict):
        characteristics = {}

    diet = characteristics.get("diet")
    animal_type = characteristics.get("type")

    locations = animal.get("locations")
    location = None
    if isinstance(locations, list) and locations:
        location = locations[0]

    return {
        "name": name,
        "diet": diet,
        "location": location,
        "type": animal_type,
    }


def build_info_line(label, value):
    """Builds one labeled line inside the card text block."""
    if not value:
        return ""
    return f'      <strong>{label}:</strong> {value}<br/>\n'


def build_animal_li(animal):
    """Serializes one animal into the Step-4 <li class="cards__item">...</li> card."""
    fields = extract_animal_fields(animal)
    if not fields or not fields.get("name"):
        return ""

    parts = []
    parts.append('<li class="cards__item">\n')
    parts.append(f'  <div class="card__title">{fields["name"]}</div>\n')
    parts.append('  <p class="card__text">\n')
    parts.append(build_info_line("Diet", fields.get("diet")))
    parts.append(build_info_line("Location", fields.get("location")))
    parts.append(build_info_line("Type", fields.get("type")))
    parts.append("  </p>\n")
    parts.append("</li>\n")

    return "".join(parts)


def read_template(file_path):
    """Loads an HTML template file and returns it as a string."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return handle.read()


def write_html(file_path, html_content):
    """Writes the given HTML content to a file."""
    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(html_content)


def main():
    animals_data = load_data("animals_data.json")
    if not isinstance(animals_data, list):
        print("Fehler: animals_data.json muss eine Liste von Tieren enthalten.")
        return

    if DEBUG_PRINT:
        for animal in animals_data:
            fields = extract_animal_fields(animal)
            if not fields or not fields.get("name"):
                continue

            lines = []
            lines.append(f'Name: {fields["name"]}')
            if fields.get("diet"):
                lines.append(f'Diet: {fields["diet"]}')
            if fields.get("location"):
                lines.append(f'Location: {fields["location"]}')
            if fields.get("type"):
                lines.append(f'Type: {fields["type"]}')

            print("\n".join(lines))
            print()

    animals_li_items = []
    for animal in animals_data:
        animal_li = build_animal_li(animal)
        if animal_li:
            animals_li_items.append(animal_li)

    template = read_template("animals_template.html")
    animals_html = "\n".join(animals_li_items)
    html_page = template.replace("__REPLACE_ANIMALS_INFO__", animals_html)
    write_html("animals.html", html_page)


if __name__ == "__main__":
    main()
