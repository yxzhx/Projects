from __future__ import annotations
import random
from typing import Union, Optional, Callable


def comp_int(x: int, y: int) -> bool:
    """
    comprueba si son compatibles 2 fichas en el 2048
    """
    result = False
    if (x == y and x // 2 == y // 2) and x != -1 and y != 1:
        result = True
    return result


def fibo_sec(x: int, y: int) -> bool:
    """
    comprueba si son compatibles 2 fichas en el fibo_2048
    Para saber si compatible, he hecho que el número sumado, z, sea divido entre el maximo de los dos
    números. De manera que observamos que si al dividir por el máximo
    obtenemos un valor que está entre 1.6 y 1.69, por lo que será compatibles con la serie de fibonacci.
    Cada vez que el número sumado sea más grande se acerca más al 1.6.
    Luego, he utilizado está observación para comprobar si son o no compatibles.
    """
    z = x + y
    result = False
    if x == 0 and y == 0:
        result = True
    elif (x == 0 and y == 1) or (x == 1 and y == 0):
        result = True
    elif x == 1 and y == 1:
        result = True
    elif x == 0 or y == 0 and (z // (x + y)) == 1:
        result = True
    if x != 0 and y != 0:
        if (z / max(x, y)) == 1.5:
            result = True
        elif 1.6 == round((z / max(x, y)), 2) or 1.59 < round((z / max(x, y)), 2) < 1.68:
            result = True
    return result


def maximo(n: list[int]) -> int:
    """ funcion que nos devuelve el número más grande de una lista """
    maxi = n[0]
    for x in n:
        #si encuentra otro más grande en la lista se sustituye por esté así sucesivamente
        if maxi <= x:
            maxi = x
    if maxi == -1:
        maxi = 0
    return maxi


def simetria(m: int) -> list[list[None]]:
    """
    me crea una lista de lista de None. Lo utilizo para hacer la traspuesta del tablero en la funcion move_u y move_d.
    """
    tabla = []
    for i in range(m):
        fila = []
        for j in range(m):
            fila.append(None)
        tabla.append(fila)
    return tabla


def lista_inversa(t: list[list[Optional[str]]]) -> list[list[Optional[str]]]:
    """
    funcion que permite que dentro de la lista en cada lista, los últimos vayan los primeros
    y los primeros pasen a ser los últimos. Ej: si tenemos [1, 3, 4, 6] con la funcion
    me devuelve [6, 4, 3, 1]. Es decir, que al final me devuelve invertido.
    """
    result, i, j = [], 0, -1
    while i < len(t):
        fila = []
        while abs(j) < (len(t[0]) + 1):
            fila.append(t[i][j])
            j -= 1
        result.append(fila)
        j = -1
        i += 1
    return result


def condic(tipo: str):
    """
    funcion que lo uso en clase Juego, si metemos en tipo: 2048, el constructor me crea un tablero del 2048 que tiene
    un tamaño y la funcion comp_int donde al hacer los movimientos va a ver si son compatibles o no
    """
    result = 0
    if tipo == '2048':
        result = comp_int
    elif tipo == '2584':
        result = fibo_sec
    return result


class Fila:
    def __init__(self, param: Union[int, list[Optional[int]]], condic: Callable[[int, int], bool]):
        """
        Union[int, list[optional[int]]] hay un int donde en el constructor me va crear
        un tamaño del int que le he metido y si es list[optional[int]] me devolverá la misma lista
        """
        self.condic = condic
        if isinstance(param, int):
            self.fila = [None] * param
        else:
            self.fila = param

    def extrm_l(self) -> list[Optional[int]]:
        """
        funcion que me devuelve una fila movida todo hacia la izquierda
        """
        result = []
        for j in range(len(self.fila)):
            if self.fila[j] is not None:
                result.append(self.fila[j])
        for n in range(len(self.fila)):
            if self.fila[n] is None:
                result.append(self.fila[n])
        return result

    def extrm_r(self) -> list[Optional[int]]:
        """
        funcion que me devuelve una fila movida todo hacia la derecha
        """
        result = []
        for j in range(len(self.fila)):
            if self.fila[j] is None:
                result.append(self.fila[j])
        for n in range(len(self.fila)):
            if self.fila[n] is not None:
                result.append(self.fila[n])
        return result

    def deslizar_l(self) -> list[Optional[int]]:
        """funcion que me desliza hacia la izquierda, teniendo self.condic que comprueba si son compatibles, si lo son
        se me juntan"""
        result = self.fila
        for i in range(len(result)):
            # result es una lista de lista que me devuelve los Nones en -1
            if result[i] is None:
                result[i] = -1
        for j in range(len(result) - 1):
            if self.condic(result[j], result[j + 1]):
                result[j] = result[j] + result[j + 1]
                result[j + 1] = -1
        for h in range(len(result)):
            if result[h] == -1:
                # aquí todos los -1 se convierten otra vez en Nones
                result[h] = None
        return result

    def deslizar_r(self) -> list[Optional[int]]:
        """funcion que me devuelve la lista deslizada hacia la derecha. Tiene la misma estructura que deslizar_l"""
        result, j = self.fila, -1
        for i in range(len(result)):
            if result[i] is None:
                result[i] = -1
        while abs(j) < len(result):
            if self.condic(result[j], result[j - 1]):
                result[j] = result[j] + result[j - 1]
                result[j - 1] = -1
            j -= 1
        for h in range(len(result)):
            if result[h] == -1:
                result[h] = None
        return result

    def point_l(self) -> tuple[int, int]:
        """funcion que me devuelve la puntuacion y el maximo en una Fila cuando se ha deslizado a la izquierda"""
        result, i, p, not_None = self.fila, 0, 0, []
        for i in range(len(result)):
            if result[i] is None:
                # todos los Nones en self.fila se convierten en -1
                result[i] = -1
        for j in range(len(result) - 1):
            if self.condic(result[j], result[j + 1]):
                result[j] = result[j] + result[j + 1]
                result[j + 1] = -1
                p += result[j]
        for g in result:
            # not_None es una lista de numeros que en return me devuelve el número más grande que hay
            not_None.append(g)
        return p, maximo(not_None)

    def point_r(self) -> tuple[int, int]:
        """funcino que me devuelve la puntuacion y el maximo en una Fila cuando se desliza hacia la derecha"""
        result, j, p, not_None = self.fila, -1, 0, []
        for i in range(len(result)):
            if result[i] is None:
                result[i] = -1
        while abs(j) < len(result):
            if self.condic(result[j], result[j - 1]):
                p += result[j] + result[j - 1]
                result[j - 1] = -1
            j -= 1
        for g in result:
            not_None.append(g)
        return p, maximo(not_None)

    def copia(self) -> list[Optional[int]]:
        """funcion que me devuelve una copia de la Fila"""
        result = []
        for i in self.fila:
            result.append(i)
        return result


class Tablero:
    def __init__(self, param: Union[int, list[Fila]], condic: Callable[[int, int], bool]):
        self.condic = condic
        if isinstance(param, int):
            self.size = param
            self.param = [Fila(param, self.condic)] * param
        else:
            self.param = param

    def __str__(self) -> str:
        """funcion que me transforma el Tablero en un str, accediendo a los numeros de la Fila transformandolos en str
        """
        i, result = 0, ''
        while i < len(self.param):
            for j in range(len(self.param)):
                result += str(self.param[i].fila[j]) + '   ' + "\t"
            result += '\n'
            i += 1
        return result

    def traspuesta(self) -> list[list[Optional[int]]]:
        """funcion que me devuelve el tablero traspuesto"""
        fila, tablero = [], []
        for i in range(len(self.param)):
            # fila es una lista de lista de Fila copiada de self.param
            fila.append(self.param[i].copia())
        for i in range(len(fila[0])):
            result = []
            for j in range(len(fila)):
                result.append(fila[j][i])
            tablero.append(result)
        return tablero

    def move_l(self) -> list[Fila]:
        """funcion que me devuelve una lista de Fila deslizada hacia la izquierda"""
        table, tabla = [], []
        for i in range(len(self.param)):
            # primero se desliza todo hacia la izquierda
            self.param[i] = Fila(self.param[i].extrm_l(), self.condic)
        for k in self.param:
            # segundo uso deslizar_l para que se me junten las parejas
            table.append(k.deslizar_l())
        for j in range(len(table)):
            # lo transformo cada lista en Fila
            self.param[j] = Fila(table[j], self.condic)
        for m in self.param:
            # lo muevo otra vez todo hacia la izquierda
            tabla.append(m.extrm_l())
        for i in range(len(tabla)):
            # finalmente lo transformo en Fila para que el self se cambie
            self.param[i] = Fila(tabla[i], self.condic)
        return self.param

    def move_r(self) -> list[Fila]:
        """funcion que me devuelve una lista[Fila] deslizada hacia la derecha. Tiene la misma estructura que move_l"""
        table, tabla = [], []
        for i in range(len(self.param)):
            self.param[i] = Fila(self.param[i].extrm_r(), self.condic)
        for k in self.param:
            table.append(k.deslizar_r())
        for j in range(len(table)):
            self.param[j] = Fila(table[j], self.condic)
        for m in self.param:
            tabla.append(m.extrm_r())
        for i in range(len(tabla)):
            self.param[i] = Fila(tabla[i], self.condic)
        return self.param

    def move_u(self) -> list[Fila]:
        """funcion que me devuelve una lista de Fila deslizada hacia arriba"""
        n, table, result = 0, simetria(len(self.param)), self.traspuesta()
        for i in range(len(result)):
            # result es la traspuesta de self.param, donde self.param se cambia al trasponer.
            self.param[i] = Fila(result[i], self.condic)
        for j in range(len(self.param)):
            # transformo cada Fila de self.param en Fila pero movida hacia la derecha
            self.param[j] = Fila(self.param[j].extrm_l(), self.condic)
            # luego con self.move_l junta las fichas
        self.param = self.move_l()
        while n < len(self.param):
            for m in range(len(self.param)):
                # table es una lista de lista de None usando la funcion simetria
                table[n][m] = self.param[m].fila[n]
            n += 1
        for i in range(len(table)):
            # finalmente lo convierto cada lista en Fila y el self.param se cambia
            self.param[i] = Fila(table[i], self.condic)
        return self.param

    def move_d(self) -> list[Fila]:
        """funcion que me devuelve una lista de Fila deslizada hacia abajo. Tiene la misma estructura que move_u"""
        n, table, result = 0, simetria(len(self.param)), self.traspuesta()
        for i in range(len(result)):
            self.param[i] = Fila(result[i], self.condic)
        for j in range(len(self.param)):
            self.param[j] = Fila(self.param[j].extrm_r(), self.condic)
        self.param = self.move_r()
        while n < len(self.param):
            for m in range(len(self.param)):
                table[n][m] = self.param[m].fila[n]
            n += 1
        for i in range(len(table)):
            self.param[i] = Fila(table[i], self.condic)
        return self.param

    def move_point_l(self) -> tuple[int, int]:
        """funcion que me devuelve la puntuacion y el maximo en un Tablero al mover a la izquierda"""
        puntuacion, result, maxim = 0, [], []
        for i in range(len(self.param)):
            # primero me hace una copia de la fila que lo transformor en Fila para poder aplicar la funcino point_l
            result.append(Fila(self.param[i].copia(), self.condic).point_l())
        for k in range(len(result)):
            puntuacion += result[k][0]
            # maxim me guarda todos los número grandes, donde en return me devuelve el maximo de todo ellos
            maxim.append(result[k][1])
        return puntuacion, maximo(maxim)

    def move_point_r(self) -> tuple[int, int]:
        """funcion que me devuelve la puntuacion y el maximo en un Tablero al mover a la derecha.
        Tiene la misma característica que move_point_l"""
        puntuacion, result, maxim = 0, [], []
        for i in range(len(self.param)):
            result.append(Fila(self.param[i].copia(), self.condic).point_r())
        for k in range(len(result)):
            puntuacion += result[k][0]
            maxim.append(result[k][1])
        return puntuacion, maximo(maxim)

    def move_point_u(self) -> tuple[int, int]:
        """funcion que me devuelve la puntuacion y el maximo en un Tablero al mover hacia arriba.
            Tiene la misma característica que move_point_l"""
        tablero, result = [], self.traspuesta()
        for i in range(len(result)):
            tablero.append(Fila(result[i], self.condic))
        for j in range(len(tablero)):
            tablero[j] = Fila(tablero[j].extrm_l(), self.condic)
            # en return transformo tablero en Tablero para poder usar move_point_l y tener la puntuacion y el maximo
        return Tablero(tablero, self.condic).move_point_l()

    def move_point_d(self) -> tuple[int, int]:
        """funcion que me devuelve la puntuacion y el maximo en un Tablero al mover hacia abajo.
            Tiene la misma característica que move_point_l"""
        tablero, result = [], self.traspuesta()
        for i in range(len(result)):
            tablero.append(Fila(result[i], self.condic))
        for j in range(len(tablero)):
            tablero[j] = Fila(tablero[j].extrm_r(), self.condic)
        return Tablero(tablero, self.condic).move_point_r()

    def tablero_aleatorio(self) -> Tablero:
        """funcion que me devuelve un tablero aleatorio dependiendo del tipo de tablero"""
        tablero = []
        x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        x1, y1 = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        for i in range(self.size):
            a = []
            for j in range(self.size):
                # a es una lista de None
                a.append(None)
            tablero.append(a)
        if self.condic == comp_int:
            tablero[x][y], tablero[x1][y1] = random.choice([2, 2]), random.choice([2, 2, 2, 2, 4])
        elif self.condic == fibo_sec:
            tablero[x][y], tablero[x1][y1] = random.choice([1, 1]), random.choice([1, 1, 0, 1, 1, 1, 1, 1, 1])
        for k in range(len(tablero)):
            self.param[k] = Fila(tablero[k], self.condic)
        return Tablero(self.param, self.condic)

    def save(self) -> None:
        """funcion que me guarda en un archivo dependiendo del tipo de juego, el tablero se convierte en str con
        la funcion __str__()"""
        if self.condic == comp_int:
            file_name = 'clásico'
        else:
            file_name = 'venv/fibo'
        f = open(file_name, 'a')
        f.write('\n')
        f.write(self.__str__())
        f.close()

    def load(self) -> Tablero:
        """funcion que me trae el tablero en un archivo"""
        result, tablero, ordenada, partida = [], [], [], []
        i, j = -1, -1
        if self.condic == comp_int:
            file_name = 'clásico'
        else:
            file_name = 'venv/fibo'
        f = open(file_name, 'r')
        fila = f.readlines()
        for f in fila:
            # como fila es una lista de todas las lineas
            # lo guardo en un result quitando los espacios
            result.append(f.split())
        for i in range(len(result)):
            # result es una lista de lista de str y None, aquellos que tienen longitud distinto al tamaño del tablero
            # guardado con save se convierte en None
            if len(result[i]) != self.size:
                result[i] = None
        while result[i] is not None:
            # los que no son None será nuestro tablero, pero que esta al revés
            tablero.append(result[i])
            i -= 1
        while abs(j) < len(tablero) + 1:
            ordenada.append(tablero[j])
            # ordenada ya me devuelve el tablero original ordenándola
            j -= 1
        for k in range(len(ordenada)):
            for m in range(len(ordenada)):
                # como todavía son str en ordenada, pues lo convierto todo en no str, si es 'None' es None
                # si es un numero se convierte en un int
                if ordenada[k][m] == 'None':
                    ordenada[k][m] = None
                elif ordenada[k][m] != 'None':
                    ordenada[k][m] = int(ordenada[k][m])
        for j in range(len(ordenada)):
            partida.append(Fila(ordenada[j], self.condic))
        return Tablero(partida, self.condic)


class Juego:
    def __init__(self, tam: int | Tablero, tipo: str):
        """el constructor crea un tablero aleatorio o toma el tablero que queremos"""
        self.tam, self.tipo, self.puntos, self.mayor = tam, tipo, 0, 0
        if isinstance(tam, int):
            # en el constructor self.tablero es un tablero aleatorio
            self.tablero = Tablero(tam, condic(tipo)).tablero_aleatorio()
        elif isinstance(tam, Tablero):
            self.tablero = tam

    def empty(self) -> None:
        """funcion que me devuelve las posiciones de los None y rellena una casilla vacia al azar con un 2 o 1"""
        result = []
        for i in range(len(self.tablero.param)):
            for j in range(len(self.tablero.param)):
                if self.tablero.param[i].fila[j] is None:
                    result.append([i, j])
                    # result es una lista donde hay lista de los posiciones de los None
        pos = random.choice(result)
        # con pos me devuelve una lista al azar con la posicion
        if self.tipo == '2048':
            self.tablero.param[pos[0]].fila[pos[1]] = 2
        elif self.tipo == '2584':
            self.tablero.param[pos[0]].fila[pos[1]] = random.choice([1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1])

    def hacer_jugada(self, accion: str) -> None:
        """funcion que hace ejecutar los movimientos"""
        cond = condic(self.tipo)
        if accion == 'l':
            Juego(Tablero(self.tablero.move_l(), cond), self.tipo)
        elif accion == 'r':
            Juego(Tablero(self.tablero.move_r(), cond), self.tipo)
        elif accion == 'u':
            Juego(Tablero(self.tablero.move_u(), cond), self.tipo)
        elif accion == 'd':
            Juego(Tablero(self.tablero.move_d(), cond), self.tipo)
        else:
            print(f"wrong action")

    def archivo(self) -> str:
        """funcion que devuelve un archivo segun el tipo de juego estamos jugando"""
        if self.tipo == '2048':
            file_name = 'clásico'
        else:
            file_name = 'venv/fibo'
        return file_name

    def puntuacion(self, accion: str) -> int:
        """funcion que me devuelve la puntuacion cuando estamos jugando"""
        number, punto, k, m = [], [], -1, -1
        change = ''
        if accion == 'l':
            self.puntos += self.tablero.move_point_l()[0]
        elif accion == 'r':
            self.puntos += self.tablero.move_point_r()[0]
        elif accion == 'u':
            self.puntos += self.tablero.move_point_u()[0]
        elif accion == 'd':
            self.puntos += self.tablero.move_point_d()[0]
        elif accion == 'save':
            # si accion es save guardamos la puntuacion en un archivo usando la funcion archivo
            f = open(self.archivo(), 'a')
            f.write('\n')
            f.write('puntuacion:' + '' + str(self.puntos))
            f.close()
        elif accion == 'continuar':
            # si queremos continuar jugando el juego traigo del archivo la puntuacion
            f = open(self.archivo(), 'r')
            # en la linea -7 es donde está escrito la puntuacion
            linea = f.readlines()[-7].split()
            for i in linea[0]:
                for j in i:
                    number.append(j)
            while number[k] != ':':
                punto.append(number[k])
                k -= 1
            while abs(m) < (len(punto) + 1):
                change += punto[m]
                m -= 1
            self.puntos += int(change)
        return self.puntos

    def mayor_number(self, accion: str) -> int:
        """funcion que me devuelve el número más grande que hay en el tablero mientras estamos jugando"""
        if accion == 'l':
            self.mayor = self.tablero.move_point_l()[1]
        elif accion == 'r':
            self.mayor = self.tablero.move_point_r()[1]
        elif accion == 'u':
            self.mayor = self.tablero.move_point_u()[1]
        elif accion == 'd':
            self.mayor = self.tablero.move_point_d()[1]
        elif accion == 'save':
            # si queremos guardar el archivo abro el archivo y guardo el mayor numero
            f = open(self.archivo(), 'a')
            f.write('\n')
            f.write('mayor numero:' + '' + str(self.mayor) + '\n')
            f.close()
        return self.mayor

    def final(self) -> bool:
        """funcion que me devuelve un True si hay fichas que se pueden juntar o que hay un 2048 o 2584 o que hay
        casillas vacías (None) y si no me devuelve False"""
        tab, fila, result = [], [], False
        for i in range(len(self.tablero.param)):
            for j in range(len(self.tablero.param)):
                fila.append(self.tablero.param[i].fila[j])
            tab.append(fila)
        for i in range(len(tab)):
            for j in range(len(tab)):
                if tab[i][j] is None:
                    tab[i][j] = -1
        for i in range(len(tab)):
            for j in range(len(tab) - 1):
                if self.tablero.condic(tab[i][j], tab[i][j + 1]) is True or self.tablero.condic(tab[j][i], tab[j + 1][i]) is True:
                    result = True
        for i in range(len(tab)):
            for j in range(len(tab)):
                if self.tablero.param[i].fila[j] == -1 or 2048 or 2584:
                    result = True
        return result


class Partida:
    def __init__(self, tam: int, tipo_juego: str):
        self.tam, self.tipo_juego = tam, tipo_juego
        self.tablero = Juego(tam, self.tipo_juego)

    def jugar(self):
        """funcion que me permite ejecutar el juego"""
        start = input(f"¿tablero nuevo o continuar partida?: ")
        if start == 'nuevo':
            # si es nuevo creo un nuevo tablero
            self.tablero = Juego(self.tam, self.tipo_juego)
            print(self.tablero.tablero.__str__())
        elif start == 'continuar':
            # si es continuar traigo la puntuacion del archivo y el tablero del juego usando load
            self.tablero.puntuacion(start)
            self.tablero = Juego(Tablero(self.tam, condic(self.tipo_juego)).load(), self.tipo_juego)
            print(self.tablero.tablero.__str__())
        while self.tablero.final():
            move = input(f"mover: ")
            # print aparece en la pantalla la puntuacion y el mayor valor mientras estamos jugando
            print(f"puntuacion: {self.tablero.puntuacion(move)}  mayor valor: {self.tablero.mayor_number(move)}")
            # si move es save, el tablero lo guardamos con la funcion save y devuelve un str de que se finalizado
            if move == 'save':
                self.tablero.tablero.save()
                return f"se ha finalizado la partida, se ha guardado la partida"
            elif move == 'end':
                return None
            else:
                self.tablero.hacer_jugada(move)
                self.tablero.empty()
                print(self.tablero.tablero.__str__())
                self.tablero.final()


def tests() -> None:
    print(f" fibo_sec(3, 3) devuelve: {fibo_sec(3, 3)} y debería devolver False")
    print(f" fibo_sec(21, 13) devuelve: {fibo_sec(21, 13)} y debería devolver True")
    f1 = Fila([2, 2, 4, None], comp_int)
    f2 = Fila([None, None, 4, 8], comp_int)
    f3 = Fila([None, None, None, None], comp_int)
    f4 = Fila([16, 2, None, None], comp_int)
    tab1 = Tablero([f1, f2, f3, f4], comp_int)
    tab2 = Juego(tab1, '2048')
    print(f"tab1.mover_point_l() devuelve: {tab1.move_point_l()} y debería devolver (4, 16)")
    print(f"tab1.mover_point_d() devuelve: {tab1.move_point_d()} y debería devolver (12, 16)")
    print(f"f1.deslizar_l() devuelve: {f2.extrm_l()} y debería devolver [4, 8, None,None] ")
    print(f"tab1.mover_l() devuelve: {tab1.move_l()} \n{tab1.__str__()} y debería devolver una lista de Fila "
          f"f1 = Fila([4, 4, None, None], f2 = Fila([4, 8, None, None]), f3 = ([None, None, None, None])"
          f"f4 = Fila([16, 2, None, None]) ")
    print(f"tab2.mayor_number() devuelve: {tab2.mayor_number('l')} y debería devolver 16")


tests()
