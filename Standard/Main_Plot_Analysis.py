import matplotlib.pyplot as plt
from collections import defaultdict

if __name__ == "__main__":

    folder = "MainPlotData/"
    file_input = ["BMS2-1000-5-3.txt","BMS2-1000-5-3.txt","BMS2-1000-50-3.txt","BMS2-1000-50.txt"]
    #file_input = ["BMS1-1000-7-4.txt","BMS1-1000-7-4.txt","BMS1-1000-10-4.txt","BMS1-1000-10.txt"]
    x_label = ["p", "m", "r", "p"]
    y_label = ["KL-Divergence","KL-Divergence","KL-Divergence","Times (sec)"]
    marker = ["o", "s", "X", "D", "*", "^", "H", "1"]
    color = ["b", "g", "r", "c", "m", "y", "k"]
    changing_variable = ["m", "p", "p", "with RCM"]

    for i in range(4):
        folder_t = folder + str(i)+"/"
        file_read = open(folder_t + file_input[i], "r")
        triplets = file_read.read().split(";")
        file_read.close()

        ns_list = []
        p_list = []
        KL_list = []
        for triplet in triplets:
            if triplet == "":
                continue
            triplet = triplet.split(",")
            ns_list.append(triplet[0])
            p_list.append(triplet[1])
            KL_list.append(float(triplet[2]))


        def list_duplicates(seq):
            dd = defaultdict(list)
            for i, item in enumerate(seq):
                dd[item].append(i)
            return ((key, locs) for key, locs in dd.items()
                    if len(locs) > 1)

        dict_ns = dict(sorted(list_duplicates(ns_list)))
        dict_p = dict(sorted(list_duplicates(p_list)))

        dict_fin = dict()
        for val in dict_ns.keys():
            for val1 in dict_p.keys():
                for arr in dict_ns.get(val):
                    for arr1 in dict_p.get(val1):
                        if arr == arr1:
                            tt = dict_fin.get(str(val) + "," + str(val1))
                            if tt is not None:
                                tt[0] += KL_list[arr]
                                tt[1] += 1
                            else:
                                dict_fin[str(val) + "," + str(val1)] = [KL_list[arr], 1]
        if len(dict_fin) == 0 :
            for val in dict_ns.keys():
                for p_in in range(len(p_list)):
                    dict_fin[str(val) + "," + str(p_list[p_in])] = [KL_list[p_in], 1]

        ns_list = list(dict.fromkeys(ns_list))
        p_list = list(dict.fromkeys(p_list))
        dict_keys = dict_fin.keys()
        for in_n in range(len(ns_list)):
            n = ns_list[in_n]
            x = list()
            y = list()
            att = list()
            for p in p_list:
                key = str(n) + "," + str(p)
                if key in dict_keys:
                    arr_t = dict_fin[key]
                    att.append(arr_t[1])
                    y.append(arr_t[0] / arr_t[1])
                    x.append(int(p))
            for i_1 in range(len(x)-1):
                for i_2 in range(i_1+1, len(x)):
                    if x[i_1] > x[i_2]:
                        t = x[i_1]
                        x[i_1] = x[i_2]
                        x[i_2] = t
                        t = y[i_1]
                        y[i_1] = y[i_2]
                        y[i_2] = t
            i_m1 = in_n % len(marker)
            i_m2 = in_n % len(color)
            plt.plot(x, y, marker=marker[i_m1], linestyle='-', color=color[i_m2], label=changing_variable[i]+' = '+str(n)+"  "+str(att))
        plt.xlabel(x_label[i])
        plt.ylabel(y_label[i])
        plt.title(file_input[i].split(".")[0])
        plt.legend(frameon=False, loc='upper center')
        plt.show()
        print("Analysis n: %s" % i)
        data = file_input[i].split(".")[0].split("-")
        print("Dataset: " + data[0])
        if i == 0:
            print("QID matrix dimension: " + data[1])
            print("R value: " + data[2])
            print("R attempts: " + data[3])
        elif i == 1:
            print("QID matrix dimension: " + data[1])
            print("R value: " + data[2])
            print("R attempts: " + data[3])
        elif i == 2:
            print("QID matrix dimension: " + data[1])
            print("Number of sensitive attributes: " + data[2])
            print("R attempts: " + data[3])
        elif i == 3:
            print("QID matrix dimension: " + data[1])
            print("Number of sensitive attributes: " + data[2])
        print("")






