import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    folder = "Priority-Study/BMS1-10--3-4-471_"
    file_input = "complete_input.txt"
    file_output = "divergence_result.txt"
    file_time = "complete_time.txt"
    file_exit = "complete_exit.txt"

    file_read = open(folder + file_input, "r")
    input_data = file_read.read().split(";")
    file_read.close()

    file_read = open(folder + file_output, "r")
    output_data = file_read.read().split(";")
    file_read.close()

    file_read = open(folder + file_time, "r")
    output_time = file_read.read().split(";")
    file_read.close()

    file_read = open(folder + file_exit, "r")
    output_exit = file_read.read().split(";")
    file_read.close()

    t = [0]*(len(output_time)-1)
    e = [0]*(len(output_exit)-1)
    d = [0]*(len(output_data)-1)
    x = [0]*(len(input_data)-1)
    y = [0]*(len(input_data)-1)

    for it in range(len(input_data)-1):
        itt = input_data[it].split(",")
        x[it] = float(itt[0])
        y[it] = float(itt[1])
    for it in range(len(output_data) - 1):
        d[it] = float(output_data[it])
    for it in range(len(output_time) - 1):
        t[it] = float(output_time[it])
    for it in range(len(output_exit) - 1):
        e[it] = float(output_exit[it])

#    t_n = [0]*len(t)
    y_max = max(y)
    y_min = min(y)

    y_max += 0.02 * (y_max - y_min)
    y_min -= 0.02 * (y_max - y_min)

    x = np.array(x)
    y = np.array(y)
    t = np.array(t)
    d = np.array(d)
    e = np.array(e)

    cmap = plt.plasma()

    f, ax = plt.subplots()
    ax.set_title("KL-Divergence (%s)" % len(d))
    ax.set_ylabel('Privacy')
    ax.set_xlabel('Priority')
    points = ax.scatter(x, y, c=d, s=10, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()

    x1 = x.copy()
    y1 = y.copy()
    d1 = d.copy()
    standard_deviation = np.std(d1)
    print("KL-Divergence")
    while 1:
        m_std = min(d1)
        M_std = max(d1)
        x1_t = list()
        y1_t = list()
        d_t = list()
        x1_m = None
        y1_m = None
        x1_M = None
        y1_M = None
        for index in range(len(d1)):
            if d1[index] == m_std and x1_m is None:
                x1_m = x1[index]
                y1_m = y1[index]
            elif d1[index] == M_std and x1_M is None:
                x1_M = x1[index]
                y1_M = y1[index]
            else:
                d_t.append(d1[index])
                x1_t.append(x1[index])
                y1_t.append(y1[index])
        standard_deviation_t = np.std(d_t)
        diff = standard_deviation - standard_deviation_t
        print("%s - %s" % (M_std, m_std))
        print("%s - %s = %s" % (standard_deviation, standard_deviation_t, diff))
        if diff > 0.0005:
            x1 = x1_t
            y1 = y1_t
            d1 = d_t
            standard_deviation = standard_deviation_t
        else:
            break

    if len(x) > len(x1):
        f, ax = plt.subplots()
        ax.set_title("KL-Divergence (%s)" % len(d1))
        ax.set_ylabel('Privacy')
        ax.set_xlabel('Priority')
        points = ax.scatter(x1, y1, c=d1, s=10, cmap=cmap)
        f.colorbar(points)
        plt.ylim((y_min, y_max))
        plt.show()

    """
    cmap = plt.winter()

    avg_d = np.average(d)
    avg_l = list()
    x_l = list()
    x_u = list()
    y_l = list()
    y_u = list()
    avg_u = list()
    for index in range(len(d)):
        if d[index] < avg_d:
            x_l.append(x[index])
            y_l.append(y[index])
            avg_l.append(d[index])
        elif d[index] > avg_d:
            x_u.append(x[index])
            y_u.append(y[index])
            avg_u.append(d[index])

    avg_d = np.average(avg_l)
    avg_l_l = list()
    x_l_l = list()
    y_l_l = list()
    for index in range(len(avg_l)):
        if avg_l[index] < avg_d:
            x_l_l.append(x_l[index])
            y_l_l.append(y_l[index])
            avg_l_l.append(avg_l[index])
    avg_d = np.average(avg_l_l)
    avg_l = list()
    x_l = list()
    y_l = list()
    for index in range(len(avg_l_l)):
        if avg_l_l[index] < avg_d:
            x_l.append(x_l_l[index])
            y_l.append(y_l_l[index])
            avg_l.append(avg_l_l[index])

    f, ax = plt.subplots()
    ax.set_title("min - KL-Divergence (%s)" % len(avg_l))
    ax.set_ylabel('Privacy')
    ax.set_xlabel('Priority')
    points = ax.scatter(x_l, y_l, c=avg_l, s=10, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()
    
    cmap = plt.autumn()

    avg_d = np.average(avg_u)
    avg_u_u = list()
    x_u_u = list()
    y_u_u = list()
    for index in range(len(avg_u)):
        if avg_u[index] > avg_d:
            x_u_u.append(x_u[index])
            y_u_u.append(y_u[index])
            avg_u_u.append(avg_u[index])
    avg_d = np.average(avg_u_u)
    avg_u = list()
    x_u = list()
    y_u = list()
    for index in range(len(avg_u_u)):
        if avg_u_u[index] > avg_d:
            x_u.append(x_u_u[index])
            y_u.append(y_u_u[index])
            avg_u.append(avg_u_u[index])

    f, ax = plt.subplots()
    ax.set_title("Max - KL-Divergence (%s)" % len(avg_u))
    ax.set_ylabel('Privacy')
    ax.set_xlabel('Priority')
    points = ax.scatter(x_u, y_u, c=avg_u, s=10, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()
    """
    '''
    cmap = plt.plasma()

    f, ax = plt.subplots()
    ax.set_title("Time (%s)" % len(t))
    ax.set_ylabel('Privacy')
    ax.set_xlabel('Priority')
    points = ax.scatter(x, y, c=t, s=10, cmap=cmap)
    f.colorbar(points)
    plt.ylim((y_min, y_max))
    plt.show()

    x1 = x.copy()
    y1 = y.copy()
    standard_deviation = np.std(t)
    print("Time")
    while 1:
        m_std = min(t)
        M_std = max(t)
        x1_t = list()
        x1_removed_m = list()
        x1_removed_M = list()
        y1_t = list()
        y1_removed_m = list()
        y1_removed_M = list()
        d_t = list()
        for index in range(len(t)):
            if t[index] == m_std:
                x1_removed_m.append(x1[index])
                y1_removed_m.append(y1[index])
            elif t[index] == M_std:
                x1_removed_M.append(x1[index])
                y1_removed_M.append(y1[index])
            else:
                d_t.append(t[index])
                x1_t.append(x1[index])
                y1_t.append(y1[index])
        standard_deviation_t = np.std(d_t)
        diff = standard_deviation - standard_deviation_t
        print("%s - %s" % (M_std, m_std))
        print("%s - %s = %s" % (standard_deviation, standard_deviation_t, diff))
        if diff > 0.39:
            x1 = x1_t
            y1 = y1_t
            t = d_t
            standard_deviation = standard_deviation_t
        else:
            break

    if len(x) > len(x1):
        f, ax = plt.subplots()
        ax.set_title("Time (%s)" % len(t))
        ax.set_ylabel('Privacy')
        ax.set_xlabel('Priority')
        points = ax.scatter(x1, y1, c=t, s=10, cmap=cmap)
        f.colorbar(points)
        plt.ylim((y_min, y_max))
        plt.show()
    '''
    lista_x = list()
    lista_y = list()
    lista_d = list()
    lista_e = list()
    lista_t = list()
    index = 0
    while index < len(y):
        list_1 = [x[index]]
        #list_2 = [d[index]]
        list_3 = [e[index]]
        #list_4 = [t[index]]
        lista_y.append(y[index])
        index += 1
        counter = 1
        while index < len(y) and y[index] == y[index - 1] and counter < 5:
            list_1.append(x[index])
           # list_2.append(d[index])
            list_3.append(e[index])
           # list_4.append(t[index])
            index += 1
            counter += 1
        lista_x.append(list_1)
       # lista_d.append(list_2)
        lista_e.append(list_3)
       # lista_t.append(list_4)
    y_values = y.copy()
    y_values = list(set(y_values))
    print(str(y_values))
    for y_temp in y_values:
        xe = list()
        ye = list()
        ze = list()
        f, ax = plt.subplots()
        y_p = 0
        x_min = list()
        x_min_t = list()
        for y_index in range(len(lista_y)):
            if lista_y[y_index] == y_temp:
                array = lista_e[y_index]
                array_x = lista_x[y_index]
                min_v = min(array)
                for size_index in range(len(array)):
                    if array[size_index] == min_v:
                        x_min.append(array_x[size_index])
                        x_min_t.append(y_p)
                    else:
                        ye.append(y_p)
                        ze.append(array[size_index] - min_v)
                        xe.append(array_x[size_index])
                y_p += 1
        ax.plot(x_min, x_min_t, marker="x", color="g", linestyle="")
        points = ax.scatter(xe, ye, c=ze, s=10, cmap=plt.plasma())
        ax.set_title("Groups with Privacy = %s" % y_temp)
        ax.set_ylabel("Attempts")
        ax.set_xlabel('Priority')
        f.colorbar(points)
        plt.show()
