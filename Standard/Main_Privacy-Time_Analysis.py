import BandMatrix
import CAHDalgorithm
import time


if __name__ == "__main__":
    dim_finale = 1000
    num_sensibile = 50
    grado_privacy_list = [15, 25, 50, 75]
    alpha = 3
    name_file_list = ["Dataset/BMS1.csv"]
    list_item = ["Dataset/items_BMS1.txt"]

    max_attempts = 4

    for index_nameFile in range(len(name_file_list)):
        big_ben = time.time()
        nameFile = name_file_list[index_nameFile]
        listaItem = list_item[index_nameFile]
        #print("Read Dataset file "+nameFile)
        for att in range(max_attempts):
            for i in range(2):
                for index_grado_privacy in range(len(grado_privacy_list)):
                    start_time = time.time()
                    print("%.2f |File : %s | Mode : %s | Attempt : %s | Index privacy: %s" % (start_time - big_ben, index_nameFile, i, att, index_grado_privacy))
                    df = BandMatrix.BandMatrix(nameFile)
                    name_file = nameFile.split("/")[1].split(".")[0] + "-" + str(dim_finale) + "-" + str(num_sensibile)

                    withRCM = (i != 0)

                    df.compute_band_matrix(
                        dim_finale=dim_finale,
                        nome_file_item=listaItem,
                        num_sensibile=num_sensibile,
                        plot=False,
                        withRCM=withRCM)
                    dataframe_bandizzato = df.dataframe_bandizzato.copy()
                    grado_privacy = grado_privacy_list[index_grado_privacy]
                    cahd = CAHDalgorithm.CAHDalgorithm(
                        df,
                        grado_privacy=grado_privacy,
                        alfa=alpha)
                    cahd.compute_hist()
                    hist_item = cahd.hist
                    if(cahd.CAHD_algorithm(analysis=True,
                                           plot=False)):
                        end_time = time.time() - start_time
                        file_1 = open("MainPlotData/3/" + name_file + ".txt", "a")
                        file_1.write(str(i) + "," + str(grado_privacy) + "," + str(end_time) + ";")
                        file_1.close()