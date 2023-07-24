# Mi-primer-programa-en-Python-leer-estaciones-meteorologicas-desde-web
Lectura datos estaciones meteorológicas de España (web  pública agencia estatal de meteorología )

# Propósito: 
          Obtener  datos metereológicos de estaciones metereológicas de españa.

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

from time import sleep => Retrasar n segundos la ejecución 

from threading import Timer => para poder hacer temporizador para  subprocesos (hilos) 

import time => no usada aún  en su lugar uso datetime

# Funciones
 **Print => controla las salidas de información por pantalla y al archivo log.**
 
            --Parámetros de entrada :
  
              Data : es lo que hay que mostrar por pantalla(print) o guardar en archivo log
              
              log: es un valor numérico que condiciona lo que hay que hacer con Data
              
                    0  no hace nada, no presenta ni guarda en log
                    1  solo guarda Data en archivo log 
                    2  guarda en log y ademas presenta por pantalla el contenido de data 
                    3  guarda en log y presenta por pantalla sobreescribiendo en una sola linea


**beep => reproduce un sonido**
            --Parámetros de entrada :

                NSound: número de sonido , se pretende un número asociado a un tipo de sonido 
                        sólo funciona con 0 de momento 


**Log_Error => guarda errores en archivolog de errores**
         
          --Parámetros de entrada :
  
              Data : es lo que hay que mostrar por pantalla(print) o guardar en archivo log
              
              log: es un valor numérico que condiciona lo que hay que hacer con Data
              
                    0  no hace nada, no presenta ni guarda en log
                    1  solo guarda Data en archivo log 
                
**Exist_Archivo_Ruta => verificamos previamente si existe un Directorio o Archivo en disco**
    
          --Parámetros de entrada :
  
              Directorio_datos : ruta de carpeta general donde se ejecuta el programa 

              directorio_o_archivo :  directorio o ruta de archivo a verificar si existe o no .
              
              log: es un valor numérico que condiciona lo que hay que hacer con Data
              
          --Parámetros de retorno :
              True si existe la carpeta o archivo
              False si no existe la carpeta o directorio 

**RutaCompuesta => Compone la ruta a partir de un directorio y un nombre de archivo**
           
           --Parámetros de entrada :
  
              Ruta : ruta de carpeta general donde se ejecuta el programa 

              directorio_o_archivo :  directorio o ruta de archivo a verificar si existe o no .
              
              log: es un valor numérico que condiciona lo que hay que hacer con Data

**Abrir_archivo_df => Abre un archivo DAtaframe guardado en disco como csv**

           --Parámetros de entrada :
  
              Ruta : ruta de carpeta  donde se encuentra  el dataframe

              Nombre_archivo : Nombre del archivo que deseamos obtener.

              Delimt : valor del separador de los datos normalmente Delimt=','.
              
              Head=0: no lo uso actualmente , se trata de indicar en que linea se encuentran las métricas(nombre de las variables) en el archivo.
              
              log: es un valor numérico que condiciona lo que hay que hacer con Data

**crear_Estaciones_df => actualiza el archivo estaciones_df cuando es creado a partir de una lista antigua**

           --Parámetros de entrada :
              Estaciones_df => los datos disponibles de las estaciones en el dataframe Estaciones _df .
              
           --Salida : 
              Estaciones_df
              añade como  fecha de actualización  la fecha actual a cada estación del archivo. 
              añade las url de escarga de cada estación al archivo.

**Guardar_archivo_df => guarda un archivo_df en formato CSV**
          
          --Parámetros de entrada :
          
              Archivo_df :  el archivo que queremos guardar en disco 
  
              Ruta : ruta de carpeta  donde se encuentra  el dataframe

              Nombre_archivo : Nombre del archivo que deseamos obtener.

              Delimt : valor del separador de los datos, normalmente Delimt=','.
                
              log: es un valor numérico que condiciona lo que hay que hacer con Data
              

**Descagar_data_URL =>  descaraga de la web los dagtos de la url dada**
           --Parámetros de entrada :
          
              remote_url :  la url que contiene los datos que queremos obtener .
                
              log: es un valor numérico que condiciona lo que hay que hacer con Data
           
           --Salida : 
              data.text
              retorna los datos descargados en formato texto para su posterior tratamiento .
              
**Actualizar_estaciones=> descarga de la web la lista e información de las distintas estaciones metereológicas**

           --Parámetros de entrada :
          
              Estaciones_df :  archivo para actualizar su contenido en estaciones, solo se agregan, no se eliminan las ya existentes ..
           
           --Salida : 
              
              Estaciones_df : archivo ya actualizado 

**class MyInfiniteTimer():=> clase para poder ejecutar un "hilo" cada cierto tiempo .....**

**Inicio_automático=> ejecutar la actualización de las estaciones cada cierto tiempo**
         
          --Parámetros de entrada :
          
              Minutos :  cada cuantos minutos se actualizan los datos de las estaciones .
              
          --Salida : 
              
              t : variable de clase MyInfiniteTimer 
              En_ejecución: variable que indica si está activa la temporización 

**Stop_automatico => detener la captura automatica cada cierto tiempo**

          --Parámetros de entrada :
          
              t : variable de clase MyInfiniteTimer 
              
          --Salida : 
              
              En_ejecucion: variable que indica si está activa la temporización 

**Programa_ejecutar => realiza la captura de datos de la web recorre las estaciones y las actualiza.**
          
          --Parámetros de entrada :
                        
              log: es un valor numerico que condiciona lo que hay que hacer con Data


**Duplicados=> verifica si hay estaciones con el mismo INDCLIM es decir duplicadas .**
          --Parámetros de entrada :
                        
              log: es un valor numerico que condiciona lo que hay que hacer con Data

**menu_lista => menu de uso del programa**

          





          

