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
    'PA': 'fma',
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

def get_district_key_from_state_country(state:str = None, country:str = None, year:str | int = None) ->str:
    if state in state_district_dict:
        return str(year) + state_district_dict[state]
    elif country in country_district_dict:
        return str(year) + country_district_dict[country]
    print(state)