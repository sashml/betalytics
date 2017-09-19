import sqlite3

import pandas as pd

from betting_analytics.soccer.const import BOOKIE, MATCH_INFO


def load_data(db_file_name):
    with sqlite3.connect(db_file_name) as con:
        all_data = pd.read_sql_query("SELECT * FROM Match", con)

    all_data.columns = [col.upper() for col in all_data.columns]
    return all_data


def load_and_normalize_data(db_file_name, bookie='BET365'):
    match_info = load_data(db_file_name)

    columns_to_rename = {
        'HOMETEAM': 'HOME_TEAM',
        'AWAYTEAM': 'AWAY_TEAM',
        'FTHG': 'HOME_TEAM_GOAL',
        'FTAG': 'AWAY_TEAM_GOAL',
        'FTR': 'RESULT'
    }
    columns_to_rename.update(BOOKIE[bookie])

    match_info = match_info[MATCH_INFO + BOOKIE[bookie].keys()].rename(columns=columns_to_rename)

    match_info = match_info.sort_values(by='DATE', ascending=True)
    print('Dataset[Full] Shape = {}'.format(match_info.shape))
    match_info = match_info.dropna()
    match_info = match_info[
        (match_info.HOME_ODDS >= 1.0) &
        (match_info.DRAW_ODDS >= 1.0) &
        (match_info.AWAY_ODDS >= 1.0)
        ]

    match_info.loc[:, 'LEAGUE'] = match_info['COUNTRY'] + '.' + match_info['LEAGUE']
    match_info.loc[:, 'HOME_TEAM'] = match_info['DIV'] + '.' + match_info['HOME_TEAM']
    match_info.loc[:, 'AWAY_TEAM'] = match_info['DIV'] + '.' + match_info['AWAY_TEAM']

    print('Dataset[DropNA] Shape = {}'.format(match_info.shape))

    return match_info

