import matplotlib.pylab as pltt
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee


# definizione

class BandMatrix:
    size = None
    dataframe = None  # dataframe iniziale
    dataframe_bandizzato = None  # dataframe after RCM e square
    items_final = None  # lista di tutti i prodotti indicizzati con colonna
    lista_sensibili = None  # lista prodotti sensibili
    df_square_complete = None  # matrice transazioni completa
    original_band = None  # larghezza banda pre processing
    band_after_rcm = None  # larghezza banda dopo processing

    # inizializzazione

    def __init__(self, nome_file=None):
        # lettura file .csv
        self.dataframe = pd.read_csv(nome_file, header=None, index_col=None)
        self.size = self.dataframe.shape[0]

    def compute_band_matrix(self, dim_finale=1000, nome_file_item=None, num_sensibile=1, plot=True, withRCM=True):
        """
            Metodo per la lettura da file del dataframe e
            per la creazione di una matrice bandizzata
            tramite algoritmo reverse_cuthill_mckee
        """

        # lettura file e dimensionamento matrice
        original_dataset = self.dataframe
        if original_dataset is not None and nome_file_item is not None:
            file_read = open(nome_file_item, "r")
            items = file_read.read().splitlines()
            file_read.close()
            if len(original_dataset.columns) < dim_finale + num_sensibile:
                if not plot:
                    dim_finale= len(original_dataset.columns) - num_sensibile
                else:
                    choose = input(
                        "Non ci sono abbastanza colonne, vuoi cambiare il numero di colonne da %d a %d? [s/n] " % (dim_finale, len(original_dataset.columns) - num_sensibile))
                    if choose == "s":
                        dim_finale = len(original_dataset.columns) - num_sensibile
                    else:
                        return

            if len(original_dataset) < dim_finale:
                if not plot:
                    dim_finale = len(original_dataset)
                else:
                    choose = input(
                        "Non ci sono abbastanza righe, vuoi cambiare il numero di righe da %d a %d? [y/N] " % (dim_finale, len(original_dataset)))
                    if choose == "y":
                        dim_finale = len(original_dataset)
                    else:
                        return

            # permutazione randomica valori da inserire nella matrice banda
            random_column = np.random.permutation(original_dataset.shape[1])[:dim_finale + num_sensibile]
            random_row = np.random.permutation(original_dataset.shape[0])[:dim_finale]

            items_reordered = [items[i] for i in random_column]
            items_final = dict(zip(random_column, items_reordered))

            self.df_square_complete = original_dataset.iloc[random_row][random_column]


            # controllo che le colonne relative ai sensitive items non sia formata da soli zeri
            lista_sensibili = list()
            SD_zeros = list()
            while len(lista_sensibili) < num_sensibile:
                temp = np.random.choice(random_column)
                if temp not in lista_sensibili and temp not in SD_zeros:
                    if self.df_square_complete[temp].sum() > 0:
                        lista_sensibili.append(temp)
                    else:
                        SD_zeros.append(temp)

            # calcolo densità della matrice
            if withRCM:
                square_column_index = [x for x in random_column if x not in lista_sensibili]
                row_index = [i for i in range(dim_finale)]
                #creazione matrice sensitive
                df_sensitive = self.df_square_complete.iloc[row_index][lista_sensibili]
                #creazione matrice QID
                df_square = self.df_square_complete.iloc[row_index][square_column_index]


                # creazione matrice banda tramite riordine della matrice iniziale
                sparse = csr_matrix(df_square)
                order = reverse_cuthill_mckee(sparse)
                #riordinamento di righe e colonne
                column_reordered = [df_square.columns[i] for i in order]
                df_square_band = df_square.iloc[order][column_reordered]
                df_sensitive_band = df_sensitive.iloc[order]

                #concatenazione di matrice QID bandizzata e matrice sensitive riordinata
                final_df = pd.concat([df_square_band, df_sensitive_band], axis=1, join='inner')

                # calcolo larghezze di banda pre e post processing
                [i, j] = np.where(df_square == 1)
                bw = max(i - j) + max(j - i) + 1
                self.original_band = bw

                [i, j] = np.where(df_square_band == 1)
                bw1 = max(i - j) + max(j - i) + 1
                self.band_after_rcm = bw1

                # parametri per il plot delle matrici
                if plot:
                    f, (ax1, ax2) = pltt.subplots(1, 2, sharey=True)
                    ax1.spy(df_square, marker='.', markersize='3')
                    ax2.spy(df_square_band, marker='.', markersize='3')
                    pltt.show()
                    print("Bandwidth before RCM: ", bw)
                    print("Bandwidth after RCM", bw1)


                self.dataframe_bandizzato = final_df
                self.items_final = items_final
                self.lista_sensibili = lista_sensibili
                
            else:
                [i, j] = np.where(self.df_square_complete == 1)
                bw = max(i - j) + max(j - i) + 1
                self.original_band = bw
                self.band_after_rcm = bw
                if plot:
                    print("Bandwidth before RCM: ", bw)

                self.dataframe_bandizzato = self.df_square_complete
                self.items_final = items_final
                self.lista_sensibili = lista_sensibili
        else:
            print("Error 404: Dataset not found or file not found.")
