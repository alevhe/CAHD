import time
import random
import CAHD_Priority
import BandMatrix_Priority
import KLDivergence
import numpy as np
"""
    Il programma testa dataset di diversa densità con diversi valori del parametro priority
    Si può scegliere tra dataset densi o sparsi ed i risultati vengono stampati su file.
"""
if __name__ == "__main__":
    n_sensibili = 10
    alfa = 3
    n_test = 10
    # Valori di priority (primo valore = 0 per valutare anche il caso senza priority)
    priority_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    scelta = None
    while scelta != "d" and scelta != "s":
        scelta = input("Si desiderano dataset densi o sparsi? [d/s]")

    if scelta == "s":
        set_dim = 50
        file_avg = open("TestSparsi/avg0.txt", "a")
        densita_dataset = [0.01, 0.04, 0.07, 0.1]
    else:
        set_dim = 100
        file_avg = open("TestDensi/avg1.txt", "a")
        densita_dataset = [0.2, 0.3, 0.4, 0.45]
    
    start_time = time.time()

    # Ciclo su 4 dataset: densi o sparsi
    for n in range(4):
        print("\nDATASET n.%d\n" % n)

        # Setto i file di lettura o scrittura
        if scelta == "s":
            privacy = 5
            nameFileTest = "TestSparsi/test" + str(n) + ".txt"
            nameFile = "Dataset-Test-Priority/data_transaction" + str(n) + ".csv"
            listaItem = "Dataset-Test-Priority/list_items" + str(n) + ".txt"
        else:
            privacy = 2
            nameFileTest = "TestDensi/test1" + str(n) + ".txt"
            nameFile = "Dataset-Test-Priority/data_transaction1" + str(n) + ".csv"
            listaItem = "Dataset-Test-Priority/list_items1" + str(n) + ".txt"

        file_test = open(nameFileTest, "a")
        hist_item = None
        KL_avg_list = [0] * len(priority_list)

        n_fail = 0
        # Ciclo n_test volte lo stesso dataset per avere risultati più attendibili
        for i in range(n_test):
            fail = False
            file_test.write("Test n " + str(i) + "\n")
            bm = BandMatrix_Priority.BandMatrix_priority(nameFile)
            bm.compute_band_matrix(dim_finale=set_dim, nome_file_item=listaItem, num_sensibile=n_sensibili)

            KL_list = list()
            # Ciclo su ogni valore di 'priority'
            for p in priority_list:
                file_test.write("Priority %.2f :" % p)
                print("Test %d priority %.2f" % (i, p))
                cahd = CAHD_Priority.CAHDalgorithm(bm, grado_privacy=privacy, priority_grade=p)
                hist_item = cahd.hist

                # cahd.CAHD_algorithm torna true se riesce a creare gruppi con grado privacy > 1
                if cahd.CAHD_algorithm(True):
                    # KL-Divergence
                    r = 5  # numero di QID nella query
                    all_item = list(bm.items_final.keys())
                    columns_item_sensibili = bm.lista_sensibili.copy()
                    dataframe_bandizzato = bm.dataframe_bandizzato

                    QID = cahd.lista_gruppi[0].columns.tolist()
                    QID_select = list()
                    QID_zeros = list()
                    # Prendo 'r' QI randomicamente
                    while len(QID_select) < r:
                        temp = random.choice(QID)
                        if temp not in QID_select and temp not in QID_zeros:
                            # Scarto i QI son soli zeri
                            if dataframe_bandizzato[temp].sum() > 0:
                                QID_select.append(temp)
                            else:
                                QID_zeros.append(temp)

                    all_value = KLDivergence.get_all_combination_of_n(r)

                    # Torna la label dell'item sensibile con più occorrenze
                    item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
                    KL_Divergence = 0
                    for valori in all_value:
                        actsc = KLDivergence.compute_act_s_in_c(dataframe_bandizzato, QID_select, valori,
                                                                item_sensibile)
                        estsc = KLDivergence.compute_est_s_in_c(dataframe_bandizzato, cahd.sd_gruppi,
                                                                cahd.lista_gruppi, QID_select, valori,
                                                                item_sensibile)

                        if actsc > 0 and estsc > 0: KL_Divergence += actsc * np.log(actsc / estsc)

                    file_test.write("Privacy: %d - KL-Divergence: %.3f \n\n" % (cahd.grado_privacy, KL_Divergence))
                    KL_list.append(KL_Divergence)
                else:
                    # Cahd torna False se il grado_privacy massimo è 1 o se crea i gruppi ma l'ultimo gruppo non soddisfa
                    print("CAHD non andata a buon fine")
                    KL_Divergence = 0
                    if cahd.flagErr: KL_Divergence = float(-999) #Ultimo gruppo non soddisfa
                    else: KL_Divergence = float(-99) #grado privacy non accettato (=1)
                    KL_list.append(KL_Divergence)
                    file_test.write("KL-Divergence: %.3f \n\n" % KL_Divergence)

            print("-------Test %d FINITO---------" % i)
            file_test.write("\n--------------------------\n")

            for j in range(len(priority_list)):
                if KL_list[j] != -99: KL_avg_list[j] += KL_list[j]
                else:
                    fail = True

            if fail: n_fail += 1

        file_test.write("\n-------------VALORI MEDI-------------\n")
        file_avg.write("\nValori Medi Dataset %d con densita' %.2f\n" % (n, densita_dataset[n]))
        n_true_test = n_test-n_fail
        if n_true_test > 0:
            for k in range(len(KL_avg_list)):
                file_test.write("Priorità: %.2f KL medio: %.2f -- con %d fallimenti\n" % (priority_list[k], KL_avg_list[k]/n_true_test, n_fail))
                file_avg.write("Priorità: %.2f KL medio: %.2f\n" % (priority_list[k], KL_avg_list[k]/n_true_test))
        file_test.close()

    file_avg.close()
    end_time = time.time() - start_time
    print("\nTempo di esecuzione %s s\n" % end_time)
