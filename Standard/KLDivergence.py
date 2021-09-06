import itertools

"""
    classe per il calcolo della funzione di distribuzione
    di probabilità effettiva e stimata e per il calcolo
    delle combinazioni degli item sensibili nelle celle C
"""


def compute_act_s_in_c(dataframe_bandizzato, listaQID, valoriQID, itemSensibile):
    """
        metodo per il calcolo della pdf ("Probability
        Distribution Function")
        dato il sensitive item s
        per una specifica cella C.
        act_s_in_c = n° occorrenze di s in C / n° occorrenze di s in T
    """

    # nel caso in cui ci sia un solo item sensibile
    if type(itemSensibile) is int:
        row_sensibile = dataframe_bandizzato[dataframe_bandizzato[itemSensibile] == 1].index.tolist()
        number_s_t = len(row_sensibile)
        set_row = set(row_sensibile)

        # controllo di tutti i valori nella lista dei QID
        for i in range(0, len(listaQID)):
            set_temp = dataframe_bandizzato[dataframe_bandizzato[listaQID[i]] == valoriQID[i]].index.tolist()
            set_temp = set(set_temp)
            set_row = set_row.intersection(set_temp)
        number_s_c = len(set_row)
        if number_s_t > 0:
            return number_s_c / number_s_t
        else:
            return 0
    # nel caso in cui abbia una lista di item sensibili
    elif type(itemSensibile) is list:
        listOccurrence = list()
        for s in itemSensibile:
            value = compute_act_s_in_c(dataframe_bandizzato, listaQID, valoriQID, s)
            listOccurrence.append(value)
        return listOccurrence
    else:
        return 0


def compute_est_s_in_c(dataframe_bandizzato, gruppi_sd, lista_gruppi, listaQID, valoriQID, itemSensibile):
    """
        metodo per il calcolo della pdf ("Probability
        Distribution Function")  stimata
        dato il sensitive item s
        per una specifica cella C
        est_s_in_c = a*b/|G|
        dove a è il numero di item sensibibile nel gruppo G
        b il numero di transizioni che matchano i QID nel gruppo
        |G| è la cardinalità del gruppo
    """
    value_tot = 0

    # in ogni gruppo trovo n° transazioni che matchano QID
    for index in range(0, len(lista_gruppi)):
        cardinality_G = len(lista_gruppi[index])
        set_row = set(lista_gruppi[index].index.tolist())
        for i in range(0, len(listaQID)):
            set_temp = lista_gruppi[index][lista_gruppi[index][listaQID[i]] == valoriQID[i]].index.tolist()
            set_temp = set(set_temp)

            # numero di occorrenze di s in C (dove le condizioni listaQID sono verificate)
            set_row = set_row.intersection(set_temp)

        # calcolo b & a per il gruppo[index]
        value_b = len(set_row)
        value_a = gruppi_sd[index][itemSensibile]
        value_tot = value_tot + ((value_a * value_b) / cardinality_G)

    # calcolo b*a/|G|
    row_sensibile = dataframe_bandizzato[dataframe_bandizzato[itemSensibile] == 1].index.tolist()
    number_s_t = len(row_sensibile)
    if number_s_t > 0:
        value_tot = value_tot / number_s_t
    else:
        value_tot = 0
    return value_tot


def get_all_combination_of_n(n):
    """
        metodo per il calcolo di tutte le
        2^n combinazioni derivanti dal
        coinvolgimento di n QID all'interno
        delle transazioni sensibili
    """
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    return lst
