# definizione
class Printer:
    cahd = None
    bm = None

    # inizializzazione
    def __init__(self, cahd=None, bm=None):
        self.cahd = cahd
        self.bm = bm

    # metodo per la stampa dei gruppi anonimizzati
    def stampa_gruppi(self):
        label = "   "

        # labelizzazione dei dati della matrice
        for t in range(len(str(self.bm.size))):
            label += " "
        labels_size = list()
        for c in self.cahd.lista_gruppi[0].columns:
            temp = self.bm.items_final.get(c)
            label += "  " + temp
            labels_size.append(len(temp))
        label += "    "
        for j, v in self.cahd.sd_gruppi[0].iteritems():
            temp = self.bm.items_final.get(j)
            label += "  " + temp
            labels_size.append(len(temp))
        print(label)
        print("")

        # formattazione  e stampa output a schermo
        for i in range(len(self.cahd.lista_gruppi)):
            group_indexes = self.cahd.lista_gruppi[i].index
            group_position = 0
            for index in group_indexes:
                row = str(index)
                dbm = self.cahd.lista_gruppi[i].loc[index]
                single_transaction = list(dbm)
                data = 0
                a_l = len(row)
                b_l = len(str(self.bm.size))
                for t in range(max(b_l - a_l, 0)):
                    row += " "
                row += "   "
                for transaction in single_transaction:
                    row += "  " + str(transaction)
                    for d in range(max(labels_size[data] - len(str(transaction)), 0)):
                        row += " "
                    data += 1
                if group_position == 0:
                    row += "    "
                    data = 0
                    for j, v in self.cahd.sd_gruppi[i].iteritems():
                        row += "  " + str(v)
                        for d in range(max(labels_size[data] - len(str(v)), 0)):
                            row += " "
                        data += 1
                print(row)
                group_position += 1
            print("")

    # metodo per controllo integrità dei dati
    def controllo_dati(self, control=False):
        errore = 0

        # controllo riga per riga che i QID siano corretti e segno, nel caso, il numero di errori
        for i in range(len(self.cahd.lista_gruppi)):
            row = str(i) + " ||  QID : "
            group_rows = self.cahd.dict_group[i]
            initial_dataframe = self.bm.df_square_complete.loc[group_rows][self.cahd.QID_items]
            final_dataframe = self.cahd.lista_gruppi[i]
            final_dataframe = final_dataframe.loc[group_rows]

            # se non sono presenti errori nel campionamento
            if initial_dataframe.equals(final_dataframe):
                row += "ok"
            else:

                # se sono presenti errori nel campionamento
                row += "KOOO"
                errore += 1
            row += " || SENSITIVE : "
            initial_sensitive = self.bm.df_square_complete.loc[group_rows][self.bm.lista_sensibili].sum()

            # controllo che i sensitive item siano corretti e segno, nel caso, il numero di errori
            for j in self.bm.lista_sensibili:
                initial_sensitive[j] -= self.cahd.sd_gruppi[i][j]
            err = False
            for j in initial_sensitive:
                if j != 0:
                    err = True
                    break
            if err:
                row += "KOOO"
                errore += 1
            else:
                row += "ok"
            if control:
                print(row)
        return errore
