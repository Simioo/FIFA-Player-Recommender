position_ord_map = {'GK': 0, 'CB': 1, 'LCB': 1, 'RCB': 1, 'LB': 2, 'LWB': 2, 'RB': 3, 'RWB': 3, 'CDM': 4,
                    'LDM': 4, 'RDM': 4, 'CM': 5, 'LCM': 5, 'RCM': 5, 'CAM': 6, 'LAM': 6, 'RAM': 6,
                    'LW': 7, 'LM': 7, 'RW': 7, 'RM': 7, 'CF': 7, 'RF': 7, 'LF': 7, 'ST': 7,
                    'RS': 7, 'LS': 7}

all_positions = ['CAM', 'CB', 'CDM', 'CF', 'CM', 'LAM', 'LB', 'LCB', 'LCM', 'LDM', 'LF', 'LM', 'LS', 'LW',
                 'LWB', 'RAM', 'RB', 'RCB', 'RCM', 'RDM', 'RF', 'RM', 'RS', 'RW', 'RWB', 'ST']

irrelevant_columns = ['Unnamed: 0', 'ID', 'Photo', 'Flag', 'Club Logo', 'Real Face', 'Jersey Number', 'Joined',
                      'Loaned From', 'Contract Valid Until', 'Club', 'Nationality', 'Release Clause']

gk_ratings_columns = ['GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes']

columns_to_skip_scaling = ['Name', 'Preferred Foot', 'Body Type', 'Att work rate', 'Def work rate', 'Position', 'Overall']


# Lists of irrelevant positions for each playing position
irrelevant_cb_positions = ['CAM', 'LAM', 'RAM', 'LW', 'LM', 'RW', 'RM', 'CF', 'RF', 'LF', 'ST', 'RS', 'LS']
irrelevant_rb_lb_positions = ['CAM', 'LAM', 'RAM', 'CF', 'RF', 'LF', 'ST', 'RS', 'LS']
irrelevant_cdm_positions = ['LW', 'LM', 'RW', 'RM', 'CF', 'RF', 'LF', 'ST', 'RS', 'LS']
irrelevant_cm_positions = ['CB', 'LCB', 'RCB', 'LB', 'LWB', 'RB', 'RWB', 'LW', 'LM', 'RW', 'RM', 'CF', 'RF', 'LF', 'ST', 'RS', 'LS']
irrelevant_cam_positions = ['CB', 'LCB', 'RCB', 'LB', 'LWB', 'RB', 'RWB', 'ST', 'RS', 'LS']
irrelevant_lw_rw_positions = ['CB', 'LCB', 'RCB', 'CDM', 'LDM', 'RDM', 'CM', 'LCM', 'RCM']
irrelevant_cf_st_positions = ['CB', 'LCB', 'RCB', 'LB', 'LWB', 'RB', 'RWB', 'CDM', 'LDM', 'RDM', 'CM', 'LCM', 'RCM']

# Lists of irrelevant ratings for each playing position
irrelevant_cb_ratings = ['Crossing', 'Finishing', 'Volleys', 'Curve', 'FKAccuracy', 'ShotPower', 'LongShots', 'Penalties']
irrelevant_lb_rb_ratings = ['HeadingAccuracy', 'Volleys', 'Penalties', 'Finishing']
irrelevant_cdm_ratings = ['Finishing', 'Volleys', 'Curve', 'FKAccuracy', 'Penalties']
irrelevant_cam_ratings = ['SlidingTackle', 'Interceptions', 'Marking']
irrelevant_lw_rw_ratings = ['Interceptions', 'Marking', 'StandingTackle', 'SlidingTackle']
irrelevant_cf_st_ratings = ['Interceptions', 'Marking', 'StandingTackle', 'SlidingTackle', 'LongPassing']
