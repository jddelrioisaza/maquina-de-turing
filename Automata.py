class Automata():

    def __init__(self, cinta):

        self.__cinta = cinta
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

    def procesar(self):

        while self.__estado_actual not in self.__estados_finales:

            caracter_actual = self.__cinta[self.__posicion_cabezal]
            transicion = self.__transiciones.get((self.__estado_actual, caracter_actual), None)

            if transicion is None:

                return False

            estado_siguiente, caracter_nuevo, direccion = transicion
            self.__cinta[self.__posicion_cabezal] = caracter_nuevo
            self.__estado_actual = estado_siguiente

            if direccion == 'D':

                self.__posicion_cabezal += 1

            elif direccion == 'I':

                self.__posicion_cabezal -= 1

            else:

                return False

        return True

automata = Automata(list("#abababababababa#"))
print(automata.procesar())
