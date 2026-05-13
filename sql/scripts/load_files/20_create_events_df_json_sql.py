from pathlib import Path
import pandas as pd
import json


from sql.write_df_to_sql import write_df_to_postgres
from sql.get_keys_from_table import get_keys_from_table_schema_set
from config import REPO_ROOT, SCHEMA
from sql.get_district_from_state_country import get_district_key_from_state_country


EVENTS_FOLDER = REPO_ROOT / 'api' / 'json' / 'events_data'
SAVE_PATH = REPO_ROOT / 'sql' / 'jsons_of_sql_tables'/ 'events_in_frc.json'


existing_event_keys_set = get_keys_from_table_schema_set("event_key","events", SCHEMA)


event_list_for_conv_df = []
event_files = [p.name for p in Path(EVENTS_FOLDER).iterdir() if p.is_file()]
for file_name in event_files:
        loop_path = EVENTS_FOLDER / file_name
        with open(loop_path) as loop_file:
              loop_data = json.load(loop_file)
        for events_entry in loop_data:
                loop_event_key = events_entry['key']
                year = int(events_entry.get('key')[:4]) if len(events_entry.get('key')) > 4 else None
                state_prov = events_entry.get('state_prov')
                country = events_entry.get('country')
                if loop_event_key not in existing_event_keys_set:
                    event_list_for_conv_df.append({
                        'event_key':loop_event_key,
                        'year': year,
                        'event':str(events_entry.get('name')),
                        'event_type':str(events_entry.get('event_type')),
                        'event_code':str(events_entry.get('event_code')),
                        'date': pd.Timestamp(events_entry.get('start_date')) if events_entry.get('start_date') else None,
                        'location':events_entry.get('location_name'),
                        'webcast':f"youtube.com/watch?v={events_entry.get('webcasts')[0].get('channel')}" if len(events_entry.get('webcasts')) else None,
                        'week':events_entry.get('week'),
                        'district_key':events_entry.get('district').get('key') if events_entry.get('district') else get_district_key_from_state_country(state_prov,country,year),
                        'state_prov':state_prov,
                        'country':country,
                            })
                existing_event_keys_set.add(loop_event_key)
                
event_df = pd.DataFrame(event_list_for_conv_df)
event_json = event_df.to_json(SAVE_PATH, orient = 'records', indent = 2, date_format='iso')

write_df_to_postgres(event_df, 'events', if_exists = "append", schema = SCHEMA)


