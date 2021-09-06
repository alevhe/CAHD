import BandMatrix_Priority
import CAHD_Priority
import time
import numpy as np
import KLDivergence
import random

if __name__ == "__main__":
    alpha = 3
    nameFile = "Dataset/BMS1.csv"
    listaItem = "Dataset/items_BMS1.txt"
    print("Read Dataset")
    df = BandMatrix_Priority.BandMatrix_priority(nameFile)
    dim_finale = 471  # per BMS1.csv
    num_sensibile = 10

    max_attempts = 15  # Numero test completi
    grado_privacy = [30]  # Valori di Privacy
    #grado_privacy = [5, 10, 15, 20, 30]  # Valori di Privacy
    priority_value_attempts = 5  # Numero di valori di priority utilizzati per ogni grado privacy
    # range valori priority
    min_priority = 0.05
    max_priority = 2
    kl_attempts = 3  # Numero di volte in cui viene eseguita la KL_Divergence con QID diversi
    r = 4  # Numero di QID considerati nella KL_Divergence



    big_ben = time.time()
    for i in range(max_attempts):
        df.compute_band_matrix(dim_finale=dim_finale, nome_file_item=listaItem, num_sensibile=num_sensibile)
        dim_finale = df.size_after_RCM
        # Ciclo per ogni valore di grado_privacy
        for privacy in grado_privacy:
            all_item = list(df.items_final.keys())
            columns_item_sensibili = df.lista_sensibili
            dataframe_bandizzato = df.dataframe_bandizzato
            QID = [x for x in dataframe_bandizzato.columns if x not in columns_item_sensibili]
            QID_list_to_select = list()

            # Creo i kl_attemps gruppi di QID (ognuno di r QID)
            for ii in range(kl_attempts):
                QID_select = list()
                while len(QID_select) < r:
                    temp = random.choice(QID)
                    if temp not in QID_select:
                        QID_select.append(temp)
                QID_list_to_select.append(QID_select)

            KLs = list()
            time_list = list()
            priority_time_list = list()
            exit_list = list()
            privacy_list = list()
            # Compio CAHD priority_value_attempts volte con valori di priority compresi tra min_priority e max_priority
            for iii in range(priority_value_attempts):
                start_time = time.time()
                if iii == 0: priority = 0
                else: priority = np.random.uniform(min_priority, max_priority)
                cahd = CAHD_Priority.CAHDalgorithm(
                    df,
                    grado_privacy=privacy,
                    alfa=alpha,
                    priority_grade=priority)

                hist_item = cahd.hist
                # CAHD torna False solo se il grado massimo di privacy è 1
                if cahd.CAHD_algorithm(analysis=True):
                    end_time_1 = time.time() - start_time
                    KL_Divergence = 0
                    for ii in range(kl_attempts):
                        all_value = KLDivergence.get_all_combination_of_n(r)
                        # get max value of sensibile data
                        item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
                        QID_select = QID_list_to_select[ii]
                        for valori in all_value:
                            actsc = KLDivergence.compute_act_s_in_c(dataframe_bandizzato, QID_select, valori,
                                                                    item_sensibile)
                            estsc = KLDivergence.compute_est_s_in_c(dataframe_bandizzato, cahd.sd_gruppi,
                                                                    cahd.lista_gruppi,
                                                                    QID_select, valori, item_sensibile)
                            if actsc > 0 and estsc > 0:
                                temp = actsc * np.log(actsc / estsc)
                            else:
                                temp = 0
                            KL_Divergence += temp
                    # Aggiungiamo la media dei valori di KL_Divergence sui kl_attempts prove
                    KLs.append(KL_Divergence / kl_attempts)
                    ac_t = time.time()
                    print("%.2f | Attempt : %s | Priority : %s | grado_privacy  : %s | Execution CAHD : %.2f | Execution KL-D : %.2f" % (
                    ac_t - big_ben, i, priority, cahd.grado_privacy, end_time_1, ac_t - start_time))
                    exit_list.append(len(cahd.lista_gruppi))
                    priority_time_list.append(priority)
                    time_list.append(ac_t - start_time)
                    privacy_list.append(cahd.grado_privacy)
                else:
                    ac_t = time.time()
                    print("%.2f | Attempt : %s | Priority : %s | grado_privacy  : %d | CAHD failed : %.2f" % (
                        ac_t - big_ben, i, priority, cahd.grado_privacy, ac_t - start_time))


            # Stampa su file dei risultati
            name_file = nameFile.split("/")[1].split(".")[0] + "-" + str(num_sensibile) + "-" + "-" + str(kl_attempts) + "-" + str(r) + "-" + str(dim_finale)
            folder = "Priority-Study/"
            file_1 = open(folder + name_file + "_divergence_result.txt", "a")
            file_3 = open(folder + name_file + "_complete_time.txt", "a")
            file_4 = open(folder + name_file + "_complete_exit.txt", "a")
            file_5 = open(folder + name_file + "_complete_input.txt", "a")
            for j in range(len(KLs)):
                file_1.write(str(KLs[j]) + ";")  # Valore KL
                file_3.write(str(time_list[j]) + ";")  # Tempo impiegato per CAHD e KL_Divergence
                file_4.write(str(exit_list[j]) + ";")  # Numero di gruppi creati (-1 se fallisce)
                file_5.write(str(priority_time_list[j]) + "," + str(privacy_list[j]) + ";")  # Coppia valore priorità, valore privacy
            file_1.close()
            file_3.close()
            file_4.close()
            file_5.close()
