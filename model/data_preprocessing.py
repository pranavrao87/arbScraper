import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',1000)
pd.set_option('display.max_rows',1000)

# Column names for data
colNames = ['date','dblheader_code','day_of_week','team_v','league_v','game_no_v',
           'team_h','league_h','game_no_h', 'runs_v', 'runs_h','outs_total','day_night',
            'completion_info','forfeit_info','protest_info','ballpark_id','attendance','game_minutes',
            'linescore_v','linescore_h',
           'AB_v','H_v','2B_v','3B_v','HR_v','RBI_v','SH_v','SF_v','HBP_v','BB_v','IBB_v','SO_v',
            'SB_v', 'CS_v','GIDP_v','CI_v','LOB_v',
            'P_num_v','ERind_v','ERteam_v','WP_v','balk_v',
            'PO_v','ASST_v','ERR_v','PB_v','DP_v','TP_v',
           'AB_h', 'H_h', '2B_h', '3B_h', 'HR_h', 'RBI_h', 'SH_h', 'SF_h', 'HBP_h', 'BB_h', 'IBB_h','SO_h',
            'SB_h', 'CS_h', 'GIDP_h', 'CI_h', 'LOB_h',
            'P_num_h', 'ERind_h', 'ERteam_h', 'WP_h', 'balk_h',
            'PO_h', 'ASST_h', 'ERR_h', 'PB_h', 'DP_h', 'TP_h',
            'ump_HB_id', 'ump_HB_name','ump_1B_id', 'ump_1B_name','ump_2B_id', 'ump_2B_name',
            'ump_3B_id', 'ump_3B_name','ump_LF_id', 'ump_LF_name','ump_RF_id', 'ump_RF_name',
            'mgr_id_v', 'mgr_name_v', 'mgr_id_h', 'mgr_name_h',
            'pitcher_id_w','pitcher_name_w','pitcher_id_l','pitcher_name_l','pitcher_id_s','pitcher_name_s',
            'GWRBI_id','GWRBI_name','pitcher_start_id_v','pitcher_start_name_v','pitcher_start_id_h','pitcher_start_name_h',
            'batter1_name_v', 'batter1_id_v', 'batter1_pos_v', 'batter2_name_v', 'batter2_id_v', 'batter2_pos_v',
            'batter3_name_v', 'batter3_id_v', 'batter3_pos_v', 'batter4_name_v', 'batter4_id_v', 'batter4_pos_v',
            'batter5_name_v', 'batter5_id_v', 'batter5_pos_v', 'batter6_name_v', 'batter6_id_v', 'batter6_pos_v',
            'batter7_name_v', 'batter7_id_v', 'batter7_pos_v', 'batter8_name_v', 'batter8_id_v', 'batter8_pos_v',
            'batter9_name_v', 'batter9_id_v', 'batter9_pos_v', 'batter1_name_h', 'batter1_id_h', 'batter1_pos_h',
            'batter2_name_h', 'batter2_id_h', 'batter2_pos_h', 'batter3_name_h', 'batter3_id_h', 'batter3_pos_h',
            'batter4_name_h', 'batter4_id_h', 'batter4_pos_h', 'batter5_name_h', 'batter5_id_h', 'batter5_pos_h',
            'batter6_name_h', 'batter6_id_h', 'batter6_pos_h', 'batter7_name_h', 'batter7_id_h', 'batter7_pos_h',
            'batter8_name_h', 'batter8_id_h', 'batter8_pos_h', 'batter9_name_h', 'batter9_id_h', 'batter9_pos_h',           
           'misc_info','acqui_info'
           ]

df = pd.DataFrame()
for year in range(2010, 2025):
    file = "/Users/Prana/Documents/arbScraper/model/gl/gl" + str(year) + ".txt"
    df_temp = pd.read_csv(file, header=None)
    df_temp.columns = colNames
    df_temp['season'] = year
    df = pd.concat((df, df_temp))

