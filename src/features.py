from sklearn.preprocessing import MinMaxScaler
import constants


def replace_special_body_types(body_type):
    special_types = {'Akinfenwa': 'Stocky', 'Shaqiri': 'Stocky', 'C. Ronaldo': 'Lean', 'Courtois': 'Lean',
                     'Messi': 'Lean', 'Neymar': 'Lean', 'PLAYER_BODY_TYPE_25': 'Lean'}

    if body_type not in special_types:
        return body_type
    else:
        return special_types.get(body_type)


def height_to_cm(height):
    """Convert feet-inch height to cm"""
    h_ft, h_inch = [float(i) for i in height.split('\'')]
    h_inch += h_ft * 12
    return round(h_inch * 2.54, 1)


def rating_to_number(rating):
    """Remove everything in ratings from + till the end. If rating doesn't contain +, it is skipped """
    if type(rating) is not int:
        return rating.split('+')[0]
    else:
        return 0


def convert_value(value):
    """Convert value units from thousands to millions. Values already in millions are skipped. Example: 600K -> 0.6 """
    if 'K' in value:
        return round(float(value.replace('K', ''))/1000, 3)
    else:
        return value


def irrelevant_ratings_to_zero(s):
    """For each position, set irrelevant ratings for that position to 0"""
    if s.Position in ['CB', 'LCB', 'RCB']:
        cols = constants.irrelevant_cb_positions + constants.irrelevant_cb_ratings
        s[cols] = s[cols].apply(lambda x: 0)

    elif s.Position in ['RB', 'RWB', 'LB', 'LWB']:
        cols = constants.irrelevant_rb_lb_positions + constants.irrelevant_lb_rb_ratings
        s[cols] = s[cols].apply(lambda x: 0)

    elif s.Position in ['CDM', 'LDM', 'RDM']:
        cols = constants.irrelevant_cdm_positions + constants.irrelevant_cdm_ratings
        s[cols] = s[cols].apply(lambda x: 0)

    elif s.Position in ['CM', 'LCM', 'RCM']:
        cols = constants.irrelevant_cm_positions
        s[cols] = s[cols].apply(lambda x: 0)

    elif s.Position in ['CAM', 'LAM', 'RAM']:
        cols = constants.irrelevant_cam_positions + constants.irrelevant_cam_ratings
        s[cols] = s[cols].apply(lambda x: 0)

    elif s.Position in ['LW', 'LM', 'RW', 'RM']:
        cols = constants.irrelevant_lw_rw_positions + constants.irrelevant_lw_rw_ratings
        s[cols] = s[cols].apply(lambda x: 0)

    elif s.Position in ['CF', 'RF', 'LF', 'ST', 'RS', 'LS']:
        cols = constants.irrelevant_cf_st_positions + constants.irrelevant_cf_st_ratings
        s[cols] = s[cols].apply(lambda x: 0)

    return s


class Features:

    def __init__(self, x_raw):
        self.x_raw = x_raw
        self.processed_features = x_raw

    def replace_nulls_with_zeroes(self):
        """Filling null values for position ratings for goalkeepers"""
        self.processed_features[self.processed_features.Position == 'GK'] = \
            self.processed_features[self.processed_features.Position == 'GK'].fillna(0)

    def process_positions(self):
        """Remove everything starting from + till the end for each position rating"""
        pos = constants.all_positions
        self.processed_features[pos] = self.processed_features[pos].applymap(rating_to_number)

    def process_work_rate(self):
        """Replace Work Rate column with two separate numeric features"""
        self.processed_features[["Att work rate", "Def work rate"]] = self.processed_features['Work Rate'].str.split('/ ', expand=True)
        wr_ord_map = {'Low': 0, 'Medium': 1, 'High': 2}
        self.processed_features['Att work rate'] = self.processed_features['Att work rate'].map(wr_ord_map)
        self.processed_features['Def work rate'] = self.processed_features['Def work rate'].map(wr_ord_map)

    def encode_position(self):
        """Replace position with numerical value"""
        self.processed_features.Position = self.processed_features.Position.map(constants.position_ord_map)

    def drop_columns(self):
        """Drop irrelevant columns"""
        self.processed_features.drop(constants.irrelevant_columns, axis=1, inplace=True)

    def process_value_and_wage(self):
        """Remove characters from Value and Wage"""
        self.processed_features.Value = self.processed_features.Value.str.replace('€', '').str.replace('M', '')
        # Correctly converting Values which are less than 1M, for example 600K converts to 0.6
        self.processed_features.Value = self.processed_features.Value.apply(convert_value)
        self.processed_features.Wage = self.processed_features.Wage.str.replace('€', '').str.replace('K', '')

    def process_preferred_foot(self):
        """Replace preferred foot with numbers 0 and 1"""
        foot_ord_map = {'Left': 0, 'Right': 1}
        self.processed_features["Preferred Foot"] = self.processed_features["Preferred Foot"].map(foot_ord_map)

    def encode_body_types(self):
        """Replace body types with numerical values"""
        body_ord_map = {'Lean': 0, 'Normal': 1, 'Stocky': 2}
        self.processed_features["Body Type"] = self.processed_features["Body Type"].map(body_ord_map)

    def gk_ratings_to_zero(self):
        """Set goalkeeper ratings to 0 for every player that's not goalkeeper"""
        for rating in constants.gk_ratings_columns:
            self.processed_features[rating][self.processed_features.Position != 'GK'] = \
                self.processed_features[rating][self.processed_features.Position != 'GK'].apply(lambda x: 0)

    def process_ratings(self):
        """Set irrelevant ratings to 0 for different playing positions"""
        self.processed_features = self.processed_features.apply(irrelevant_ratings_to_zero, axis=1)


    def build_features(self):
        """Process raw features and get fully processed features ready for model application"""
        self.drop_columns()
        self.process_value_and_wage()
        self.process_preferred_foot()
        self.process_work_rate()
        self.processed_features = self.processed_features.drop(['Work Rate'], axis=1)
        self.processed_features['Body Type'] = self.processed_features['Body Type'].apply(replace_special_body_types)
        self.encode_body_types()
        self.replace_nulls_with_zeroes()
        self.gk_ratings_to_zero()
        self.process_ratings()
        self.encode_position()
        self.processed_features.Height = self.processed_features.Height.map(height_to_cm)
        self.processed_features.Weight = self.processed_features.Weight.apply(lambda x: x.replace('lbs', ''))
        self.process_positions()

    def columns_to_scale(self):
        """Return the names of columns that need to be scaled"""
        return [i for i in self.processed_features.columns if i not in constants.columns_to_skip_scaling]

    def scale_features(self, dataset):
        """Scale features with respect to dataset set"""
        scaler = MinMaxScaler()
        columns = self.columns_to_scale()
        scaler.fit(dataset[columns])

        self.processed_features[columns] = scaler.transform(self.processed_features[columns])

        scaler = MinMaxScaler(feature_range=(0, 5))
        scaler.fit(dataset[['Overall']])
        self.processed_features[['Overall']] = scaler.transform(self.processed_features[['Overall']])

        for col in columns:
            self.processed_features[col] = self.processed_features[col].apply(lambda x: round(float(x), 4))
