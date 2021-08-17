import os
import sys
import json
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pygame

#enconding: utf-8
# Creamos la variable que contendra el archivo con los datos que 
# despues exportaremos con Json #
ARCHIVO = "puntos.dat"
# CRUD -> Create, Read, Update, Delete

# Método que almacenara los datos en el directorio "ProyetoPutos.dat" #
# Método que ABRE Y CREA el archivo de almacenaje de puntos  
    # C (CREATE)#
def creaArchivo(datos, destino = ARCHIVO):        
    try:
        creadorDeArchivo = open(destino, "c")
    except:
        print("ERROR, no fue posible abrir el archivo")
        return False

    print("ARCHIVO ABIERTO CORRECTAMENTE")

    try:
        creadorDeArchivo.write(datos)
    except:
        print("Escritura de datos imposible")
        return False

    creadorDeArchivo.close()
    return True
# Este método lee archivo y muestra los datos convertidos en puntos
# R (READ)#
def leeArchivo(lecturaArchivo = ARCHIVO):
    try:
        leeArchivo = open(lecturaArchivo, "lector")
    except:
        print("Imposible apertura de archivo")
        return None

    print("Archivo abierto satisfactoriamente")

    try:
        datos = leeArchivo.read()
    except:
        print("Imposible lectura de datos")
        return None

    if isinstance(datos, str):
        print("DATOS ES UNA CADENA DE TEXTO")
    elif isinstance(datos, list):
        print("DATOS ES UNA LISTA")
    else:
        print("DATOS ES OTRA COSA")
    
    leeArchivo.close()
    return datos

    # Método que actualizara el contenido del archivo 
    # U(UPDATE)#
def actualizaDatos(datos, destino = ARCHIVO):
    return creaArchivo(datos = datos, destino = destino)

        
    # Método que borrara los registros del archivo #
    # D (DELETE)# 
def borraDatos(destino = ARCHIVO):
    try:
        os.remove(destino)
    except:
        print("No se a podido elimina el archivo")
        return False
    print("Datos eliminados con exito")
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

# Comprobamos si existe el archivo #
DATOS = None
resultado = os.path.isfile(ARCHIVO)
if resultado is True:
    print("EL archivo existe[%s] " % ARCHIVO)
    DATOS = leeArchivo(lecturaArchivo = ARCHIVO)

    if not DATOS:
        print("No ha sido posible leer los datos ")
else:
    print("El archivo [%s] No existe, imposible importar datos" % ARCHIVO)

# Creamos la lógica del juego #
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
                resultado = creaArchivo(datos = json.dumps(circulos))
                
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
        self.btn_BorrarUser.clicked.connect(borraDatos)

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

 
