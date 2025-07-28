import xml.etree.ElementTree as ET

def extract_producermailbox_from_schedule(schedule_elem):
    params_elem = schedule_elem.find('SCHEDULE_PARAMS')
    if params_elem is not None and params_elem.text:
        cdata = params_elem.text.strip()
        try:
            # Parse the CDATA XML
            cdata_root = ET.fromstring(cdata)

            # Dynamically get the namespace
            namespace_uri = cdata_root.tag.split('}')[0].strip('{')
            ns = {'ns': namespace_uri}

            # Loop through all <Parameter> elements
            for param in cdata_root.findall('.//ns:Parameter', ns):
                name_elem = param.find('ns:name', ns)
                value_elem = param.find('ns:value', ns)
                if name_elem is not None and name_elem.text.strip().lower() == 'producermailbox':
                    return value_elem.text.strip()
        except ET.ParseError as e:
            print(f"[WARN] Failed to parse CDATA for a schedule: {e}")
    return None




# scux_user_id comes from producer XML
for schedule_elem in all_schedule_elements:
    mailbox = extract_producermailbox_from_schedule(schedule_elem)
    if mailbox:
        mailbox_clean = mailbox.strip().strip('/').lower()
        scux_clean = scux_user_id.strip().lower()

        if mailbox_clean == scux_clean:
            # 🎯 Found the matching schedule for the producer
            return schedule_elem
