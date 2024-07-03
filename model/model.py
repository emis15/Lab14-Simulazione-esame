import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.bestPath = []
        self.bestPeso = 0
        self.minimo = 1000
        self.massimo = 0

    def creaGrafo (self):
        #self.grafo.add_nodes_from(DAO.getNodes())
        #self.grafo.add_edges_from(DAO.getEdges())
       # for e in self.grafo.edges(data=True):
            # e[2]['weight'] = DAO.getPeso(e[0], e[1])
        self.grafo.add_weighted_edges_from(DAO.getAllPesi())
        self.pesoMinimo()
        self.pesoMassimo()

    def contaArchi(self, soglia):
        archiMinore = []
        archiMaggiore = []
        for e in self.grafo.edges(data=True):
            if e[2]['weight'] < soglia:
                archiMinore.append(e)
            elif e[2]['weight'] > soglia:
                archiMaggiore.append(e)
        return archiMinore, archiMaggiore

    def cercaPercorso(self, soglia):
        self.bestPath = []
        self.bestPeso = 0
        for e in self.grafo.edges(data=True):
            if e[2]['weight'] > soglia:
                parziale = []
                parziale.append(e)
                self.ricorsione(parziale, e[2]['weight'])
        return

    def ricorsione(self, parziale, peso):
        archiAmmissibili = []
        for e in self.grafo.edges(parziale[-1][1], data=True):
            if e[2]['weight'] > peso and self.checkNode(parziale, e[1]):
                archiAmmissibili.append(e)
        if len(archiAmmissibili) == 0:
            if len(parziale) > len(self.bestPath):
                self.bestPath = copy.deepcopy(parziale)
                self.bestPeso = self.calcolaPeso(parziale)
            return
        sorted(archiAmmissibili, key=lambda x: x[2]['weight'])
        for e in archiAmmissibili:
            parziale.append(e)
            self.ricorsione(parziale, e[2]['weight'])
            parziale.pop()
        return

    def checkNode(self, lista, nodo):
        check = True
        for e in lista:
            if e[0]==nodo or e[1]==nodo:
                check = False
        return check
    def calcolaPeso(self, lista):
        weight = 0
        for e in lista:
            weight += e[2]['weight']
        return weight
    def numNodes(self):
        return len(self.grafo.nodes)

    def numEdges(self):
        return len(self.grafo.edges)

    def pesoMinimo(self):
        minimo = 1000
        for e in self.grafo.edges(data=True):
            if e[2]['weight']<minimo:
                minimo = e[2]['weight']
        self.minimo = minimo

    def pesoMassimo(self):
        massimo = 0
        for e in self.grafo.edges(data=True):
            if e[2]['weight']>massimo:
                massimo = e[2]['weight']
        self.massimo = massimo

