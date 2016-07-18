#Trabajo realizado por: Rodriguez Calvo, Sergio.
#DNI: 
#Curso y grupo: Grado en Ingenieria del Software, 3º Grupo 1
#Asignatura: Inteligencia Artificial

#En este proyecto vamos a utilizar la logica clausal con variables, es decir, funciones. Por ello vamos a necesitar
#por un lado una forma de representar las funciones, por otro las clausulas y por ultimo las variables.

#Para ello vamos a utilizar clases, las cuales contendran toda la informacion necesarias para la representacion
#del problema del que se encarga. Por ejemplo, las fucniones contendra el nombre de la funcion y los parametros de la misma
#, pero ademas funciones que permitan conocer la aridad, realizar unificaciones, etc. En los algoritmos he trabajo con
#listas siempre.

#Como bibliografia he utilizado las transparencias utilizadas en clase, proporcionadas por el profesor de la asignatura,
#utilizado para aclarar conceptos de logica clausal y obtener el algoritmo de unificacion, y algunos ejemplos
#de unificacion para comprobar dicho algoritmo. El resto de informacion la he extraido del propio documento aportado 
#para la realizacion de este trabajo, a traves del cual he inferido los algoritmos para realizar tanto absorcion,
#identificacion, intra-construccion e inter-construccion, asi como, realizar los ejemplos. Tambien he acudido a tutorias
#para resolver dudas puntuales sobre el problema. Por ultimo, he resulto dudas con algunos compañeros, siempre contrastando
#resultados obtenidos como manera de comprobar los algoritmos.

#A lo largo del codigo encontrara reseñas sobre las decisiones tomadas, como por ejemplo, en la identificacion me he dado 
#cuenta que solo hay que unificar las cabezas de ambas clausulas. Todas las funciones y clases tienen comentarios
#al inicio explicando que se quiere hacer, y en caso necesario, como funciona. Ademas, el codigo en los algoritmos principales
#(absorcion, ...) cuenta con comentario desodorante, que si bien no se debe utilizar, en este caso lo creo combeniente
#para explicar porque hago el algoritmo de esa manera.

#EL FICHERO ESTA DIVIDIDO EN 3 PARTES: FUNCIONES (METODOS), CLASES Y PRUEBAS. DE ESTE MODO ENCONTRAMOS CADA COSA EN SU SITIO.

"""IMPORTS"""
import random

"""FUNCIONES================================================================================================================"""
#Funciones

def esVariable(parametro):
    """Metodo que recibe un parametro que tendremos que identificar como Funcion, Variable constante o Variable no constante.
    De hecho, lo que entendemos como variables es la variable no constante, algo del tipo 'x' no 'X', '0' o 'f(x)'."""
    if type(parametro) == Funcion: 
        return bool(0)
    elif type(parametro) == Variable and parametro.esConstante():
        return bool(0)
    else:
        return bool(1)
                    
def componer(tita, sigma):
    """Funcion que realiza lo que se describe a continuacion, si x->y y luego tenemos y->a pues devolvemos directamente x->a
    eliminando x->y y dejando y->a, para luego poder hacer la unificacion."""
    for i in range(len(tita)):
        for j in range(len(sigma)):
            if tita[i].sustitucion == sigma[j].valor:
                uni = Unificacion(tita[i].valor, sigma[j].sustitucion)
                tita[i] = uni
    return tita 

def unifica_recursivo_lista(ls, lt, tita):
    """Si se trata de dos funciones con mismo nombre y aridad esta funcion unificara elemento a elemento los parametros de
    ambas funciones."""
    if len(ls) == 0:
        return tita
    else:
        sigma = unifica_recursivo(ls[0], lt[0], tita)
        if sigma == None:
            return None
        else:
            return unifica_recursivo_lista(ls[1:],lt[1:], componer(tita, sigma))

