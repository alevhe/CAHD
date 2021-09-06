import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import random


class BandMatrix_priority:
    size = None
    dataframe = None
    dataframe_bandizzato = None
    items_final = None
    lista_sensibili = None
    size_after_RCM = None
    bm_square_complete = None

    def __init__(self, nome_file=None):

        self.dataframe = pd.read_csv(nome_file, header=None, index_col=None)
        self.size = self.dataframe.shape[0]

    def compute_band_matrix(self, dim_finale=1000, nome_file_item=None, num_sensibile=1):

        original_dataset = self.dataframe
        if original_dataset is not None and nome_file_item is not None:

            file_read = open(nome_file_item, "r")
            items = file_read.read().splitlines()
            file_read.close()

            if len(original_dataset.columns) < dim_finale + num_sensibile:

                dim_finale = len(original_dataset.columns) - num_sensibile


            if len(original_dataset) < dim_finale:

                dim_finale = len(original_dataset)
            self.size_after_RCM = dim_finale

            random_column = np.random.permutation(original_dataset.shape[1])[:dim_finale + num_sensibile]
            random_row = np.random.permutation(original_dataset.shape[0])[:dim_finale]

            items_reordered = [items[i] for i in random_column]
            items_final = dict(zip(random_column, items_reordered))

            self.bm_square_complete = original_dataset.iloc[random_row][random_column]

            lista_sensibili = list()
            SD_zeros = list()
            while len(lista_sensibili) < num_sensibile:
                temp = random.choice(random_column)
                if temp not in lista_sensibili and temp not in SD_zeros:
                    if self.bm_square_complete[temp].sum() > 0:
                        lista_sensibili.append(temp)
                    else:
                        SD_zeros.append(temp)

            square_column_index = [x for x in random_column if x not in lista_sensibili]
            row_index = [i for i in range(dim_finale)]
            df_sensitive = self.bm_square_complete.iloc[row_index][lista_sensibili]
            df_square = self.bm_square_complete.iloc[row_index][square_column_index]

            sparse = csr_matrix(df_square)
            order = reverse_cuthill_mckee(sparse)

            column_reordered = [df_square.columns[i] for i in order]

            df_square_band = df_square.iloc[order][column_reordered]
            df_sensitive_band = df_sensitive.iloc[order]

            final_df = pd.concat([df_square_band, df_sensitive_band], axis=1, join='inner')

            self.dataframe_bandizzato = final_df
            self.items_final = items_final
            self.lista_sensibili = lista_sensibili
        else:
            print("Error 404: Dataset not found or file not found.")
