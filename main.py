from PySide6.QtWidgets import QApplication

from AutomataGUI import AutomataGUI

import sys

def iniciar():

    # CREAR APLICACIÓN DE QT
    aplicacion = QApplication(sys.argv)

    # CREAR VENTANA PRINCIPAL
    ventana = AutomataGUI()
    ventana.show()

    # EJECUTAR APLICACIÓN DE QT
    sys.exit(aplicacion.exec())

iniciar()