def unifica_recursivo(s, t, lista):
    """Metodo que realiza la unificacion y devuelve la lista con las unificaciones. Recibe una lista de funciones, que
    inicialmente tendra una unica posicion."""
    if s == t:
        return list() 
    elif esVariable(s): #s es variable
        if type(t) == Funcion and t.ocurre(s): #si t es una funcion y contiene s devolvemos fallo
            return None #devolver fallo
        else:
            uni = Unificacion(s, t)
            lista.append(uni)
            return lista 
    elif esVariable(t): #t es variable
        return unifica_recursivo(t, s, lista)
    elif  type(s) == Funcion and type(t) == Funcion : #en otro caso. Es decir, ambas son funciones
        if  s.nombre != t.nombre or s.aridad() != t.aridad(): #Y si las funciones son distintas o no tienen misma aridad
            return None #devolver fallo
        else:
            return unifica_recursivo_lista(s.parametros, t.parametros, lista)        

def unifica(s, t):
    """Metodo que unifica ambas dos funciones recibidas por parametro."""
    return unifica_recursivo(s, t, list()) 

def contiene(lista, elemento):
    """Devuelve la posicion del elemento en la lista si lo contiene, pero en caso de no contenerlo devuelve -1."""
    res = -1
    for i in range(len(lista)):
        if lista[i] == elemento:
            res = i
            i = len(lista)
    return res

def interseccion(lista1, lista2):
    """Devuelve la lista con los pares formados por los elementos repetidos en ambas lista para realizar la interseccion."""
    res = list()
    for i in range(len(lista1)):
        auxiliar = contiene(lista2, lista1[i])
        if auxiliar != -1:
            res.append((lista1[i],lista2[auxiliar]))
    
    return res

def noContiene(item, lista):
    """Devuelve true si no contiene el elemento, o false si lo contiene."""
    res = bool(1)
    
    for i in range(len(lista)):
        if lista[i].valor == item.valor: #solo con mirar el valor ya es suficiente.
            res = bool(0)
            i = len(lista)-1
    
    return res

def componerUnificaciones(lista): 
    """Metodo que elimina las sustituciones repetidas. Es un metodo necesario puesto que la forma en que lo hago obtengo 
    sustituciones validas para misma variable. De este modo, nos quedamos con uno de ellos."""
    res = list()
    
    for i in range(len(lista)):
        item = lista[i]
        if item != None:
            for j in range(len(item)):
                if noContiene(item[j], res):
                    res.append(item[j])
    
    return res    

def devolverUnificaciones(elemsC, elemsC1):
    """Metodo usado en la absorcion para hacer todas las unificaciones posibles entre los elementos de ambas lista. 
    Posteriormente antes de devolver el resultado eliminamos las repetidas."""
    res = list()
    
    for i in range(len(elemsC)):
        for j in range(len(elemsC1)):
            uni = unifica(elemsC[i], elemsC1[j])
            res.append(uni)
    
    res = componerUnificaciones(res) #Se eliminan los repetidos y se devuelve una unica lista con todas las unificaciones. Eliminar tambien los fallos producidos
    
    return res

def esta(lista, elem):
    """Metodo que comprueba si un elemento esta en una lista."""
    for i in range(len(lista)):
        if lista[i].nombre == elem.nombre:
            return bool(1) #esta, luego delvolvemos true
    
    return bool(0)    

def filtrar(intersec, lista): 
    """Metodo que quita los elementos de lista que estan en intersec, porque estan repetidos en ambas clausulas."""
    res = list()
    
    for i in range(len(intersec)):#eliminamos los pares
        res.append(intersec[i][0])
        
    copia = list(lista)
    for i in range(len(copia)):
        for j in range(len(res)):
            if copia[i].nombre == res[j].nombre and esta(lista, copia[i]):
                lista.remove(copia[i])
    return lista

def hacerUnificaciones(lista1, lista2, unificaciones):
    """Metodo que tambien se encuentra en las clases clausula y funcion (realmente es dentro de la clase funcion donde se hace
    la unificacion) que realiza las unificaciones. Lo necesitamos porque en intraconstruccion e interconstruccion debemos 
    hacer las unificaciones y lo llamamos a traves de un metodo para modularizar el codigo."""
    for i in range(len(lista1)):
        lista1[i].hacerUnificaciones(unificaciones)
    for i in range(len(lista2)):
        lista2[i].hacerUnificaciones(unificaciones)
    
    return lista1, lista2

