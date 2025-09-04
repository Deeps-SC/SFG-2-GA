# validator.py

import xml.etree.ElementTree as ET
from keymap import normalize_key

def parse_producer_xml(file_path: str) -> dict:
    """
    Parse producer XML (flat structure).
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = {}
    for elem in root:
        if elem.text and elem.text.strip():
            data[elem.tag] = elem.text.strip()
    return data


def parse_export_xml(file_path: str) -> dict:
    """
    Parse export XML (nested structure).
    Returns dict: {section: {key: value}}
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    export_data = {}
    for section in root:
        section_name = section.tag
        export_data[section_name] = {}
        for elem in section:
            if elem.text and elem.text.strip():
                export_data[section_name][elem.tag] = elem.text.strip()
    return export_data


def validate(producer_file: str, export_file: str):
    producer_data = parse_producer_xml(producer_file)
    export_data = parse_export_xml(export_file)

    results = []

    for section, kvs in export_data.items():
        for key, value in kvs.items():
            normalized_key = normalize_key(section, key)
            if normalized_key in producer_data:
                if producer_data[normalized_key] == value:
                    results.append((section, key, "match"))
                else:
                    results.append((section, key, "mismatch"))
            else:
                results.append((section, key, "not_found"))

    return results


if __name__ == "__main__":
    producer_file = "sample_producer.xml"
    export_file = "sample_export.xml"

    results = validate(producer_file, export_file)

    print("\nValidation Results:")
    for section, key, status in results:
        print(f"[{section}] {key}: {status}")
