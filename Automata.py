import networkx as nx
import matplotlib.pyplot as plt

class Automata():

    def __init__(self):

        self.__cinta = ""
        self.__posicion_cabezal = 1
        self.__estados = {'p', 'q', 'r'}
        self.__transiciones = {

            ('p', 'a'): ('p', 'a', 'D'),
            ('p', 'b'): ('p', 'a', 'D'),
            ('p', '#'): ('q', '#', 'I'),
            ('q', 'a'): ('q', 'a', 'I'),
            ('q', '#'): ('r', '#', 'D')

        }
        self.__estado_inicial = 'p'
        self.__estados_finales = {'r'}
        self.__estado_actual = 'p'

        self.posVertices = {

        'p': (2, 1),
        'q': (1, 1),
        'r': (2, -1)

        }

        self.edgeColors = {

            ('p', 'p'): 'b',
            ('p', 'q'): 'b',
            ('q', 'q'): 'b',
            ('q', 'r'): 'b'

        }

        self.__grafo = nx.DiGraph()
        self.__grafo.add_nodes_from(self.__estados)
        self.__grafo.add_edges_from(self.__generarAristas())

        plt.rcParams['toolbar'] = 'None'

    def __generarAristas(self):

        aristas = set()

        aristas.add(('p', 'p'))
        aristas.add(('p', 'q'))
        aristas.add(('q', 'q'))
        aristas.add(('q', 'r'))

        return aristas

    def __iniciarGrafo(self, velocidad):

        nx.draw(self.__grafo, self.posVertices, with_labels = True, node_color = "red", node_size = 500)
        nx.draw_networkx_edges(self.__grafo, self.posVertices)
        plt.pause(1 / velocidad)

    def __actualizarNodos(self, estado, velocidad):

        if (estado != 'r'):

            nx.draw(self.__grafo, self.posVertices, with_labels = True, node_color = ['blue' if node == estado else 'red' for node in self.__grafo.nodes()], node_size = 500)
            plt.pause(1 / velocidad)
            self.__iniciarGrafo(velocidad)

        else:

            nx.draw(self.__grafo, self.posVertices, with_labels = True, node_color = ['blue' if node == estado else 'red' for node in self.__grafo.nodes()], node_size = 500)
            plt.pause(3 / velocidad)
            self.__iniciarGrafo(velocidad)

    def __actualizarAristas(self, estadoInicial, estadoFinal, velocidad):

        nx.draw_networkx_edges(self.__grafo, self.posVertices, edge_color = ['blue' if edge == (estadoInicial, estadoFinal) else 'black' for edge in self.__grafo.edges()])
        plt.pause(1 / velocidad)

    def procesar(self, palabra, velocidad):

        self.__cinta = list(palabra)

        self.__iniciarGrafo(velocidad)
        self.__actualizarNodos(self.__estado_actual, velocidad)

        while self.__estado_actual not in self.__estados_finales:

            caracter_actual = self.__cinta[self.__posicion_cabezal]
            transicion = self.__transiciones.get((self.__estado_actual, caracter_actual), None)

            if transicion is None:

                return False

            estado_siguiente, caracter_nuevo, direccion = transicion
            self.__cinta[self.__posicion_cabezal] = caracter_nuevo
            estado_anterior = self.__estado_actual
            self.__estado_actual = estado_siguiente

            self.__actualizarAristas(estado_anterior, self.__estado_actual, velocidad)
            self.__actualizarNodos(self.__estado_actual, velocidad)

            if direccion == 'D':

                self.__posicion_cabezal += 1

            elif direccion == 'I':

                self.__posicion_cabezal -= 1

            else:

                return False

        self.__posicion_cabezal = 1
        self.__estado_actual = "p"

        return True