def funcionAleatoria():
    """Funcion que genera una funcion aleatoria sin parametros, es decir, un predicado. Pero en este caso nos vale."""
    numAleatorio = random.randint(100, 999) #Para dar un nombre distinto a cada funcion segun el valor aleatorio
    nombreFuncion = 'f' + str(numAleatorio)
    return Funcion(nombreFuncion, [])
    
"""CLASES================================================================================================================"""
#Clases

class Unificacion(object):
    """Clase que almacena una sustitucion de modo que guarda el valor de la variable y el de su sustitucion."""
    
    def __init__(self, valor, sustitucion):
        self.valor = valor
        self.sustitucion = sustitucion
    
    def __str__(self):
        return str(self.valor) + '/' + str(self.sustitucion) 
    
    def __eq__(self, otro):
        if not isinstance(otro, Unificacion):
            return bool(0)

        return (self.valor == otro.valor and self.sustitucion == otro.sustitucion)

class Parametro(object):
    """Clase abstracta para ser heredada desde Variable y Funcion, necesaria para el tipo de implementacion de
    __eq__ (equals), que nos ayudara a saber si son iguales o no dos parametros, que podran ser funcion y/o variable."""
    
    def __init__(self):
        pass
        
    def __eq__(self, otro):
        return self.__dict__ == otro.__dict__

class Variable(Parametro):
    """Clase que almacena una variable."""
    
    def __init__(self, valor):
        self.valor = valor
        
    def __str__(self):
        return self.valor       
    
    def esConstante(self): 
        """Es constante si tiene solo numero o algun caracter mayusculas. No es constante si es minuscula todo o minusuclas
        con algun numero."""
        return self.valor.isdigit() or (not self.valor.islower())
    
class Funcion(Parametro):
    """Clase que utilizaremos para representar funciones. Contiene el nombre de dicha funcion y una lista con los parametros de entrada, que podran ser variables (Strings) u otras funciones (Objeto Funcion)."""

    def __init__(self, nombre, parametros):
        self.nombre = nombre
        if type(parametros)==list:
            self.parametros = list(parametros) #se copia la lista
        else:
            self.parametros = [parametros]

    def __str__(self): #sobreescritura del metodo para mostrar la informacion con la notacion propia.
        res = self.nombre + '('
        
        for i in range(len(self.parametros)):
            if i<len(self.parametros)-1:
                res += str(self.parametros[i]) + ', '
            else:
                res += str(self.parametros[i])
        
        res +=  ')'
        
        return res
    
    def aridad(self): 
        """Devuelve el numero de parametros que recibe la funcion."""
        return len(self.parametros)
        
    def ocurre(self, s):
        """Devuelve true si en los parametros de la funcion se encuentra la variable s recibida por parametro. 
        Nunca deberia llegar un s que no sea variable."""
        for i in range(len(self.parametros)):
            if self.parametros[i] == s:
                return bool(1)
        
        return bool(0)
    
    def hacerUnificaciones(self, unificaciones):
        """Realiza las unificaciones recibidas en los parametros de la propia funcion."""
        if unificaciones!=None and len(unificaciones)>0:
            for i in range(len(unificaciones)):
                for j in range(len(self.parametros)):
                    if type(self.parametros[j]) == Funcion:
                        self.parametros[j].hacerUnificaciones(unificaciones)
                    else:
                        if self.parametros[j] == unificaciones[i].valor:
                            self.parametros[j] = unificaciones[i].sustitucion
                    
