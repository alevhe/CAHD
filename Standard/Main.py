import time
import BandMatrix
import CAHDalgorithm
import OutputData

"""
    Main principale per la 
    chiamata alle classi 
    BandMatrix & CAHDalgorithm
"""

if __name__ == "__main__":
    dim_finale = 10000  # dimensione massima matrice
    num_sensibile = 10  # n° dati sensibili
    grado_privacy = 10  # grado di privacy richiesto
    alpha = 3

    # lettura da file del dataset
    nameFile = "Dataset/BMS1.csv"
    listaItem = "Dataset/items_BMS1.txt"
    print("Read Dataset")

    # partenza cronometro per registrazione prestazioni
    start_time = time.time()
    print("Calcolo la band matrix" + "\n")
    df = BandMatrix.BandMatrix(nameFile)

    # calcolo matrice banda
    df.compute_band_matrix(
        dim_finale=dim_finale,
        nome_file_item=listaItem,
        num_sensibile=num_sensibile)

    # applicazione algoritmo CAHD
    cahd = CAHDalgorithm.CAHDalgorithm(
        df,
        grado_privacy=grado_privacy,
        alfa=alpha)
    print("Eseguo Anonimizzazione")
    if cahd.CAHD_algorithm():
        end_time = time.time() - start_time
        print("Il tempo di esecuzione per il grado di privacy %s è %s" % (cahd.grado_privacy, end_time))
        print("")

        pr = OutputData.Printer(cahd, df)
        pr.stampa_gruppi()
        print("Control data")
        pr.controllo_dati(control=True)