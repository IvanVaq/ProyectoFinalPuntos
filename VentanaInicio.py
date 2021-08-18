import os
import sys
import json
import sqlite3
 
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pygame
 
DATAFILE = "puntos.json"



def crearBBDD():

    try:
        con = sqlite3.connect("BaseDeDatosPuntos.bd")
        cursor1 = con.cursor()
        cursor1.execute('''CREATE TABLE puntos (idNombre INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT (20) NOT NULL,
                        pos TEXT,
                        color TEXT)''')    
        con.commit()
        print("Tabla creada correctamente")
    except sqlite3.OperationalError as e:
        print("Error al abrir",e)
        con.rollback()#Método que hace que la transaccion se retortaigaal munto de partida
    con.close()
    
    
# CRUD -> Create, Read, Update, Delete
# C

# Método que almacenara los datos en el directorio que le indicamos #
def almacenar_datos(datos, destino=DATAFILE):
    try:
        # Para abrir el archivo utilizamos el método open y como parametros le indicaremos
        # la ruta y los permisos como el permiso necesario es de escritura le pasaremos w(write)#
        escritor_de_fichero = open(destino, "w")
    except:
        print("ERROR: no he podido abrir el fichero")
        return False
 
    print("ARCHIVO ABIERTO")
 
    try:
        escritor_de_fichero.write(datos)
    except:
        print("ERROR: no he podido escribir los datos en el fichero")
        return False
    #   Cerramos la conexion #
    escritor_de_fichero.close()
    return True
# Método que leera el archivo donde hemos guardado los datos #
# R
def leer_datos(fuente=DATAFILE):
    try:
        # Para abrir el archivo utilizamos el método open y como parametros le indicaremos
        # la ruta y los permisos como el permiso necesario es de lectura le pasaremos r(read)#
        lector_de_fichero = open(fuente, "r")
    except:
        print("ERROR: no he podido abrir el fichero")
        return None
 
    print("EL ARCHIVO SE ABRIO CORRECTAMENTE")
 
    try:
        datos = lector_de_fichero.read()
    except:
        print("ERROR: no he podido leer los datos desde el fichero")
        return None
 
    if isinstance(datos, str):
        print("DATOS ES UNA CADENA DE TEXTO")
    elif isinstance(datos, list):
        print("DATOS ES UNA LISTA")
    else:
        print("DATOS ES OTRA COSA")
 
    lector_de_fichero.close()
    return datos
 
# Método que actualizara los datos del archivo # 
# U
def actualizar_datos(datos, destino=DATAFILE):
    return almacenar_datos(datos=datos, destino=destino)
 
# Método que borrara el archivo # 
# D
def borrar_datos():
    try:
        os.remove(DATAFILE)
    except:
        print("ERROR: Imposible borrar archivo que no existe")
        return False
 
    print("OK: he podido BORRAR el fichero")
    return True
 
# Creamos un método que nos mostrara una paleta de colores y nos permitira
# la elección del color que utilizaremos en nuestro juego #
def seleccionaColorPaleta():
    colorin = QColorDialog.getColor() 
    if colorin.isValid():
        colorin = colorin.name()
    else:
        sys.exit()
    return colorin
 
# Ver si existe el fichero de datos.
DATOS = None
resultado = os.path.isfile(DATAFILE)
if resultado is True:
    print("El fichero existe: [%s]" % DATAFILE)
    DATOS = leer_datos(fuente=DATAFILE)
 
    if not DATOS:
        # corresponde con: False, None, ERROR-False, 0
        print("ERROR: No he podido leer los datos (pero puede que no sean NULOS).")
else:
    print("El fichero [%s] NO existe. No vamos a importar datos." % DATAFILE)

 
