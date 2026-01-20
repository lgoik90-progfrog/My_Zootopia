import json
from json import JSONDecodeError


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

def format_animal(animal):
    """Builds the output lines for one animal dict."""
    lines = []

    name = animal.get("name")
    if name:
        lines.append(f"Name: {name}")

    characteristics = animal.get("characteristics", {})
    diet = characteristics.get("diet")
    if diet:
        lines.append(f"Diet: {diet}")

    locations = animal.get("locations")
    if isinstance(locations, list) and locations:
        lines.append(f"Location: {locations[0]}")

    animal_type = characteristics.get("type")
    if animal_type:
        lines.append(f"Type: {animal_type}")

    return lines



def build_animal_li(animal):
    """Builds one <li> card for the animal for the HTML page."""
    lines = format_animal(animal)
    if not lines:
        return ""

    title = ""
    body_lines = []

    for line in lines:
        if line.startswith("Name: "):
            title = line.replace("Name: ", "").strip()
        else:
            body_lines.append(line)

    body_html = "<br>".join(body_lines)

    return (
        '<li class="cards__item">'
        f'<div class="card__title">{title}</div>'
        f'<p class="card__text">{body_html}</p>'
        "</li>"
    )


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

    # 1) Optional: Konsole (Debug / Schritt 1)
    for animal in animals_data:
        if not isinstance(animal, dict):
            continue

        lines = format_animal(animal)
        if lines:
            print("\n".join(lines))
            print()

    # 2) HTML erzeugen (Schritt 2)
    animals_li_items = []
    for animal in animals_data:
        if not isinstance(animal, dict):
            continue

        animal_li = build_animal_li(animal)
        if animal_li:
            animals_li_items.append(animal_li)

    template = read_template("animals_template.html")
    animals_html = "\n".join(animals_li_items)
    html_page = template.replace("__REPLACE_ANIMALS_INFO__", animals_html)
    write_html("animals.html", html_page)


if __name__ == "__main__":
    main()


