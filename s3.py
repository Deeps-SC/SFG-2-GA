import xml.etree.ElementTree as ET
from copy import deepcopy

def inject_matching_schedule_into_producer_xml(producer_xml_str, schedules_xml_str):
    # Parse XML from string inputs
    producer_root = ET.fromstring(producer_xml_str)
    schedules_root = ET.fromstring(schedules_xml_str)

    # Get scux_user_id from producer XML
    scux_elem = producer_root.find('.//scux_user_id')
    if scux_elem is None or not scux_elem.text:
        print("❌ scux_user_id not found.")
        return producer_xml_str

    scux_user_id = scux_elem.text.strip().lower()

    # Loop through all SCHEDULE entries in the schedules XML
    for schedule_elem in schedules_root.findall('.//SCHEDULE'):
        mailbox = extract_producermailbox_from_schedule(schedule_elem)
        if mailbox:
            mailbox_clean = mailbox.strip().strip('/').lower()
            if mailbox_clean == scux_user_id:
                print(f"✅ Match found for SCUX ID: {scux_user_id}")
                producer_elem = producer_root.find('.//producer')
                if producer_elem is not None:
                    schedule_copy = deepcopy(schedule_elem)
                    producer_elem.append(schedule_copy)
                return ET.tostring(producer_root, encoding='unicode')

    print(f"❌ No matching schedule found for SCUX ID: {scux_user_id}")
    return producer_xml_str
