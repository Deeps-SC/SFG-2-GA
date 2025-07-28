with open('schedules.xml') as f1, open('producer.xml') as f2:
    schedules_xml = f1.read()
    producer_xml = f2.read()

updated_producer_xml = inject_schedule_for_producer(schedules_xml, producer_xml)

with open('updated_producer.xml', 'w') as fout:
    fout.write(updated_producer_xml)
