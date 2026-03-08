import pandas as pd

from betalytics.soccer.finance_management.all import apply_finance_strategy


def get_stats_from_matches(match_info, need_print=False):
    if match_info.shape[0] == 0:
        return None, None, None
    percent_on_home = match_info[~(match_info.PAYOUT_ON_HOME == 0)].shape[0] / float(match_info.shape[0])
    percent_on_favorite = match_info[~(match_info.PAYOUT_ON_FAVORITE == 0)].shape[0] / float(match_info.shape[0])
    percent_on_dog = match_info[~(match_info.PAYOUT_ON_DOG == 0)].shape[0] / float(match_info.shape[0])

    investment_on_home = match_info.STAKE_ON_HOME.sum()
    investment_on_favorite = match_info.STAKE_ON_FAVORITE.sum()
    investment_on_dog = match_info.STAKE_ON_DOG.sum()

    roi_on_home = sum(match_info.PAYOUT_ON_HOME)
    roi_on_favorite = sum(match_info.PAYOUT_ON_FAVORITE)
    roi_on_dog = sum(match_info.PAYOUT_ON_DOG)
    # calculate percantage reduction error what we stake vs earcn in %
    pre_on_home = (roi_on_home - investment_on_home) / investment_on_home * 100
    pre_on_favorite = (roi_on_favorite - investment_on_favorite) / investment_on_favorite * 100
    pre_on_dog = (roi_on_dog - investment_on_dog) / investment_on_dog * 100
    if need_print:
        print (
        "Correct bets for home={} | favorite={} | dog={}".format(percent_on_home, percent_on_favorite, percent_on_dog))
        # print ("Net investment:", net_investment)
        print ("ROI for home={} | favorite={} | dog={}".format(roi_on_home, roi_on_favorite, roi_on_dog))
        print ("PRE for home={} | favorite={} | dog={}:".format(pre_on_home, pre_on_favorite, pre_on_dog))
    return pre_on_home, pre_on_favorite, pre_on_dog


def generate_stats_over_all_seasons(match_info, strategy):
    profitablity = {}
    stats_on_home = {}
    stats_on_favorite = {}
    stats_on_dog = {}

    for league in match_info['LEAGUE'].unique():
        for season in match_info['SEASON'].unique():
            #         print('Processing -> {} - {}'.format(league, season))
            match_df = match_info[
                (match_info['LEAGUE'] == league) &
                (match_info['SEASON'] == season)
                ]
            match_df = apply_finance_strategy(match_df, strategy=strategy)
            on_home, on_favorite, on_dog = get_stats_from_matches(match_df)
            profitablity.setdefault(league, {}).setdefault(
                season,
                {
                    'BET_ON_HOME': on_home,
                    'BET_ON_FAVORITE': on_favorite,
                    'BET_ON_DOG': on_dog
                }
            )
            stats_on_home.setdefault(league, {}).setdefault(season, on_home)
            stats_on_favorite.setdefault(league, {}).setdefault(season, on_favorite)
            stats_on_dog.setdefault(league, {}).setdefault(season, on_dog)

    return profitablity, stats_on_home, stats_on_favorite, stats_on_dog


def get_standings_table(matches, n_teams=15):
    home_standings = matches[['HOME_TEAM', 'RESULT']].groupby(by=['HOME_TEAM', 'RESULT']).size().unstack(fill_value=0)
    home_standings.loc[:, 'HOME_SCORE'] = home_standings[['H', 'D', 'A']].apply(lambda x: x[0] * 3 + x[1],
                                                                                axis='columns')
    home_standings.loc[:, 'HOME_MAX_SCORE'] = home_standings[['H', 'D', 'A']].apply(
        lambda x: x[0] * 3 + x[1] * 3 + x[2] * 3, axis='columns')
    away_standings = matches[['AWAY_TEAM', 'RESULT']].groupby(by=['AWAY_TEAM', 'RESULT']).size().unstack(fill_value=0)
    away_standings.loc[:, 'AWAY_SCORE'] = away_standings[['H', 'D', 'A']].apply(lambda x: x[2] * 3 + x[1],
                                                                                axis='columns')
    away_standings.loc[:, 'AWAY_MAX_SCORE'] = away_standings[['H', 'D', 'A']].apply(
        lambda x: x[0] * 3 + x[1] * 3 + x[2] * 3, axis='columns')

    standings = pd.concat([home_standings, away_standings], axis='columns')
    standings.loc[:, 'SCORE'] = standings['HOME_SCORE'] + standings['AWAY_SCORE']
    standings.loc[:, 'MAX_SCORE'] = standings['HOME_MAX_SCORE'] + standings['AWAY_MAX_SCORE']
    standings.loc[:, 'WIN_RATE'] = standings['SCORE'] / standings['MAX_SCORE']
    standings = standings.sort_values(by='WIN_RATE', ascending=False).head(n_teams)

    return standings
