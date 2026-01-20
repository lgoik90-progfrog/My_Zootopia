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


def main():
    animals_data = load_data("animals_data.json")
    if not isinstance(animals_data, list):
        print("Fehler: animals_data.json muss eine Liste von Tieren enthalten.")
        return

    for animal in animals_data:
        if not isinstance(animal, dict):
            continue

        lines = format_animal(animal)
        if lines:
            print("\n".join(lines))
            print()


if __name__ == "__main__":
    main()
