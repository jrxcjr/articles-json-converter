import json

def read_entries(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        entries = file.read().split('\n\n')
    return entries

def extract_values(entry):
    values = {}
    lines = entry.split('\n')
    current_key = None
    for line in lines:
        if line.strip():
            if '-' in line:
                key, value = line.split('-', 1)
                current_key = key.strip()
                if current_key == 'AU' or current_key == 'KW':
                    values.setdefault(current_key, []).append(value.strip())
                else:
                    values[current_key] = value.strip()
            elif current_key == 'AU' or current_key == 'KW':
                values[current_key][-1] += ' ' + line.strip()
            else:
                values[current_key] += ' ' + line.strip()
    return values

def write_to_json(entries, json_path):
    data = []
    current_kw_value = None

    for entry in entries:
        values = extract_values(entry)

        if 'KW' in values:
            current_kw_value = values['KW']
            del values['KW']

        if current_kw_value is not None:
            values['KW'] = current_kw_value

        data.append(values)

    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import re

    input_file = "phase_2_revisao_sistematica.txt"
    output_json = "output.json"

    entries = read_entries(input_file)
    write_to_json(entries, output_json)


