from biomeanalyzer.Data_IO import load_data, load_legend
from biomeanalyzer.normalization.normalize_data import normalize_data


class AddLegend:
    def __init__(self, data_path, legend_path, normalize=True):

        self.normalize = normalize

        if self.normalize == True:
            self.df = normalize_data(data_path)
        else:
            self.df = load_data(data_path)

        self.legend = load_legend(legend_path)

    def add_legend(self):
        self.df['Legend'] = self.df['Sample Name'].map(self.legend)
        return self.df