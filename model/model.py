import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.lista_vertici = []
        self.costo_cammino_max = 0
        self.archi_cammino = []

    def crea_grafo(self):
        self.grafo.clear()
        # Cancello diz o liste se le ho inizializzate se uno schiacca due volte pulsante non ci sono problemi
        self.lista_vertici.clear()
        vertici = DAO.get_vertici()
        for v in vertici:
            self.lista_vertici.append(v)
            self.grafo.add_node(v)
        archi = DAO.get_archi()
        for a in archi:
            self.grafo.add_edge(a[0], a[1], weight=a[2])

    # Ritorno lunghezza nodi e archi
    def num_nodi(self):
        return len(self.grafo.nodes)

    def num_archi(self):
        return len(self.grafo.edges)

    def min_max_archi(self):
        min = 10000000
        max = -10000000
        for arco in self.grafo.edges(data=True):
            peso = float(arco[2]["weight"])
            if peso > max:
                max = peso
            elif peso < min:
                min = peso
        return min, max

    def soglia(self, soglia):
        inf = 0
        sup = 0
        for arco in self.grafo.edges(data=True):
            peso = float(arco[2]["weight"])
            if peso > soglia:
                sup += 1
            elif peso < soglia:
                inf += 1
        return inf, sup

    def ricerca_cammino(self, soglia):
        for nodo in self.grafo.nodes:
            self.ricorsione(soglia, [nodo], [])
        return self.costo_cammino_max, self.archi_cammino
    def ricorsione(self, soglia, cammino_attuale, lista_archi):
        if self.get_peso_cammino(lista_archi) > self.costo_cammino_max:
            self.costo_cammino_max = copy.deepcopy(self.get_peso_cammino(lista_archi))
            self.archi_cammino = copy.deepcopy(lista_archi)

        for nodo in self.grafo.successors(cammino_attuale[-1]):
            if self.grafo[cammino_attuale[-1]][nodo]["weight"] > soglia and [cammino_attuale[-1], nodo, self.grafo[cammino_attuale[-1]][nodo]["weight"]] not in lista_archi:
                lista_archi.append([cammino_attuale[-1], nodo, self.grafo[cammino_attuale[-1]][nodo]["weight"]])
                cammino_attuale.append(nodo)
                self.ricorsione(soglia, cammino_attuale, lista_archi)
                cammino_attuale.pop()
                lista_archi.pop()


    def get_peso_cammino(self, lista_archi):
        somma = 0
        for arco in lista_archi:
            somma += arco[2]
        return somma

