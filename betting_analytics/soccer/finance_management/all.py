import numpy as np
import pandas as pd



def _apply_on_bank(match_info):
    for pref in ['STAKE_', 'PAYOUT_']:
        for suff in ['ON_HOME', 'ON_FAVORITE', 'ON_DOG']:
            match_info[pref + suff] = 0.0
    match_info['BANK'] = -1.0
    for col in ['ON_HOME', 'ON_FAVORITE', 'ON_DOG']:
        cols = ['RESULT_{}'.format(col), 'ODDS_{}'.format(col),
                'STAKE_{}'.format(col), 'PAYOUT_{}'.format(col)]
        vals = match_info[['RESULT'] + cols].values
        #     print(vals.shape)
        BANK, BANK_PERCENTAGE = 1000, 0.01
        for iRow in range(len(vals)):
            _stake = BANK * BANK_PERCENTAGE
            vals[iRow][3] = _stake
            vals[iRow][4] = float(np.where(
                vals[iRow][0] == vals[iRow][1],
                vals[iRow][2] * vals[iRow][3],
                0
            ))
            BANK = BANK - _stake + vals[iRow][4]
            #     print(len(cols), match_info[cols].shape, vals[:, 1:].shape)
        match_info.loc[:, cols] = vals[:, 1:]

    return match_info


def apply_finance_strategy(match_info, strategy='FLAT'):
    if strategy == 'BANK':
        match_info = _apply_on_bank(match_info)
    else:
        FLAT_STAKE = 10
        DESIRE_PROFIT = 20
        if strategy == 'FLAT':
            match_info['STAKE_ON_HOME'] = FLAT_STAKE
            match_info['STAKE_ON_FAVORITE'] = FLAT_STAKE
            match_info['STAKE_ON_DOG'] = FLAT_STAKE
        else:
            match_info['STAKE_ON_HOME'] = float(DESIRE_PROFIT) / (match_info.ODDS_ON_HOME - 1)
            match_info['STAKE_ON_FAVORITE'] = float(DESIRE_PROFIT) / (match_info.ODDS_ON_FAVORITE - 1)
            match_info['STAKE_ON_DOG'] = float(DESIRE_PROFIT) / (match_info.ODDS_ON_DOG - 1)

        match_info['PAYOUT_ON_HOME'] = match_info.ODDS_ON_HOME * match_info.STAKE_ON_HOME
        match_info.loc[~(match_info.RESULT_ON_HOME == match_info.RESULT), 'PAYOUT_ON_HOME'] = 0

        match_info['PAYOUT_ON_FAVORITE'] = match_info.ODDS_ON_FAVORITE * match_info.STAKE_ON_FAVORITE
        match_info.loc[~(match_info.RESULT_ON_FAVORITE == match_info.RESULT), 'PAYOUT_ON_FAVORITE'] = 0

        match_info['PAYOUT_ON_DOG'] = match_info.ODDS_ON_DOG * match_info.STAKE_ON_DOG
        match_info.loc[~(match_info.RESULT_ON_DOG == match_info.RESULT), 'PAYOUT_ON_DOG'] = 0

    return match_info