class Clausula(object):
    """Clase que utilizaremos para representar clausulas del tipo A,B->C, donde A,B,C son funciones. Es decir distinguimos
    entre la cabeza de la implicacion donde puede haber una funcion o una conjuncion de funciones, y el cuerpo que es el 
    resultado de la implicacion cuando se cumple lo que ha
y en la cabeza, que sera una funcion en cualquier caso.
    """

    def __init__(self, cuerpo, cabeza):
        """Cuerpo es la parte anterior a la implicacion (->), y cabeza la parte posterior."""
        if type(cuerpo) == list:
            self.cuerpo = list(cuerpo)
        else:
            self.cuerpo = [cuerpo]
        self.cabeza = cabeza

    def __str__(self):
        res = ''
        
        for i in range(len(self.cuerpo)):
            if i<len(self.cuerpo)-1:
                res += str(self.cuerpo[i]) + ','
            else:
                res += str(self.cuerpo[i])
        
        res += ' → ' + str(self.cabeza) #por si hace falta el caracter opuesto es: ←
        
        return res
    
    def __eq__(self, otro):
        return self.__dict__ == otro.__dict__   
     
    def devuelveElementos(self):
        """Devuelve todas las funciones de la clausula para utilizarlos en el metodo interseccion."""
        res = list()
        
        for i in range(len(self.cuerpo)):
            res.append(self.cuerpo[i])
        res.append(self.cabeza)
        
        return res 
        
    def hacerUnificaciones(self, unificaciones):
        """Metodo que hace las unificaciones recibidas en las funciones contenidas en la clasula. Esta a su vez llama al
        metodo correspondiente de cada funcion encargada de hacer dicha tarea."""
        for i in range(len(self.cuerpo)):
            self.cuerpo[i].hacerUnificaciones(unificaciones)
        
        self.cabeza.hacerUnificaciones(unificaciones)                 
                    
class VOperador(object):
    """Clase que contendra los algoritmos para realizar los algoritmos de absorcion e identificacion para los 
    V-operadores."""

    def __init__(self, clausula):
        self.clausula = clausula
    
    def absorcion(self, clausula1):
        """A traves de dos clausulas se formara una tercera que sera devuelta. Para obtener esa tercera clausula se 
        formara apartir de las funciones no repetidas en ambas clausulas iniciales. Para la cabeza de la clausula
        tercera la añadiremos puesto que conocemos cual es gracias al esquema general, y por tanto no se añadira al
        cuerpo."""  
        #Nos traemos todos los elementos de ambas clausulas.
        elemsC = self.clausula.devuelveElementos()
        elemsC1 = clausula1.devuelveElementos()
        #Obtenemos todas las unificaciones entre todos los elementos de ambas. La lista de unificaciones vendra filtrada
        #para evitar ingoherencias.
        unificaciones = devolverUnificaciones(elemsC, elemsC1)
        
        #Aqui se muestran las unificaciones por pantalla
        if type(unificaciones) == list:
            print('A continuacion se muestran las unificaciones:')
            for i in range(len(unificaciones)):
                print(str(unificaciones[i]))
        
        #Realizamos las unificaciones en todos los elementos para posteriormente hacer la interseccion.
        #Si esto no se hiciera podrian no intersectar.
        elemsC, elemsC1 = hacerUnificaciones(elemsC, elemsC1, unificaciones)
        #Obtenemos las cabezas de ambas clausulas (ultima poisicion) para realizar la interseccion solo con los elementos
        #del cuerpo
        cabezaC1 = elemsC1[len(elemsC1)-1]
        cabezaC = elemsC1[len(elemsC1)-1]
        #Obtenemos los elementos que se repiten en ambas clausulas.
        intersec = interseccion(elemsC[:len(elemsC)-1], elemsC1[:len(elemsC1)-1])
        #Eliminamos los elementos repetidos para formar la clausula resultante a partir de ellos.
        elemsC = filtrar(intersec, elemsC[:len(elemsC)-1]) 
        elemsC1 = filtrar(intersec, elemsC1[:len(elemsC1)-1])
        elemsC.append(cabezaC)
        elemsC1.append(cabezaC1)
        #una vez eliminados esos elementos
        if len(elemsC) > 1: #Puede haber casos donde venga un solo elemento que sera cabeza de c2 (clausula resultante).
            elemsCprima = list(elemsC[:len(elemsC)-1]) #Quitamos el elemento que ira en la cabeza de c2
        else:
            elemsCprima = elemsC
        if len(self.clausula.cuerpo) == 0: #para el caso especial del ejemplo 2.
            """Si la clausula no traia cuerpo, en ese caso necesitamos construir la nueva clausula con los elementos
            unicamente de provenientes del cuerpo de la clausula 1."""
            res = Clausula(elemsC1,self.clausula.cabeza) #Clausula c2, segun el esquema general.
        else:    
            res = Clausula(elemsCprima+elemsC1,self.clausula.cabeza) #Clausula c2, segun el esquema general.
        return res
        
    def identificacion(self, clausula2):
        """A traves de dos clausulas se formara una tercera que sera devuelta. Para obtener esa tercera clausula se 
        formara apartir de las funciones no repetidas en ambas clausulas iniciales. Para la cabeza de la clausula
        tercera la añadiremos puesto que conocemos cual es gracias al esquema general, y por tanto no se añadira al
        cuerpo."""
        #Obtenemos los elementos de las calusulas, cuerpo y cabeza de cada uno.
        elemsCuerpoC = list(self.clausula.cuerpo)
        cabezaC = self.clausula.cabeza
        elemsCuerpoC2 = list(clausula2.cuerpo)
        cabezaC2 = clausula2.cabeza
        #Obtenemos la unificacion, en este caso solo necesitamos unificar ambas cabezas de C2 y C.
        unificacionesCabeza = unifica(cabezaC, cabezaC2)
        
        #Aqui se muestran las unificaciones por pantalla
        if type(unificacionesCabeza) == list:
            print('A continuacion se muestran las unificaciones para aplicar a los elementos:')
            for i in range(len(unificacionesCabeza)):
                print(str(unificacionesCabeza[i]))
        
        #Realizamos las unificaciones de ambos cuerpos.
        elemsCuerpoC, elemsCuerpoC2 = hacerUnificaciones(elemsCuerpoC, elemsCuerpoC2, unificacionesCabeza)
        #Obtenemos los elementos repetidos en ambas clausulas.
        intersecCuerpo = interseccion(elemsCuerpoC, elemsCuerpoC2)
        #Eliminamos los repetidos
        elemsCuerpoC = filtrar(intersecCuerpo, elemsCuerpoC) 
        elemsCuerpoC2 = filtrar(intersecCuerpo, elemsCuerpoC2)
        #Formamos la clausula que tendra como cabeza el unico elemento que se supone debe quedar en elemsCuerpoC2 tras filtrar.
        res = Clausula(elemsCuerpoC, elemsCuerpoC2[0]) #Se supone que elemsCuerpoC2 trae un unico elemento
        return res

