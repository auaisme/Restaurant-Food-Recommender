
import csv
import json
import os

ERRORS = {
    0: "No Errors",
    1: "Failed Executing Main Error; Name is not \'__main__\'",
}

def csv_to_combo_format(csv_path, json_output_path = False):
    combos = []

    json_output_path = json_output_path or (os.path.splitext(csv_path)[0] + ".json")

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        # The first header is assumed to be the name
        name_field = headers[0]
        vector_fields = headers[1:]  # everything after name is part of vector

        for row in reader:
            combo_id = row[name_field]
            components = []
            vector = []

            for field in vector_fields:
                value = row[field].strip()

                # Handle numeric values in the vector
                try:
                    num = float(value)
                    vector.append(num)
                    if num > 0 and not field.lower() == 'price':
                        components.append(f"{int(num)} {field}" if num != 1 else field)
                except ValueError:
                    vector.append(value)  # e.g., if price is not numeric

            combos.append({
                "combo_id": combo_id,
                "components": components,
                "vector": vector
            })

    # Write to JSON file
    with open(json_output_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(combos, jsonfile, indent=2)
    return combos

def main():
    print("Executing Main")
    if __name__ != "__main__":
        return 1
    # do stuff
    csv_path = 'test_menu_1.csv'
    combos = csv_to_combo_format(csv_path)

    # Pretty print the result
    print(json.dumps(combos, indent=2))
    return 0

error_code = main()

print(ERRORS[error_code])