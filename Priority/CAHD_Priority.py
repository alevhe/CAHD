import numpy as np
import operator


class CAHDalgorithm:
    dataframe_originale = None
    id_sensitive_transaction = None
    dataframe_bandizzato = None
    items_sensibili = None
    grado_privacy = None
    alfa = None
    hist = None
    dict_group = None
    lista_gruppi = None
    sd_gruppi = None
    QID_items = None
    priority_grade = None
    flagErr = None
    """
        Implementazione utilizzando un parametro chiamato priority
        utilizzato nella formazione dei gruppi per favorire l'inserimento di righe con dati sensibili
        per evitare che l'ultimo gruppo non soddisfi i requisiti di privacy a causa dell'alto numero di righe sensibili
    """
    def __init__(self, dataframe=None, grado_privacy=5, alfa=3, priority_grade=0):

        self.dataframe_originale = dataframe.dataframe_bandizzato.copy()
        self.items_sensibili = dataframe.lista_sensibili
        self.nome_item = dataframe.items_final
        self.grado_privacy = grado_privacy
        self.alfa = alfa
        self.QID_items = [x for x in list(self.dataframe_originale) if x not in self.items_sensibili]
        self.priority_grade = priority_grade
        self.hist = dict(self.dataframe_originale[self.items_sensibili].sum())

    def check_grado_privacy(self, grado_privacy):
        value = max(self.hist.values())
        if value * grado_privacy > len(self.dataframe_originale):
            return False
        return True

    def check_conflict(self, row_i, position_j):
        row_j = list(self.dataframe_bandizzato.iloc[position_j][self.items_sensibili])
        for position in range(len(self.items_sensibili)):
            if row_i[position] + row_j[position] > 1:
                return True
        return False

    def select_best_transactions(self, candidate_list, transaction_target):
        distance = list()
        list1 = self.dataframe_bandizzato.iloc[transaction_target][self.QID_items]
        for row in candidate_list:
            list2 = self.dataframe_bandizzato.iloc[row][self.QID_items]
            similarity = [(x and y) for x, y in zip(list1, list2)]
            # priority: il numero di item sensibili presenti in 'row'
            priority = sum(self.dataframe_bandizzato.iloc[row][self.items_sensibili])
            distance.append(sum(similarity) + priority * self.priority_grade)

        best_rows = list()
        for i in range(self.grado_privacy - 1):
            max_index, max_value = max(enumerate(distance), key=operator.itemgetter(1))
            best_rows.append(candidate_list[max_index])
            distance[max_index] = -1
        return best_rows

    def check_list(self, i, indice_transazione_sensibile, k, lc):
        row_i = list(self.dataframe_bandizzato.iloc[i][self.items_sensibili])
        if self.check_conflict(row_i, indice_transazione_sensibile):
            k = k + 1
        else:
            conflitto_lista = False
            for index in lc:
                if self.check_conflict(row_i, index):
                    conflitto_lista = True
                    break
            if not conflitto_lista:
                lc.append(i)
            else:
                k = k + 1
        return k

    def compute_candidate_list(self, indice_transizione_sensibile):
        alpha_p = self.alfa * self.grado_privacy
        lc = list()  # lista candidate
        k = 1
        i = indice_transizione_sensibile - 1
        while i > max(indice_transizione_sensibile - alpha_p - k, -1):
            k = self.check_list(i, indice_transizione_sensibile, k, lc)
            i -= 1

        k = 1
        i = indice_transizione_sensibile + 1
        while i < min(indice_transizione_sensibile + alpha_p + k, len(self.dataframe_bandizzato)):
            k = self.check_list(i, indice_transizione_sensibile, k, lc)
            i += 1
        error = False
        if len(lc) < self.grado_privacy:
            error = True
        return lc, error

    def CAHD_algorithm(self, analysis=False):
        """
        soddisfabile = False
        temp_privacy = self.grado_privacy

        while not soddisfabile and temp_privacy > 0:
            soddisfabile = self.check_grado_privacy(temp_privacy)
            if not soddisfabile:
                temp_privacy -= 1

        self.grado_privacy = temp_privacy
        if self.grado_privacy == 1:
            print("Il grado massimo di privacy soddifacibile è 1, non garantisce perciò alcuna privacy.")
            return False
        """
        if not self.check_grado_privacy(self.grado_privacy): return False

        dict_group = list()

        self.id_sensitive_transaction = self.dataframe_originale.iloc[
            list(set(list(np.where(self.dataframe_originale[self.items_sensibili] == 1)[0])))].index

        lista_gruppi = list()
        sd_gruppi = list()

        self.dataframe_bandizzato = self.dataframe_originale.copy()
        id_sensitive_transaction = np.random.permutation(self.id_sensitive_transaction)
        remaining = len(self.dataframe_bandizzato)
        ts_index = 0
        while ts_index < len(id_sensitive_transaction):
            q = id_sensitive_transaction[ts_index]
            t = self.dataframe_bandizzato.index.get_loc(q)
            lc, errore = self.compute_candidate_list(t)
            if not errore:
                group = self.select_best_transactions(lc, t)
                group.append(t)

                selected_sensitive_items = self.dataframe_bandizzato.iloc[group][self.items_sensibili].sum()
                temp_hist = self.hist.copy()

                for index in selected_sensitive_items.index:
                    temp_hist[index] -= selected_sensitive_items.loc[index]

                th_max = max(temp_hist.values())
                if th_max * self.grado_privacy > remaining - len(group):
                    ts_index += 1
                else:
                    self.hist = temp_hist.copy()
                    label_group = self.dataframe_bandizzato.iloc[group].index
                    id_sensitive_transaction = [x for x in id_sensitive_transaction if x not in label_group]
                    dict_group.append(self.dataframe_bandizzato.index[group])
                    lista_gruppi.append(
                        self.dataframe_bandizzato.loc[list(self.dataframe_bandizzato.index[group]), self.QID_items])

                    # aggiungo somma item sensibili relativi al gruppo iesimo
                    sd_gruppi.append(selected_sensitive_items)

                    self.dataframe_bandizzato = self.dataframe_bandizzato.drop(
                        list(self.dataframe_bandizzato.index[group]))

                    remaining = len(self.dataframe_bandizzato.index)
            else:
                ts_index += 1
        selected_sensitive_items = self.dataframe_bandizzato[self.items_sensibili].sum()
        max_v = max(dict(selected_sensitive_items).values())
        if max_v * self.grado_privacy <= len(self.dataframe_bandizzato):
            lista_gruppi.append(self.dataframe_bandizzato[self.QID_items])
            dict_group.append(self.dataframe_bandizzato.index)
            sd_gruppi.append(selected_sensitive_items)
            self.dataframe_bandizzato = None
            self.sd_gruppi = sd_gruppi
            self.lista_gruppi = lista_gruppi
            self.dict_group = dict_group
            return True
        else:
            print("Ultimo gruppo NON soddisfa.")
            self.flagErr = True
            return False