class WOperador(object):
    """Clase que contendra los algoritmos para realizar los algoritmos de intra-construccion e inter-construccion para los 
    V-operadores."""
    
    def __init__(self, clausula1, clausula2):
        self.clausula1 = clausula1
        self.clausula2 = clausula2

    def intraConstruccion(self):
        """A traves de dos clausulas que tenemos como atributo construir c, c1 y c2 segun el esquema dado. Para ello, obtenemos 
        primero la clausula c con la interseccion de los elementos, en la que se obtiene la funcion aleatoria, que luego se
        usara en C1 y C2.
        """
        elemsCuerpoB1 = list(self.clausula1.cuerpo)
        elemsCuerpoB2 = list(self.clausula2.cuerpo)
        cabezaB1 = self.clausula1.cabeza
        cabezaB2 = self.clausula2.cabeza
        unificacionesCabeza = unifica(cabezaB1, cabezaB2)
        unificacionesCuerpo = devolverUnificaciones(elemsCuerpoB1, elemsCuerpoB2)
        elemsCuerpoB1, elemsCuerpoB2 = hacerUnificaciones(elemsCuerpoB1, elemsCuerpoB2, unificacionesCuerpo)
        cabezaB1.hacerUnificaciones(unificacionesCabeza)
        cabezaB2.hacerUnificaciones(unificacionesCabeza)
        if cabezaB1 == cabezaB2:
            
            #Aqui se muestran las unificaciones por pantalla
            if type(unificacionesCabeza) == list:
                print('A continuacion se muestran las unificaciones para aplicar a los elementos de la cabeza:')
                for i in range(len(unificacionesCabeza)):
                    print(str(unificacionesCabeza[i]))
            if type(unificacionesCuerpo) == list:
                print('A continuacion se muestran las unificaciones para aplicar a los elementos del cuerpo:')
                for i in range(len(unificacionesCuerpo)):
                    print(str(unificacionesCuerpo[i]))
            
            intersecCuerpo = interseccion(elemsCuerpoB1, elemsCuerpoB2)
            intersecC = list()
            for i in range(len(intersecCuerpo)):
                par = intersecCuerpo[i]
                intersecC.append(par[0])
            funAle = funcionAleatoria()
            intersecC.append(funAle)
            c = Clausula(intersecC, cabezaB1) 
            c1 = Clausula(elemsCuerpoB1, funAle)
            c2 = Clausula(elemsCuerpoB2, funAle)
            return c, c1, c2 
        else: #Las cabezas de B1 y B2 no coinciden, por lo que no se puede hacer la intra-construccion
            return None

    def interConstruccion(self):
        """A traves de dos clausulas que tenemos como atributo construir c, c1 y c2 segun el esquema dado. Para ello, obtenemos 
        primero la clausula c con la interseccion de los elementos, en la que se obtiene la funcion aleatoria, que luego se
        usara en C1 y C2.
        """
        elemsCuerpoB1 = list(self.clausula1.cuerpo)
        elemsCuerpoB2 = list(self.clausula2.cuerpo)
        cabezaB1 = self.clausula1.cabeza
        cabezaB2 = self.clausula2.cabeza
        unificacionesCabeza = unifica(cabezaB1, cabezaB2)
        unificacionesCuerpo = devolverUnificaciones(elemsCuerpoB1, elemsCuerpoB2)
        elemsCuerpoB1, elemsCuerpoB2 = hacerUnificaciones(elemsCuerpoB1, elemsCuerpoB2, unificacionesCuerpo)
        cabezaB1.hacerUnificaciones(unificacionesCabeza)
        cabezaB2.hacerUnificaciones(unificacionesCabeza)
        
        #Aqui se muestran las unificaciones por pantalla
        if type(unificacionesCabeza) == list:
            print('A continuacion se muestran las unificaciones para aplicar a los elementos de la cabeza:')
            for i in range(len(unificacionesCabeza)):
                print(str(unificacionesCabeza[i]))
        if type(unificacionesCuerpo) == list:
            print('A continuacion se muestran las unificaciones para aplicar a los elementos del cuerpo:')
            for i in range(len(unificacionesCuerpo)):
                print(str(unificacionesCuerpo[i]))
        
        intersecCuerpo = interseccion(elemsCuerpoB1, elemsCuerpoB2)
        intersecC = list()
        for i in range(len(intersecCuerpo)):
            par = intersecCuerpo[i]
            intersecC.append(par[0])
        funAle = funcionAleatoria()
        c = Clausula(intersecC, funAle) 
        elemsCuerpoB1.append(funAle)
        c1 = Clausula(elemsCuerpoB1, cabezaB1)
        elemsCuerpoB2.append(funAle)
        c2 = Clausula(elemsCuerpoB2, cabezaB2)
        return c, c1, c2

