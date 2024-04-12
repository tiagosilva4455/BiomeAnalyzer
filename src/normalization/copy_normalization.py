import pandas as pd
import BiomeAnalyzer
from BiomeAnalyzer.src.io.load_data import load_data
from BiomeAnalyzer.src.io.load_data import load_legend

class CopyNormalization:
    
    def __init__(self, path_dataset, path_legend):
        
        self.data = load_data(path_dataset)
        self.legend = load_legend(path_legend)
        self.copy_number_db = pd.read_csv("BiomeAnalyzer/database/16S_rRNA_copy/rrnDB-5.8_pantaxa_stats_NCBI.tsv", sep=";")
        self.normalized_data = None

    def get_mean_copy_count(self, m):
    
        taxa = m.split(";")
        n_taxa = len(taxa)-1
        name = taxa[n_taxa]
        
        try:
            if name.split(" ")[1] == "sp":
                 name = name.strip() + "."
        except:
             pass
        
        while name.strip() not in self.copy_number_db['name'].values:
            n_taxa -= 1
            if n_taxa < 0:
                return 1
            name = taxa[n_taxa]   

        if name.strip() in self.copy_number_db['name'].values:
            name = name.strip()
            # Retrieve the mean copy count for the microorganism
            mean_copy_count = self.copy_number_db.loc[self.copy_number_db['name'] == name, 'mean'].values[0]
            return mean_copy_count
        else:
            return 1 #that n was not found in the dataset, therefore the value will be it self (1)

    def normalize_data(self):

        normalized_data = self.data.copy()

        for n in self.data.index:
            normalized_data.loc[n] = self.data.loc[n] / float(self.get_mean_copy_count(n))

        total_w_copies = normalized_data.sum(axis=0)

        # print(total_w_copies)

        for n in normalized_data.index:
            normalized_data.loc[n] = (100 * normalized_data.loc[n]) / total_w_copies
        
        self.normalized_data = normalized_data

        return normalized_data
    
if __name__ == "__main__":
    normalize_data = CopyNormalization("BiomeAnalyzer/database/16S_rRNA_copy/rrnDB-5.8_pantaxa_stats_NCBI.tsv", "BiomeAnalyzer/database/16S_rRNA_copy/rrnDB-5.8_pantaxa_stats_NCBI.tsv").normalize_data()
    print(normalize_data)