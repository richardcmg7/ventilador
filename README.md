# Sistema de Visualización para control de Flujo y Presión usado para ventilador mecánico de bajo costo desarrllado en Python.

El presente repositorio corresponde a una aplicación desarrollada en python que permite visualizar y controlar los niveles de flujo y presión para proyecto de ventilador mecánico de
bajo costo. 

El proyecto utiliza en su parte mecánica el prototipo Oxygen.xyz: Para la parte electrónica el sistema de control se realizó con Arduino quien envía la señal por Serial a una Raspberry Pi
quien se va encargar de presentar la información en pantalla.

Se utiliza python como lenguaje de programación para el desarrollo de la interfaz grafica quien lee y escribe a través del puerto serial conectado al Arduino y realiza  la respectiva
representación gráfica en el sistema.

Se utilizá tkinter para realizar el GUI y Matplotlib como libreria para realizar las respectivas graficas. 


Información Base: 

Para el desarrollo de este repositorio utilizamos los post compartidos en www.thepoorengineer.com especificamente: 
* https://www.thepoorengineer.com/en/arduino-python-plot/
* https://www.thepoorengineer.com/en/python-gui/