"""PRUEBAS================================================================================================================"""
#Pruebas

#A continuacion los ejemplos del documento dado, y posteriormente los ejemplos inventados, por ese orden.


#Ejemplo WOperador para inter-construccion
"""if __name__ == '__main__':
    variable0 = Variable('0')
    funcion = Funcion('s',[variable0])
    funcion2 = Funcion('nat', [funcion])
    clausula1 = Clausula([], funcion2)
    funcion4 = Funcion('s',[funcion])
    funcion5 = Funcion('nat', [funcion4])
    clausula2 = Clausula([], funcion5)
    algoritmo = WOperador(clausula1, clausula2)
    c, c1, c2 = algoritmo.interConstruccion()
    print(str('El resultado es:'))
    print(str(c))
    print(str(c1))
    print(str(c2))"""
#Ejemplo WOperador para intra-construccion
"""if __name__ == '__main__':
    variableX = Variable('x')
    variableY = Variable('y')
    funcion = Funcion('descendiente',[variableX, variableY])
    funcion2 = Funcion('mujer', [variableX])
    funcion3 = Funcion('madre', [variableY, variableX])
    clausula1 = Clausula([funcion2, funcion3], funcion)
    funcion4 = Funcion('descendiente',[variableX, variableY])
    funcion5 = Funcion('mujer', [variableX])
    funcion6 = Funcion('padre', [variableY, variableX])
    clausula2 = Clausula([funcion5, funcion6], funcion4)
    algoritmo = WOperador(clausula1, clausula2)
    c, c1, c2 = algoritmo.intraConstruccion()
    print(str('El resultado es:'))
    print(str(c))
    print(str(c1))
    print(str(c2))"""
