import pandas as pd


def apply_result_on_favorite(x):
    #     print(x.values)
    _result, _home, _draw, _away = x

    if (min(_home, _draw, _away) == _home) and (_result == 'H'):
        return 'H'
    elif (min(_home, _draw, _away) == _draw) and (_result == 'D'):
        return 'D'
    elif (min(_home, _draw, _away) == _away) and (_result == 'A'):
        return 'A'
    else:
        return 'OTHER'


def apply_result_on_dog(x):
    #     print(x.values)
    _result, _home, _draw, _away = x

    if (max(_home, _draw, _away) == _home) and (_result == 'H'):
        return 'H'
    elif (max(_home, _draw, _away) == _draw) and (_result == 'D'):
        return 'D'
    elif (max(_home, _draw, _away) == _away) and (_result == 'A'):
        return 'A'
    else:
        return 'OTHER'


def apply_results(match_info):
    # compute the match result (i.e Home win/Draw/Away win) from the goals data for the match
    match_info['RESULT'] = 'H'
    match_info.loc[match_info.HOME_TEAM_GOAL == match_info.AWAY_TEAM_GOAL, "RESULT"] = 'D'
    match_info.loc[match_info.HOME_TEAM_GOAL < match_info.AWAY_TEAM_GOAL, "RESULT"] = 'A'

    match_info.loc[:, 'ODDS_ON_HOME'] = match_info['HOME_ODDS']
    match_info.loc[:, 'ODDS_ON_FAVORITE'] = match_info[['HOME_ODDS', 'DRAW_ODDS', 'AWAY_ODDS']].min(axis=1)
    match_info.loc[:, 'ODDS_ON_DOG'] = match_info[['HOME_ODDS', 'DRAW_ODDS', 'AWAY_ODDS']].max(axis=1)

    # find the match outcome corresponding to the safest & riskiest odds
    match_info.loc[:, 'RESULT_ON_HOME'] = 'OTHER'
    match_info.loc[match_info.RESULT == 'H', 'RESULT_ON_HOME'] = 'H'

    match_info.loc[:, 'RESULT_ON_FAVORITE'] = match_info[['RESULT', 'HOME_ODDS', 'DRAW_ODDS', 'AWAY_ODDS']].apply(
        apply_result_on_favorite,
        axis='columns'
    )

    match_info.loc[:, 'RESULT_ON_DOG'] = match_info[['RESULT', 'HOME_ODDS', 'DRAW_ODDS', 'AWAY_ODDS']].apply(
        apply_result_on_dog,
        axis='columns'
    )
    return match_info


def apply_results_to_teams(match_info, teams):
    match_info.loc[:, 'BET_ON_TEAM'] = 'OTHER'
    match_info.loc[match_info.HOME_TEAM.isin(teams), 'BET_ON_TEAM'] = match_info.HOME_TEAM
    match_info.loc[match_info.AWAY_TEAM.isin(teams), 'BET_ON_TEAM'] = match_info.AWAY_TEAM

    match_info.loc[:, 'RESULT_ON_TEAM'] = 'OTHER'
    match_info.loc[
        (match_info.HOME_TEAM.isin(teams) & (match_info.RESULT == 'H')) |
        (match_info.AWAY_TEAM.isin(teams) & (match_info.RESULT == 'A')),
        'RESULT_ON_TEAM'] = match_info.RESULT

    match_info.loc[:, 'ODDS_ON_TEAM'] = 'OTHER'
    match_info.loc[(match_info.HOME_TEAM.isin(teams) & (match_info.RESULT == 'H')), 'ODDS_ON_TEAM'] = match_info.B365H
    match_info.loc[(match_info.AWAY_TEAM.isin(teams) & (match_info.RESULT == 'A')), 'ODDS_ON_TEAM'] = match_info.B365A

    return match_info