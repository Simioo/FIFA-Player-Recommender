from features import Features


class DataSet(Features):

    def __init__(self, x_raw):
        super().__init__(x_raw)

    def process_dataset(self):
        """Drop records with a lot of null values and process dataset"""
        self.drop_null_rows()
        super().build_features()
        super().scale_features(self.processed_features)

    def drop_null_rows(self):
        """Drop records with a lot of null values"""
        self.processed_features = self.processed_features.dropna(subset=['Preferred Foot'])
        self.processed_features = self.processed_features.dropna(subset=['Position'])
        self.processed_features.reset_index()

    def save_to_csv(self):
        self.processed_features.to_csv('../data/processed/processed_dataset.csv', sep=',', index=False)