#Ejemplo 2 VOperador para absorcion
"""if __name__ == '__main__':
    variable0 = Variable('0')
    funcion = Funcion('s', [variable0])
    funcion2 = Funcion('nat', [funcion])
    funcion6 = Funcion('s', [funcion])
    funcion7 = Funcion('nat', [funcion6])
    clausula1 = Clausula([], funcion2)
    clausula = Clausula([], funcion7)
    algoritmo = VOperador(clausula)
    #algoritmo.absorcion(clausula1)
    print(str('El resultado es:'))
    print(str(algoritmo.absorcion(clausula1)))"""
#Ejemplo 1 VOperador para absorcion
"""if __name__ == '__main__':    
    variableX = Variable('x')
    variableY = Variable('y')
    variableV = Variable('v')
    variableW = Variable('w')
    funcion = Funcion('progenitor', [variableX,variableY])
    funcion2 = Funcion('madre', [variableX,variableY])
    funcion3 = Funcion('hija', [variableV,variableW])
    funcion4 = Funcion('madre', [variableW,variableV])
    funcion5 = Funcion('mujer', [variableV])
    clausula1 = Clausula([funcion2], funcion)
    clausula = Clausula([funcion5, funcion4], funcion3)
    algoritmo = VOperador(clausula)
    #algoritmo.absorcion(clausula1)
    print(str('El resultado es:'))
    print(str(algoritmo.absorcion(clausula1)))"""
#Ejemplo 2 VOperador para identificacion
"""if __name__ == '__main__':
    variableX = Variable('x')
    variable0 = Variable('0')
    funcion = Funcion('s',[variableX])
    funcion2 = Funcion('nat', [variableX])
    funcion3 = Funcion('nat', [funcion])
    funcion4 = Funcion('s',[variable0])
    funcion6 = Funcion('s', [funcion4])
    funcion7 = Funcion('nat', [funcion6])
    clausula2 = Clausula([funcion2], funcion3)
    clausula = Clausula([], funcion7)
    algoritmo = VOperador(clausula)
    #algoritmo.absorcion(clausula1)
    print(str('El resultado es:'))
    print(str(algoritmo.identificacion(clausula2)))"""
#Ejemplo 1 VOperador para identificacion
"""if __name__ == '__main__':    
    variableA = Variable('a')
    variableB = Variable('b')
    variableV = Variable('v')
    variableW = Variable('w')
    funcion = Funcion('progenitor', [variableB,variableA])
    #funcion2 = Funcion('madre', [variableX,variableY])
    funcion3 = Funcion('hija', [variableA,variableB])
    funcion4 = Funcion('madre', [variableW,variableV])
    funcion5 = Funcion('mujer', [variableA])
    funcion6 = Funcion('hija', [variableV,variableW])
    funcion7 = Funcion('madre', [variableW,variableV])
    funcion8 = Funcion('mujer', [variableV])
    clausula2 = Clausula([funcion, funcion5], funcion3)
    clausula = Clausula([funcion7, funcion8], funcion6)
    algoritmo = VOperador(clausula)
    #algoritmo.absorcion(clausula1)
    print(str('El resultado es:'))
    print(str(algoritmo.identificacion(clausula2)))"""

#Ejemplo dado por el profesor en tutoria para VOperadores, en concreto absorcion.
"""if __name__ == '__main__':
    variableX = Variable('x')
    variableA = Variable('a')
    funcion = Funcion('s',[variableX])
    funcion2 = Funcion('nat', [variableA])
    funcion3 = Funcion('nat', [funcion])
    clausula1 = Clausula([], funcion2)
    clausula = Clausula([], funcion3)
    algoritmo = VOperador(clausula)
    #algoritmo.absorcion(clausula1)
    print(str('El resultado es:'))
    print(str(algoritmo.absorcion(clausula1)))""" 

