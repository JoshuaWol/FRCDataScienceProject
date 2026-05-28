from sql.get_keys_from_table import get_keys_from_table_schema_set
from config import SCHEMA

state_district_dict = {
    'PA': 'fma',
    'CA': 'ca',
    'WI': 'win',
    'WA': 'pnw',
    'OR': 'pnw',
    'GA': 'pch',
    'ON': 'ont',
    'MD': 'fch',
    'VA': 'fch',
    'MI': 'fim',
    'NM': 'fit',
    "IN": 'fin',
    'DE': 'fma',
    'NJ': 'fma',
    'NC': 'fnc',
    'SC': 'fsc',
    'MA': 'ne',
    'CT': 'ne',
    'ME': 'ne',
    'VT': 'ne',    
}

country_district_dict = {
    "Isreal": 'isr'
}
existing_district_keys_set = get_keys_from_table_schema_set("district_key","districts", SCHEMA)

def get_district_key_from_state_country(state:str = None, country:str = None, year:str | int = None) ->str:
    returnstr = None
    if state in state_district_dict:
        returnstr =  str(year) + state_district_dict[state]
    elif country in country_district_dict:
        returnstr = str(year) + country_district_dict[country]
    if returnstr in existing_district_keys_set:
        return returnstr