# drop columns that don't matter
cols_to_drop = ['game_minutes', 'ballpark_id', 'attendance', 'ump_HB_id', 'ump_HB_name','ump_1B_id', 'ump_1B_name',
                'ump_2B_id', 'ump_2B_name','ump_3B_id', 'ump_3B_name','ump_LF_id', 'ump_LF_name','ump_RF_id', 'ump_RF_name',
                'pitcher_id_w','pitcher_name_w','pitcher_id_l','pitcher_name_l','pitcher_id_s','pitcher_name_s',
                'pitcher_start_id_v','pitcher_start_name_v','pitcher_start_id_h','pitcher_start_name_h',
                'mgr_id_v', 'mgr_name_v', 'mgr_id_h', 'mgr_name_h', 'batter4_name_h', 'batter4_id_h', 'batter4_pos_h',
                'batter1_name_v', 'batter1_id_v', 'batter1_pos_v', 'batter2_name_v', 'batter2_id_v', 'batter2_pos_v',
                'batter3_name_v', 'batter3_id_v', 'batter3_pos_v', 'batter4_name_v', 'batter4_id_v', 'batter4_pos_v',
                'batter5_name_v', 'batter5_id_v', 'batter5_pos_v', 'batter6_name_v', 'batter6_id_v', 'batter6_pos_v',
                'batter7_name_v', 'batter7_id_v', 'batter7_pos_v', 'batter8_name_v', 'batter8_id_v', 'batter8_pos_v',
                'batter9_name_v', 'batter9_id_v', 'batter9_pos_v', 'batter1_name_h', 'batter1_id_h', 'batter1_pos_h',
                'batter2_name_h', 'batter2_id_h', 'batter2_pos_h', 'batter3_name_h', 'batter3_id_h', 'batter3_pos_h',
                'batter4_name_h', 'batter4_id_h', 'batter4_pos_h', 'batter5_name_h', 'batter5_id_h', 'batter5_pos_h',
                'batter6_name_h', 'batter6_id_h', 'batter6_pos_h', 'batter7_name_h', 'batter7_id_h', 'batter7_pos_h',
                'batter8_name_h', 'batter8_id_h', 'batter8_pos_h', 'batter9_name_h', 'batter9_id_h', 'batter9_pos_h',
                'GWRBI_name', 'GWRBI_id', 'linescore_v','linescore_h']
df.drop(columns=cols_to_drop, inplace=True)

df['run_diff'] = df['runs_h']-df['runs_v']
df['home_victory'] = (df['run_diff']>0).astype(int)
df['run_total'] = df['runs_h'].copy()+df['runs_v'].copy()
df['date_dblhead'] = (df['date'].astype(str) + df['dblheader_code'].astype(str)).astype(int)

def strip_suffix(x, suff):
    if x.endswith(suff):
        return(x[:-len(suff)])
    else:
        return(x)

visit_cols = [col for col in df.columns if not col.endswith('_h')]
visit_cols_stripped = [strip_suffix(col,'_v') for col in visit_cols]
home_cols = [col for col in df.columns if not col.endswith('_v')]
home_cols_stripped = [strip_suffix(col,'_h') for col in home_cols]


def create_team_df(team):
    """
    Subsets the game level df by team in order to aggregate team statistics easily
    Also creates rolling sums for important statistics to represent the stats of a team up to the game, 
    but not including the game in question to set up training data for model to predict on
    """

    # all the away games of a team
    df_team_v = df[(df.team_v==team)]
    opponent = df_team_v['team_h']
    df_team_v = df_team_v[visit_cols]
    df_team_v.columns = visit_cols_stripped
    df_team_v['home_game'] = 0
    df_team_v['opponent'] = opponent

    # all the home games of a team
    df_team_h = df[(df.team_h==team)]
    opponent = df_team_h['team_v']
    df_team_h = df_team_h[home_cols]
    df_team_h.columns = home_cols_stripped
    df_team_h['home_game'] = 1
    df_team_h['opponent'] = opponent


    df_team = pd.concat((df_team_h, df_team_v))
    df_team.sort_values(['date', 'game_no'],inplace=True)
    
    for winsize in [162,30]: #162 games = 1 season worth of games
        suff = str(winsize)
        for raw_col in ['AB','H','2B','3B','HR','BB','runs','SB','CS','ERR']:
            new_col = 'rollsum_'+raw_col+'_'+suff
            df_team[new_col] = df_team[raw_col].rolling(winsize, closed='left').sum()

        # batting average = hits / at bat
        df_team['rollsum_BATAVG_'+suff] = df_team['rollsum_H_'+suff] / df_team['rollsum_AB_'+suff]

        # on base percentage = (hits + walks (base on balls)) / (at bats + walks) 
        df_team['rollsum_OBP_'+suff] = (df_team['rollsum_H_'+suff] + df_team['rollsum_BB_'+suff]) / (df_team['rollsum_AB_'+suff]+df_team['rollsum_BB_'+suff])

        # slugging percentage: total bases a player earns per at-bat
        # (hits + second base * 2 + third base * 3 + home runs * 4) / at bats
        df_team['rollsum_SLG_'+suff] = (df_team['rollsum_H_'+suff] + df_team['rollsum_2B_'+suff] * 2 + df_team['rollsum_3B_'+suff] * 3 + df_team['rollsum_HR_'+suff] * 4) / (df_team['rollsum_AB_'+suff])

        # cumulative sum of slugging percentages
        df_team['rollsum_OBS_'+suff] = df_team['rollsum_OBP_'+suff] + df_team['rollsum_SLG_'+suff]
    
    df_team['season_game'] = df_team['season']*1000 + df_team['game_no']
    df_team.set_index('season_game', inplace=True)
    return(df_team)