#Ejemplo inventado para VOperadores: 1- con Absorcion; 2- con Identificacion
"""if __name__ == '__main__':
    variableX = Variable('x')
    variableY = Variable('y')
    variableA = Variable('a')
    variableB = Variable('b')
    masResponsabilidadXY = Funcion('masResponsabilidad', [variableX, variableY])
    ganaMasXY = Funcion('ganaMas', [variableX, variableY])
    empleadoA = Funcion('esEmpleado',[variableA])
    masResponsabilidadAB = Funcion('masResponsabilidad', [variableA, variableB])
    subordinadoBA = Funcion('esSubordinado', [variableB, variableA])
    clausula1 = Clausula([masResponsabilidadXY], ganaMasXY)
    clausula = Clausula([empleadoA, masResponsabilidadAB], subordinadoBA)
    algoritmo = VOperador(clausula)
    print(str('El resultado es:'))
    print(str(algoritmo.absorcion(clausula1)))"""
"""if __name__ == '__main__':
    variableX = Variable('x')
    variableY = Variable('y')
    variableA = Variable('a')
    variableB = Variable('b')
    empleadoX = Funcion('esEmpleado',[variableX])
    ganaMasXY = Funcion('ganaMas', [variableX, variableY])
    subordinadoYX = Funcion('esSubordinado', [variableY, variableX])
    empleadoA = Funcion('esEmpleado',[variableA])
    masResponsabilidadAB = Funcion('masResponsabilidad', [variableA, variableB])
    subordinadoBA = Funcion('esSubordinado', [variableB, variableA])
    clausula2 = Clausula([empleadoX, ganaMasXY], subordinadoYX)
    clausula = Clausula([empleadoA, masResponsabilidadAB], subordinadoBA)
    algoritmo = VOperador(clausula)
    print(str('El resultado es:'))
    print(str(algoritmo.identificacion(clausula2)))"""
#Ejemplo inventado para WOperadores: Mismo ejemplo, probado en intraConstruccion e interConstruccion
"""if __name__ == '__main__':
    variableX = Variable('x')
    variableY = Variable('y')
    variableA = Variable('a')
    variableB = Variable('b')
    equipoX = Funcion('equipo',[variableX])
    marcaMasGolesXY = Funcion('marcaMasGoles', [variableX, variableY])
    ganaXY = Funcion('gana', [variableY, variableX])
    equipoA = Funcion('equipo',[variableA])
    marcaMasGolesAB = Funcion('marcaMasGoles', [variableA, variableB])
    ganaAB = Funcion('gana', [variableB, variableA])
    clausula2 = Clausula([equipoX, marcaMasGolesXY], ganaXY)
    clausula = Clausula([equipoA, marcaMasGolesAB], ganaAB)
    algoritmo = WOperador(clausula, clausula2)
    c, c1, c2 = algoritmo.intraConstruccion()
    print(str('El resultado es:'))
    print(str(c))
    print(str(c1))
    print(str(c2))"""
"""if __name__ == '__main__':
    variableX = Variable('x')
    variableY = Variable('y')
    variableA = Variable('a')
    variableB = Variable('b')
    equipoX = Funcion('equipo',[variableX])
    marcaMasGolesXY = Funcion('marcaMasGoles', [variableX, variableY])
    ganaXY = Funcion('gana', [variableY, variableX])
    equipoA = Funcion('equipo',[variableA])
    marcaMasGolesAB = Funcion('marcaMasGoles', [variableA, variableB])
    ganaAB = Funcion('gana', [variableB, variableA])
    clausula2 = Clausula([equipoX, marcaMasGolesXY], ganaXY)
    clausula = Clausula([equipoA, marcaMasGolesAB], ganaAB)
    algoritmo = WOperador(clausula, clausula2)
    c, c1, c2 = algoritmo.intraConstruccion()
    print(str('El resultado es:'))
    print(str(c))
    print(str(c1))
    print(str(c2))"""