def juego():
    ANCHURA_PANTALLA = 650
    ALTURA_PANTALLA = 500

    color = seleccionaColorPaleta()
    NEGRO = (0, 0, 0)
    BLANCO = (225, 225, 225)

    # Indicamos el título de la ventana
    pygame.display.set_caption("Puntos en la ventana ")
    # Indicamos el tamaño de la pantalla #
    pantalla = pygame.display.set_mode((ANCHURA_PANTALLA,ALTURA_PANTALLA))
    # Inicializamos la ventana #
    pygame.init()

    
    #       METODOS DE VENTANA #
    # Posición del raton
    def get_pos():
        return pygame.mouse.get_pos()

        # Construye el círculo
    def draw_circle(screen, color = color, radius = 10,thickness = 8, pos = None):
        if not pos:
             pos = get_pos() 
        pygame.draw.circle(screen, color, pos, radius, thickness)

    # Pintamos la ventana
    def blank_screen(screen, color=('#f6d4ff'), height=ALTURA_PANTALLA, width=ANCHURA_PANTALLA):
         pygame.draw.rect(screen, color, (0, 0, width, height))
    
    # Creamos una lista para almacenar circulos #
    circulos = None
    if DATOS:
        circulos = json.loads(DATOS)
    else:
        circulos = list()
    
    # Cremos un condicional para la logica de pygame #
    while True:
        # Llamamos al método que nos pintara la pantalla #
        blank_screen(pantalla, color = ('#f6d4ff'), height = ALTURA_PANTALLA, width = ANCHURA_PANTALLA)
        # Lamamos al método que nos pintara los circulos #
        draw_circle(pantalla, color = color, radius = 10, thickness = 8)

        # Con un bucle for iremos dibujando los circulos y actualizando la pantalla #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Dentro del juego")
                resultado = almacenar_datos(datos = json.dumps(circulos))                
                if resultado is True:
                    print("Datos guardados con exito")
                else:
                    print("ERROR al guardar los datos")

                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                print("punto nuevo")
                # Instanciamos el método get_pos que nos devolvera la posición del ratón #
                pos = get_pos()

                # Cremos un diccionario que almacenara tanto la posición como el color elegido #
                circulo_diccionario = dict()
                circulo_diccionario['pos'] = pos
                circulo_diccionario['color'] = color 

                print("Toma punto en la coordenada ", circulo_diccionario['pos'], " y el color: ", circulo_diccionario['color'])
                # Con el método de clase append almacenamos los circulos en la lista de circulos#
                circulos.append(circulo_diccionario)
        
        # Con un bucle for iremos mostrando los puntos en la pantalla #
        for circulo in circulos:
             draw_circle(screen = pantalla,
                        color = circulo['color'],
                        pos = circulo['pos'],
                         radius = 10,
                         thickness = 8 )
        # Actualizamos la pantalla para que se muestren los cambios #
        
        pygame.display.update() 

class VentanaInicio(QMainWindow):

    # Método de llamada automatica e inicialización de atributos 
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.initUi()


    # Método de creación de la ventana #    
    def initUi(self):
        # Damos tamaño a la ventana
        self.setFixedSize(350, 300)
        #Damos título a la ventana
        self.setWindowTitle("Seleccionemos el color: ")
        
        # Label que pedira el nombre al usuario #
        self.lbl_nombreUsuario = QLabel('Indica tu nombre: ', self)
        self.lbl_nombreUsuario.setGeometry(30, 40, 145, 30)
        self.lbl_nombreUsuario.setFont(QtGui.QFont("Fantansy", 11, QtGui.QFont.Black))

        # QLineEdit que recogera el nombre para en un futuro guardar al usuario con su dibujo en JSon#
        self.txt_nombreUsuario = QLineEdit(self)
        self.txt_nombreUsuario.setGeometry(200, 40, 130, 30)
        self.txt_nombreUsuario.setMaxLength(12)
        self.txt_nombreUsuario.setPlaceholderText('Nombre Usuario')
        self.txt_nombreUsuario.text()

        # instanciamos un label que inidique la función que tienen los 
        # distintos elementos de la GUI # 
        self.lbl_seleccionColor = QLabel('Selecciona un color: ', self)
        # Posicionamos el label y damos el tamaño que consideremos 
        # para su correcta lectura #
        self.lbl_seleccionColor.setGeometry(30, 90, 145, 30)
        # Indicamos el tamaño y tipo de fuente #
        self.lbl_seleccionColor.setFont(QtGui.QFont("Fantasy", 11, QtGui.QFont.Black))

        # Creamos un botón que mostrara la paleta de colores para 
        # utilizar en nuestro juego.
        # Instanciamos el Boton #
        self.btn_seleccionColor = QPushButton('PALETA DE COLORES', self)
        # Indicamos el tamaño y posición de nuestro boton #
        self.btn_seleccionColor.setGeometry(200, 90, 130, 30)
        # Indicamos el tamaño y tipo de fuente #
        self.btn_seleccionColor.setFont(QtGui.QFont("Fantasy", 8, QtGui.QFont.Black))
        # Indicamos la funcion del boton #
        self.btn_seleccionColor.clicked.connect(juego)

        # Boton que cargara una ventana con las opciones de BBDD (Crear,'leer', actualizar, borrar) #
        self.btn_BorrarUser = QPushButton('ELIMINAR USUARIO', self)
        self.btn_BorrarUser.setGeometry(30, 240, 130, 30)
        self.btn_BorrarUser.setFont(QtGui.QFont("Fantasy", 8, QtGui.QFont.Black))
        self.btn_BorrarUser.clicked.connect(borrar_datos)

        # Botón que sale de la app #
        self.btn_salirApp = QPushButton('SALIR', self)
        self.btn_salirApp.setGeometry(200, 240, 130, 30)
        self.btn_salirApp.setFont(QtGui.QFont("Fantasy", 8, QtGui.QFont.Black))
        self.btn_salirApp.clicked.connect(sys.exit)

def main():
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.show()
    
    app.exec_()

if __name__ == '__main__':
    main()    
