def extract_producermailbox_from_schedule(schedule_elem):
    params_elem = schedule_elem.find('SCHEDULE_PARAMS')
    if params_elem is not None and params_elem.text:
        cdata = params_elem.text.strip()
        print("\n📦 Raw CDATA:")
        print(cdata)

        try:
            cdata_root = ET.fromstring(cdata)
            print("✅ Parsed CDATA root tag:", cdata_root.tag)

            # Show child tags
            for child in cdata_root:
                print("  🔍 Child tag:", child.tag)

            # Extract namespace
            namespace_uri = cdata_root.tag.split('}')[0].strip('{')
            ns = {'ns': namespace_uri}
            print("📛 Namespace extracted:", namespace_uri)

            for param in cdata_root.findall('.//ns:Parameter', ns):
                name_elem = param.find('ns:Name', ns)
                value_elem = param.find('ns:Value', ns)

                print("➡️ Found Parameter block:")
                print("   Name:", name_elem.text.strip() if name_elem is not None else "None")
                print("   Value:", value_elem.text.strip() if value_elem is not None else "None")

                if (
                    name_elem is not None and name_elem.text.strip().lower() == 'producermailbox'
                    and value_elem is not None
                ):
                    return value_elem.text.strip()
        except ET.ParseError as e:
            print(f"⚠️ Failed to parse CDATA: {e}")
    else:
        print("❌ No SCHEDULE_PARAMS or it is empty.")
    return None
