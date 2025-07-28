import xml.etree.ElementTree as ET

def extract_producermailbox_from_schedule(schedule_elem):
    """Parses the CDATA in <SCHEDULE_PARAMS> to extract producermailbox."""
    params_elem = schedule_elem.find('SCHEDULE_PARAMS')
    if params_elem is not None and params_elem.text:
        try:
            inner_root = ET.fromstring(params_elem.text.strip())
            for param in inner_root.findall('.//{*}Parameter'):
                name = param.findtext('{*}name')
                value = param.findtext('{*}value')
                if name and name.lower() == 'producermailbox':
                    return value.strip()
        except ET.ParseError as e:
            print(f"Failed to parse SCHEDULE_PARAMS CDATA: {e}")
    return None

def inject_schedule_for_producer(schedules_xml_str, producer_xml_str) -> str:
    # Parse both XMLs
    schedules_root = ET.fromstring(schedules_xml_str)
    producer_root = ET.fromstring(producer_xml_str)
    
    # Extract scux_user_id from producer XML
    producer_elem = producer_root.find('.//producer')
    scux_user_id_elem = producer_elem.find('scux_user_id')
    if scux_user_id_elem is None or not scux_user_id_elem.text:
        print("No scux_user_id found in producer XML")
        return producer_xml_str
    scux_user_id = scux_user_id_elem.text.strip().lower()

    # Search for matching schedule
    matching_schedule = None
    schedules_elem = schedules_root.find('SCHEDULES')
    if schedules_elem is not None:
        for schedule in schedules_elem.findall('SCHEDULE'):
            mailbox = extract_producermailbox_from_schedule(schedule)
            if mailbox and mailbox.strip('/').lower() == scux_user_id:
                matching_schedule = schedule
                break  # stop at first match

    # Inject into producer XML
    if matching_schedule is not None:
        schedules_container = ET.Element('schedules')
        schedules_container.append(matching_schedule)
        producer_elem.append(schedules_container)
        print(f"Injected schedule for producer {scux_user_id}")
    else:
        print(f"No matching schedule found for producer {scux_user_id}")

    # Return updated XML string
    return ET.tostring(producer_root, encoding='unicode')
