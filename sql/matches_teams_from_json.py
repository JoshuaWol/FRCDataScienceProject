def matches_teams_from_json(full_match_data:dict) -> list:                
    red_teams = full_match_data['alliances']['red']['team_keys']
    blue_teams = full_match_data['alliances']['blue']['team_keys']
    match_key = full_match_data['key']
    matches_teams_list = []

    for team_key in red_teams:
        matches_teams_list.append({
            
            'match_key' : match_key,
            'team_key' : team_key,
            'alliance' : 'blue',
        })
    for team_key in blue_teams:
        matches_teams_list.append({
            'match_key' : match_key,
            'team_key' : team_key,
            'alliance' : 'blue',
        })

    return matches_teams_list