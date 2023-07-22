# Mi-primer-programa-en-Python-leer-estaciones-meteorologicas-desde-web
Lectura datos estaciones meteorológicas de España (web  publica agencia estatal de meteorología )

# Propósito: 
          Obtener  datos metereologicos de estaciones metereologicas de españa.

# Librerias:

import requests => Permite descargar la pagina web y los archivos de las estaciones 

from pathlib import Path => Para poder comprobar si existen los archivos y carpetas en disco 

import datetime => Para manejar las fechas y horas 

from datetime import timedelta => Para manejar un periodo de tiempo 

import locale => Para leer la fecha de tipo 2023 junio 15 donde el mes está en formato español.

import re =>

import sys => funcoones de sistema para poder detener el programa de fprma similar a un stop 

import winsound => Para poder reproducir  sonidos en windows

import pandas as pd => Libreria de dataframe manejar dataframes 

from io import StringIO => para poder 'leer' los datos dascargados(string) como si fuese un archivo 

from IPython.display import clear_output => CLS borrar la salida de consola

from time import sleep => Retrasar n segundos la ejecucion 

from threading import Timer => para poder hacer temporizador para  subprocesos (hilos) 

import time => no usada aún  en su lugar uso datetime

# Funciones
 **Print => controla las salidas de informacion por pantalla y al archivo log.**
 
            --Parametros de entrada :
  
              Data : es lo que hay que mostrar por pantalla(print) o guardar en archivo log
              
              log: es un valor numerico que condiciona lo que hay que hacer con Data
              
                    0  no hace nada, no presenta ni guarda en log
                    1  solo guarda Data en archivo log 
                    2  guarda en log y ademas presenta por pantalla el contenido de data 
                    3  guarda en log y presenta por pantalla sobreescribiendo en una sola linea


**beep => reproduce un sonido**
            --Parametros de entrada :

                NSound: numero de sonido , se pretende un numero asociado a un topo de sonido 
                        sólo funciona con 0 de momento 


**Log_Error => guarda errores en archivolog de errores**
         
          --Parametros de entrada :
  
              Data : es lo que hay que mostrar por pantalla(print) o guardar en archivo log
              
              log: es un valor numerico que condiciona lo que hay que hacer con Data
              
                    0  no hace nada, no presenta ni guarda en log
                    1  solo guarda Data en archivo log 
                
**Exist_Archivo_Ruta => verificamos previamente si existe un Directorio o Archivo en disco**
    
          --Parametros de entrada :
  
              Directorio_datos : ruta de carpeta general donde se ejecuta el programa 

              directorio_o_archivo :  directorio o ruta de archivo a verificar si existe o no .
              
              log: es un valor numerico que condiciona lo que hay que hacer con Data
              
          --Parametros de retorno :
              True si existe la carpeta o archivo
              False si no existe la carpeta o directorio 

**RutaCompuesta => Compone la ruta a partir de un directorio y un nombre de archivo**
           
           --Parametros de entrada :
  
              Ruta : ruta de carpeta general donde se ejecuta el programa 

              directorio_o_archivo :  directorio o ruta de archivo a verificar si existe o no .
              
              log: es un valor numerico que condiciona lo que hay que hacer con Data



