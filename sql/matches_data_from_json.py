
def matches_data_2026_from_json(full_match_data:dict) -> list:
    red_score_data=full_match_data['score_breakdown']['red']
    blue_score_data=full_match_data['score_breakdown']['blue']
    red_score_data.update(red_score_data['hubScore'])
    blue_score_data.update(blue_score_data['hubScore'])

    red_dict={
        'match_key':full_match_data['key'],
        'alliance':'red',
        'event_key':full_match_data.get('event_key'),
        'total_score':red_score_data.get('totalPoints'),
        'teleop_count':red_score_data.get('teleopCount'),
        'auto_points':red_score_data.get('autoPoints'),
        'transition_points':red_score_data.get('transitionPoints'),
        'uncounted_points':red_score_data.get('uncounted'),
        'teleop_points':red_score_data.get('teleopPoints'),
        'shift1_points':red_score_data.get('shift1Points'),
        'shift2_points':red_score_data.get('shift2Points'),
        'shift3_points':red_score_data.get('shift3Points'),
        'shift4_points':red_score_data.get('shift4Points'),
        'endgame_points':red_score_data.get('endgamePoints'),
        'total_auto_points':red_score_data.get('autoPoints'),
        'auto_tower_points':red_score_data.get('autoTowerPoints'),
        'end_game_tower_points':red_score_data.get('endGameTowerPoints'),
        'total_tower_points':red_score_data.get('totalTowerPoints'),
        'minor_foul_count':red_score_data.get('minorFoulCount'),
        'major_foul_count':red_score_data.get('majorFoulCount'),
        'foul_points':red_score_data.get('foulPoints'),
        'adjust_points':red_score_data.get('adjustPoints'),
        'ranking_points':red_score_data.get('rp'),    
        }
    blue_dict={
        'match_key':full_match_data['key'],
        'alliance':'blue',
        'event_key':full_match_data.get('event_key'),
        'total_score':blue_score_data.get('totalPoints'),
        'teleop_count':blue_score_data.get('teleopCount'),
        'auto_points':blue_score_data.get('autoPoints'),
        'transition_points':blue_score_data.get('transitionPoints'),
        'uncounted_points':blue_score_data.get('uncounted'),
        'teleop_points':blue_score_data.get('teleopPoints'),
        'shift1_points':blue_score_data.get('shift1Points'),
        'shift2_points':blue_score_data.get('shift2Points'),
        'shift3_points':blue_score_data.get('shift3Points'),
        'shift4_points':blue_score_data.get('shift4Points'),
        'endgame_points':blue_score_data.get('endgamePoints'),
        'total_auto_points':blue_score_data.get('autoPoints'),
        'auto_tower_points':blue_score_data.get('autoTowerPoints'),
        'end_game_tower_points':blue_score_data.get('endGameTowerPoints'),
        'total_tower_points':blue_score_data.get('totalTowerPoints'),
        'minor_foul_count':blue_score_data.get('minorFoulCount'),
        'major_foul_count':blue_score_data.get('majorFoulCount'),
        'foul_points':blue_score_data.get('foulPoints'),
        'adjust_points':blue_score_data.get('adjustPoints'),
        'ranking_points':blue_score_data.get('rp'),
        }

    video_data=full_match_data.get('videos')
    if len(video_data) > 0:
        video_data_write=video_data[0]
        blue_dict |= {'video_key':video_data_write['key'],'video_type':video_data_write['type']}
        red_dict |= {'video_key':video_data_write['key'],'video_type':video_data_write['type']}

    return[red_dict,blue_dict]