team_data_dict = {}
for team in df.team_v.unique():
    team_data_dict[team] = create_team_df(team)

# list of all stat names and time windows
stats = ['BATAVG', 'OBP', 'SLG', 'OBS', 'SB', 'CS', 'ERR']
windows = ['162', '30']
sides = ['h', 'v'] 

# init all arrays in a dictionary
stat_arrays = {
    f'{stat}_{window}_{side}': np.zeros(df.shape[0])
    for stat in stats for window in windows for side in sides
}

# loop through each row and populate values
i = 0
for _, row in df.iterrows():
    home_team = row['team_h']
    visit_team = row['team_v']
    game_index_h = row['season'] * 1000 + row['game_no_h']
    game_index_v = row['season'] * 1000 + row['game_no_v']

    for stat in stats:
        for window in windows:
            colname = f'rollsum_{stat}_{window}'
            stat_arrays[f'{stat}_{window}_h'][i] = team_data_dict[home_team].loc[game_index_h, colname]
            stat_arrays[f'{stat}_{window}_v'][i] = team_data_dict[visit_team].loc[game_index_v, colname]
    i += 1

# add arrays back to dataframe
for key, arr in stat_arrays.items():
    df[key] = arr

df = df[df.run_diff != 0] # drop tie games from dataset b/c doesn't count as victory or loss

# Adding odds data to main dataframe

# Data only has odds ranging from 2012 - 2021
odds_df = pd.read_csv("/Users/Prana/Documents/arbScraper/model/oddsDataMLB.csv")

# odds_df and the main_df have diff abbreviations so convert odds_df abbreviations to match 
abbreviation_map = {
    'ARI': 'ARI',
    'ATL': 'ATL',
    'BAL': 'BAL',
    'BOS': 'BOS',
    'CHC': 'CHN',  # Chicago Cubs
    'CIN': 'CIN',
    'CLE': 'CLE',
    'COL': 'COL',
    'CWS': 'CHA',  # Chicago White Sox
    'DET': 'DET',
    'HOU': 'HOU',
    'KC':  'KCA',  # Kansas City Royals
    'LAA': 'ANA',  # Los Angeles Angels
    'LAD': 'LAN',  # Los Angeles Dodgers
    'MIA': 'MIA', 
    'MIL': 'MIL',
    'MIN': 'MIN',
    'NYM': 'NYN',  # New York Mets
    'NYY': 'NYA',  # New York Yankees
    'OAK': 'OAK',
    'PHI': 'PHI',
    'PIT': 'PIT',
    'SD':  'SDN',  # San Diego Padres
    'SEA': 'SEA',
    'SF':  'SFN',  # San Francisco Giants
    'STL': 'SLN',  # St Louis Cardinals
    'TB':  'TBA',  # Tampa Bay Rays
    'TEX': 'TEX',
    'TOR': 'TOR',
    'WSH': 'WAS'   # Washington Nationals
}
odds_df["team"] = odds_df["team"].map(abbreviation_map)
odds_df["opponent"] = odds_df["opponent"].map(abbreviation_map)

# Start merging odds data database with original game data database to make it easier to train/evaluate model
df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
odds_df['date'] = pd.to_datetime(odds_df['date'])


# Only merging ML for home/visiting teams for now can also merge o/u lines later
df['merge_key_home'] = (
    df['date'].astype(str) + '_' +
    df['team_h'] + '_' + df['team_v']
)

df['merge_key_away'] = (
    df['date'].astype(str) + '_' +
    df['team_v'] + '_' + df['team_h']
)

odds_df['merge_key'] = (
    odds_df['date'].astype(str) + '_' +
    odds_df['team'] + '_' + odds_df['opponent']
)

df = df.merge(
    odds_df[['merge_key', 'moneyLine']].rename(columns={'moneyLine': 'ML_h'}),
    left_on='merge_key_home',
    right_on='merge_key',
    how='left'
).merge(
    odds_df[['merge_key', 'moneyLine']].rename(columns={'moneyLine': 'ML_v'}),
    left_on='merge_key_away',
    right_on='merge_key',
    how='left',
    suffixes=('', '_away')
)

df.drop(columns=["merge_key_home", "merge_key_away", "merge_key"], inplace=True)


def americanToProb(odds):
    if pd.isna(odds):
        return None
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)

df["imp_prob_h"] = df["ML_h"].apply(americanToProb)
df["imp_prob_v"] = df["ML_v"].apply(americanToProb)
df["imp_prob_mid_h"] = (df["imp_prob_h"] + (1 - df["imp_prob_v"])) / 2

df.to_csv('df_bp1.csv', index=False)