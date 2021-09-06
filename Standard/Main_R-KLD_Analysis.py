import BandMatrix
import CAHDalgorithm
import time
import numpy as np
import KLDivergence
import random
import matplotlib.pyplot as plt

import OutputData

if __name__ == "__main__":
    dim_finale = 1000
    grado_privacy_list = [25, 50]
    r_list = [2, 4, 6]
    alpha = 3
    name_file_list = ["Dataset/BMS1.csv"]
    list_item = ["Dataset/items_BMS1.txt"]

    num_sensibile = 50
    max_attempts = 3
    kl_attempts = 3

    for index_nameFile in range(len(name_file_list)):
        big_ben = time.time()
        nameFile = name_file_list[index_nameFile]
        listaItem = list_item[index_nameFile]
        df = BandMatrix.BandMatrix(nameFile)
        name_file = nameFile.split("/")[1].split(".")[0] + "-" + str(dim_finale) + "-" + str(num_sensibile) + "-" + str(kl_attempts)
        for att in range(max_attempts):
            for index_grado_privacy in range(len(grado_privacy_list)):
                grado_privacy = grado_privacy_list[index_grado_privacy]

                df.compute_band_matrix(
                    dim_finale=dim_finale,
                    nome_file_item=listaItem,
                    num_sensibile=num_sensibile,
                    plot=False)
                dataframe_bandizzato = df.dataframe_bandizzato.copy()
                for index_r in range(len(r_list)):
                    print("%.2f |File : %s | Index privacy : %s | Attempt : %s | Index R: %s" % (
                        time.time() - big_ben, index_nameFile, index_grado_privacy, att, index_r))
                    r = r_list[index_r]
                    cahd = CAHDalgorithm.CAHDalgorithm(
                        df,
                        grado_privacy=grado_privacy,
                        alfa=alpha)
                    cahd.compute_hist()
                    hist_item = cahd.hist
                    if cahd.CAHD_algorithm(analysis=True, plot= False):
                        if cahd.lista_gruppi is not None:
                            QID = cahd.lista_gruppi[0].columns.tolist()
                            KL_Divergence = 0
                            for kl_attempt in range(kl_attempts):
                                QID_select = list()
                                while len(QID_select) < r and len(QID_select) < len(QID):
                                    temp = random.choice(QID)
                                    if temp not in QID_select:
                                        QID_select.append(temp)
                                all_value = KLDivergence.get_all_combination_of_n(r)
                                item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
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
                                    KL_Divergence = KL_Divergence + temp
                            file_1 = open("MainPlotData/2/" + name_file + ".txt", "a")
                            file_1.write(str(grado_privacy) + "," + str(r) + "," + str(KL_Divergence) + ";")
                            file_1.close()
