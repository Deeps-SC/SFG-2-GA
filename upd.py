import xml.etree.ElementTree as ET
import re

def extract_producermailbox_from_schedule(schedule_elem, ns):
    sched_params_elem = schedule_elem.find(f'{ns}SCHEDULE_PARAMS')
    if sched_params_elem is None or not sched_params_elem.text:
        return None

    try:
        cdata_text = sched_params_elem.text.strip()

        # Remove XML declaration if present
        if cdata_text.startswith('<?xml'):
            cdata_text = cdata_text[cdata_text.find('?>') + 2:].strip()

        # Parse the inner CDATA XML
        cdata_root = ET.fromstring(cdata_text)

        # Get namespace from CDATA root
        cdata_ns = re.match(r'\{.*\}', cdata_root.tag)
        inner_ns = cdata_ns.group(0) if cdata_ns else ''

        # Loop through <Parameter> elements
        for param in cdata_root.findall(f".//{inner_ns}Parameter"):
            name_elem = param.find(f"{inner_ns}name")
            value_elem = param.find(f"{inner_ns}value")

            if name_elem is not None and value_elem is not None:
                if name_elem.text.strip().lower() == 'producermailbox':
                    return value_elem.text.strip()

    except ET.ParseError as e:
        print(f"[CDATA Parse Error]: {e}")

    return None

