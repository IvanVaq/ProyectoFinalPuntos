import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pygame

class VentanaInicio(QMainWindow):

    # Método de llamada automatica e inicialización de atributos #
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
        self.btn_seleccionColor.clicked.connect(juego)


# Creamos un método que nos mostrara una paleta de colores y nos permitira
# la elección del color que utilizaremos en nuestro juego #
def seleccionaColorPaleta():
    colores = QColorDialog.getColor() 
    if colores.isValid():
        colorin = colores.name()
    else:
        sys.exit()
    

    return colorin

# Creamos la lógica del juego #
def juego():
    ANCHURA_PANTALLA = 650
    ALTURA_PANTALLA = 500

    colorin = seleccionaColorPaleta()
    NEGRO = (0, 0, 0)
    BLANCO = (225, 225, 225)

    # Indicamos el título de la ventana
    pygame.display.set_caption("Puntos en la ventana")
    # Indicamos el tamaño de la pantalla #
    pantalla = pygame.display.set_mode((ANCHURA_PANTALLA,ALTURA_PANTALLA))
    # Inicializamos la ventana #
    pygame.init()

    
    #       METODOS DE VENTANA #
    # Posición del raton
    def get_pos():
        return pygame.mouse.get_pos()

        # Construye el círculo
    def draw_circle(screen, color = colorin, radius = 10,thickness = 2, pos = None):
        if not pos:
             pos = get_pos() 
        pygame.draw.circle(screen, color, pos, radius, thickness)

    # Pintamos la ventana
    def blank_screen(screen, color=('#AF6E37'), height=ALTURA_PANTALLA, width=ANCHURA_PANTALLA):
         pygame.draw.rect(screen, color, (0, 0, width, height))

    # Creamos una lista para almacenar circulos #
    circulos = list()

    # Cremos un condicional para la logica de pygame #
    while True:
        # Llamamos al método que nos pintara la pantalla #
        blank_screen(pantalla, color = ('#AF6E37'), height = ALTURA_PANTALLA, width = ANCHURA_PANTALLA)
        # Lamamos al método que nos pintara los circulos #
        draw_circle(pantalla, color = colorin, radius = 10, thickness = 2)

        contador = 0
        # Con un bucle for iremos dibujando los circulos y actualizando la pantalla #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
            
                # Instanciamos el método get_pos que nos devolvera la posición del ratón #
                pos = get_pos()

                # Cremos un diccionario que almacenara tanto la posición como el color elegido #
                circulo_diccionario = dict()
                circulo_diccionario['pos'] = pos
                circulo_diccionario['color'] = colorin

                # Con el método de clase append almacenamos los circulos en la lista de circulos#
                circulos.append(circulo_diccionario)
        
        # Con un bucle for iremos mostrando los puntos en la pantalla #
        for circulo in circulos:
             draw_circle(screen = pantalla,color = circulo['color'],
                        pos = circulo['pos'], radius = 10,thickness = 8 )
        # Actualizamos la pantalla para que se muestren los cambios #
        pygame.display.update() 


def main():
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.show()

    app.exec_()

if __name__ == '__main__':
    main()
