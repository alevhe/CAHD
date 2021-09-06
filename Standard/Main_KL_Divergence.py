import BandMatrix
import CAHDalgorithm
import time
import numpy as np
import KLDivergence
import random

"""
    Main per l'esecuzione di 
    MatriceBanda e CAHDalgorithm
    con calcolo KL_Divergence
"""
if __name__ == "__main__":
    dim_finale = 2000  # dimensione massima matrice
    num_sensibile = 10  # n° dati sensibili
    grado_privacy = 10  # grado privacy richiesto
    alpha = 3


    # lettura da file del dataset
    nameFile = "Dataset/BMS1.csv"
    listaItem = "Dataset/items_BMS1.txt"
    print("Read Dataset")
    df = BandMatrix.BandMatrix(nameFile)

    # partenza cronometro per registrazione prestazioni
    start_time = time.time()
    print("Calcolo la band matrix")

    # calcolo matrice banda
    df.compute_band_matrix(
        dim_finale=dim_finale,
        nome_file_item=listaItem,
        num_sensibile=num_sensibile)
    print("")

    # applicazione algoritmo CAHD
    cahd = CAHDalgorithm.CAHDalgorithm(
        df,
        grado_privacy=grado_privacy,
        alfa=alpha)
    cahd.compute_hist()
    hist_item = cahd.hist
    print("Eseguo Anonimizzazione")
    cahd.CAHD_algorithm()
    end_time = time.time() - start_time
    print("Il tempo di esecuzione per il grado di privacy %s è %s" % (cahd.grado_privacy, end_time) + "\n")

    # selezione n° QID nella query per KL_Divergence
    r = 4
    all_item = list(df.items_final.keys())
    columns_item_sensibili = df.lista_sensibili
    dataframe_bandizzato = df.dataframe_bandizzato
    QID = cahd.lista_gruppi[0].columns.tolist()
    QID_select = list()
    while len(QID_select) < r:
        temp = random.choice(QID)
        if temp not in QID_select:
            QID_select.append(temp)

    # calcolo di tutte le combinazioni per la cella C
    all_value = KLDivergence.get_all_combination_of_n(r)

    # calcolo il valore massimo nei sensitive items
    item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
    KL_Divergence = 0

    # calcolo actsc e estsc richieste per KL_Divergence
    for valori in all_value:
        actsc = KLDivergence.compute_act_s_in_c(dataframe_bandizzato, QID_select, valori, item_sensibile)
        estsc = KLDivergence.compute_est_s_in_c(dataframe_bandizzato, cahd.sd_gruppi,
                                                cahd.lista_gruppi, QID_select, valori, item_sensibile)
        if actsc > 0 and estsc > 0:
            temp = actsc * np.log(actsc / estsc)
        else:
            temp = 0
        KL_Divergence = KL_Divergence + temp
    print("Grado di privacy: " + str(cahd.grado_privacy) + ", Numero items sensibili: " + str(num_sensibile)
          + ", KL_Divergence: " + str(KL_Divergence))
