from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import os
import gettext

from gtts import gTTS
from playsound import playsound

from Automata import Automata

import matplotlib as matp
import matplotlib.backends.backend_qt5agg

matp.use('Qt5Agg')

directorio_actual = os.getcwd()
localedir = os.path.join(directorio_actual, 'locale')

gettext.bindtextdomain('myapp', localedir)
gettext.textdomain('myapp')

class AutomataGUI(QMainWindow):

    def __init__(self):

        print(localedir)

        super().__init__()

        self.__automata = Automata()

        # INICIALIZAR LAS OPCIONES DE LOS MENÚ
        self.idiomas_menu = None
        self.ingles_action = None
        self.frances_action = None
        self.espanol_action = None

        # PARA GENERAR LOS MENÚ DE LOS IDIOMAS
        self.idiomas_group = QActionGroup(self)
        self.idiomas_group.setExclusive(True)

        self.__crearInterfaz()

    def __crearInterfaz(self, idioma = 'es'):

        translations = gettext.translation(domain = 'mensajes', localedir = localedir, languages = [idioma])
        translations.install()
        _ = translations.gettext


        # NOMBRE Y TAMAÑO DE LA VENTANA
        self.setWindowTitle(_("Máquina de Turing"))

        # WIDGET PRNCIPAL
        widget = QWidget()
        self.setCentralWidget(widget)

        # ACTUALIZAR EL MENU DE IDIOMAS
        if self.idiomas_menu:

            self.__actualizarTextoIdiomasMenu()

        # BARRA DE MENU PARA CAMBIAR IDIOMA
        menu_bar = self.menuBar()

        if not self.idiomas_menu:

            self.idiomas_menu = menu_bar.addMenu(_("Idiomas"))

        if not self.ingles_action:

            self.ingles_action = QAction(_("Inglés"), self)
            self.idiomas_menu.addAction(self.ingles_action)
            self.ingles_action.setCheckable(True)
            self.idiomas_group.addAction(self.ingles_action)

        self.ingles_action.triggered.connect(lambda: self.__cambiarIdioma('en'))

        if not self.frances_action:

            self.frances_action = QAction(_("Francés"), self)
            self.idiomas_menu.addAction(self.frances_action)
            self.frances_action.setCheckable(True)
            self.idiomas_group.addAction(self.frances_action)

        self.frances_action.triggered.connect(lambda: self.__cambiarIdioma('fr'))

        if not self.espanol_action:

            self.espanol_action = QAction(_("Español"), self)
            self.idiomas_menu.addAction(self.espanol_action)
            self.espanol_action.setCheckable(True)
            self.idiomas_group.addAction(self.espanol_action)
            self.espanol_action.setChecked(True)

        self.espanol_action.triggered.connect(lambda: self.__cambiarIdioma('es'))

        # LAYOUT PRINCIPAL
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # QLABEL PARA MOSTRAR MENSAJE
        label_velocidad = QLabel(_("INTRODUZCA UNA CADENA:"))
        layout.addWidget(label_velocidad)

        # QLINEEDIT PARA INGRESAR LA CADENA
        self.__linee_cadena = QLineEdit()
        layout.addWidget(self.__linee_cadena)

        label_cadena = QLabel(_("VELOCIDAD:"))
        layout.addWidget(label_cadena)

        self.__deslizador = QSlider(Qt.Horizontal)
        self.__deslizador.setMinimum(1)
        self.__deslizador.setMaximum(5)
        self.__deslizador.setValue(1)
        layout.addWidget(self.__deslizador)

        # BOTÓN PARA PROCESAR
        btn_procesar = QPushButton(_("PROCESAR"))
        btn_procesar.clicked.connect(self.__procesar)
        layout.addWidget(btn_procesar)

        # PARA MOSTRAR EL HISTORIAL
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        btn_procesar.clicked.connect(lambda: self.__historial(self.__linee_cadena.text()))

    def __procesar(self):

        if self.__automata.procesar("#" + self.__linee_cadena.text() + "#", self.__deslizador.value()):

            self.__procesarVoz(self.traduccion("LA CADENA FUE ACEPTADA POR LA MÁQUINA DE TURING."))
            QMessageBox.information(self, self.traduccion("RESULTADO"), self.traduccion("LA CADENA FUE ACEPTADA POR LA MÁQUINA DE TURING."))

        else:

            self.__procesarVoz(self.traduccion("LA CADENA NO FUE ACEPTADA POR LA MÁQUINA DE TURING."))
            QMessageBox.warning(self, self.traduccion("RESULTADO"), self.traduccion("LA CADENA NO FUE ACEPTADA POR LA MÁQUINA DE TURING."))

    def __cambiarIdioma(self, idioma):

        if idioma == 'en':

            self.ingles_action.setChecked(True)
            locale = 'en'

        elif idioma == 'fr':

            self.frances_action.setChecked(True)
            locale = 'fr'

        else:

            self.espanol_action.setChecked(True)
            locale = 'es'

        gettext.install('mensajes', localedir, names = ("ngettext",))
        gettext.translation('mensajes', localedir, languages = [locale]).install()

        self.__crearInterfaz(locale)

    def __obtenerIdioma(self):

        if self.ingles_action.isChecked():

            return 'en'

        elif self.frances_action.isChecked():

            return 'fr'

        elif self.espanol_action.isChecked():

            return 'es'

    def traduccion(self, mensaje):

        idioma = self.__obtenerIdioma()
        translations = gettext.translation(domain='mensajes', localedir = localedir, languages = [idioma])
        translations.install()
        _ = translations.gettext

        return _(mensaje)

    def __actualizarTextoIdiomasMenu(self):

        self.ingles_action.setText(self.traduccion("Inglés"))
        self.espanol_action.setText(self.traduccion("Español"))
        self.frances_action.setText(self.traduccion("Francés"))
        self.idiomas_menu.setTitle(self.traduccion("Idiomas"))

    def __procesarVoz(self, texto):

        objeto = gTTS(text = texto, lang = self.__obtenerIdioma(), slow = False)
        objeto.save("mensaje.mp3")

        playsound("mensaje.mp3", block = False)

        os.remove("mensaje.mp3")

    def __historial(self, palabra):
        self.list_widget.addItem(palabra)
