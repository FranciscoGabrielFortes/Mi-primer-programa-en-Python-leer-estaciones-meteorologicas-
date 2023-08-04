#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Leer estaciones tiempo usando pandas


# In[2]:


# importar librerias necesarias 
from time import sleep
import pickle
import json
import requests
from pathlib import Path
import datetime
from datetime import timedelta
import locale # Para leer la fecha de tipo 2023 junio 15 donde el mes está en español.
import re
import sys
import winsound
import pandas as pd
from io import StringIO
from IPython.display import clear_output

print ('cargadas las librerias (import)')


# In[3]:


# funciones 

# Print  :  similar a print pero me permite hacer un LOG en un archivo en disco 

#log=0 (desctivado)no imprime ni guarda en log
#log=1 guarda en archivo log
#log=2 archivo +pantalla
#log=3 archivo + pantala en una misma linea

def Print (dato,log=0):
    
    if log>0  : # solo presento y guardo en log cuando le mando 1 o mayor  
        tab='\n\t' # nueva linea y 1 tabulador 
        x = datetime.datetime.now() # fecha hora actual 
        
        # regenero el valor de fecha y hora a fecha hora minuto segundo ms
        Log_info= str(str(x.strftime('%F')+' '+x.strftime("%H%M%S%f"))+' ')+'-log => '+ str(dato)
        
        if log>1: # solo imprimo por pantalla si es valor 2 o mayor 
            if log==3 :
                
              
                print(Log_info+' '*(150-len(Log_info)),end='\r')
               
            else:
                print(Log_info)# salgo por pantalla
            
        with open(Directorio_log+'/' +Archivo_log + '.txt','a') as archivo:# abrir archivo y añadir fecha+dato
            try:
               
                archivo.write(str(Log_info + "\n"))
                
            except Exception as e:
                print(('Guardando log  error ====>',e))
                archivo.write(str(e))
print ('funciones Print creada  ')
####################################################################################################################
# reproducir un sonido 
def beep (NSound=0):
    if NSound==0:
         winsound.PlaySound("SystemBeep", winsound.SND_ALIAS)
    if NSound==1:
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
print ('funciones beep creada  ')


# In[ ]:





# In[4]:


# inicializar  directorios  
Directorio_raiz='climaPanda/'# versión de programa 
Directorio_datos=Directorio_raiz+'DataPanda' # variables de directorio raiz
Directorio_config=Directorio_raiz+'ConfigPanda' # directorio archivos de configuracion
Directorio_log=Directorio_raiz+'LOGpanda' # directorio de log

Directorio_Data_Path=Path(Directorio_datos)
Directorio_config_Path=Path(Directorio_config)
Directorio_log_Path =Path(Directorio_log)
Directorio_raiz_Path=Path(Directorio_raiz)


# comprobar si existe el directorio raiz donde contendrá los archivos maestros de cada estación y crearlo
if Directorio_raiz_Path.exists() :
    print ((('precarga  el directorio {} existe '.format(Directorio_raiz),Path(Directorio_raiz).exists())))
else:
    print (('precarga  el directorio {} * NO * existe '.format(Directorio_raiz),Path(Directorio_raiz).exists()))
    Directorio_raiz_Path.mkdir()

# inicializolos archivos de  log....
Archivo_log = str(datetime.datetime.now())
Archivo_log ='log '+ re.sub('\:|\"|\-','',Archivo_log[:-7])
Archivo_log_Error='Errores_revisar '+Archivo_log[3:]
log=1# variabe que gestiona si se presentan mensajes por pantalla y archivolog

# comprobar si existe el directorio LOG y crearlo 
if Directorio_log_Path.exists() :
    Print(('Archivo log ....',Archivo_log),1)
    Print(('Archivo log_Error ....',Archivo_log_Error),1)
    Print ((('Precarga  ',' el directorio LOG existe ',Path(Directorio_log).exists())),log)
else:
    print(('Archivo log ....',Archivo_log),1)
    print (('Precarga ',' el directorio LOG * NO * existe ',Path(Directorio_log).exists()),log)
    Directorio_log_Path.mkdir()

# comprobar si existe el directorio data donde contendrá los archivos maestros de cada estación y crearlo
if Directorio_Data_Path.exists() :
    Print ((('Precarga ',' el directorio Data existe ',Path(Directorio_datos).exists())),log)
else:
    Print (('Precarga ',' el directorio Data * NO * existe ',Path(Directorio_datos).exists()),log)
    Directorio_Data_Path.mkdir()
    
# comprobar si existe el directorio config donde contendrá los archivos de config de la aplicacion y crearlo
Archivo_conf='config.txt'
if Directorio_config_Path.exists() :
    Print (('Precarga  ',' el directorio Config existe ',Path(Directorio_config).exists()),log)
else:
    Print (('Precarga ',' el directorio Config * NO * existe *-lo voy a crear-* ',Path(Directorio_config).exists()),log)
    Directorio_config_Path.mkdir()
    


# In[ ]:





# In[ ]:





# In[5]:


def Log_Error (dato,log=1):
    
    if log==1  : # solo presento y guardo en log cuando le mando 1 
        tab='\n\t' # nueva linea y 1 tabulador 
        x = datetime.datetime.now() # fecha hora actual 
        
        # regenero el valor de fecha y hora a fecha hora minuto segundo ms
        Log_info= str(str(x.strftime('%F')+' '+x.strftime("%H%M%S%f"))+' ')+'-log => '+ str(dato)
        
        #print(Log_info)# salgo por pantalla
        
        with open(Directorio_log+'/' +Archivo_log_Error + '.txt','a') as archivo:# abrir archivo y añadir fecha+dato
            try:
               
                archivo.write(str(Log_info + "\n"))
                
            except Exception as e:
                Print(('Error Guardando log_error ====>',e))
                archivo.write(str(e))
print ('funciones Log_Error creada ')


# In[6]:


def Exist_Archivo_Ruta (Directorio_datos,directorio_o_archivo,log=0):
       
        #print(Directorio_datos,directorio_o_archivo)
        directorio_o_archivo=Directorio_datos +'/'+ directorio_o_archivo
        Directorio_Data=Path(directorio_o_archivo)
        Print(('verificar si existe',Directorio_Data),log)
        if Directorio_Data.exists() and Directorio_Data.stat().st_size>10 :
            Print (('funciones ' , ' el directorio/archivo  existe ',Directorio_Data.exists),log)
            return True
        else :
            return False
print ('funciones Exist_Archivo_Ruta creada ')      


# In[7]:


# establezco la ruta con el archivo (ruta +archivo)
def RutaCompuesta(Ruta,Nombre_archivo,log=1):
    if Ruta=='':
        Nombre_archivo=  Nombre_archivo
    elif Ruta[-1]!='/':
        Ruta += '/'
        Nombre_archivo= Ruta  + Nombre_archivo
    Print(('RutaCompuesta :', Nombre_archivo),log)
    return Nombre_archivo
print ('funciones RutaCompuesta creada ') 


# In[8]:


def Abrir_archivo_df (Ruta,Nombre_archivo,Delimt=',',Head=0,log=1):
    
    Ruta=RutaCompuesta(Ruta,Nombre_archivo) # obtengo ruta final del archivo 
    
    if Path(Ruta).exists() :# si ruta existe 
        
        try:
            # leer csv y pasarlo a un datframe de panda      Estaciones_df = pd.read_csv("Estaciones.csv",delimiter=";", encoding='latin1')
            Print( ('@ Ruta:', Ruta),log )
            Archivo_df = pd.read_csv(Ruta,delimiter=Delimt, encoding='latin1')
            
           
            #Print(Estaciones_df,log)

            return Archivo_df
        
        except Exception as e:
            Print(('¡¡¡Abrir_archivo_df   Exception¡¡¡¡',e),1)
            Log_Error(('¡¡¡Abrir_archivo_df   Exception¡¡¡¡',e),1)
            return False
   
    return False
    
    
print ('funciones Abrir_archivo_df creada ')  
    


# In[9]:


# guardar en archivo csv
def Guardar_archivo_df(Archivo_df ,Ruta,Nombre_archivo,Delimt=',',log=0):
    #print(Archivo_df)
    Ruta=RutaCompuesta(Ruta,Nombre_archivo) # obtengo ruta final del archivo 
    
    if Ruta : # si ruta existe se guarda
   
        try:
            #print(Archivo_df)
            Archivo_df.to_csv(Ruta, encoding='latin1', header=True, index=False)
            return True
       
    
        
        except Exception as e:
            Print(('¡¡¡Guardar_archivo_df   Exception¡¡¡¡',e),1)
            Log_Error(('¡¡¡Guardar_archivo_df   Exception¡¡¡¡¡¡',e),1)
            return False
    return False
print ('funciones Guardar_archivo_df creada ') 


# In[10]:


def Abrir_archivo (Ruta,Nombre_archivo,log=1):
    
    Ruta=RutaCompuesta(Ruta,Nombre_archivo) # obtengo ruta final del archivo 
    
    if Path(Ruta).exists() :# si ruta existe 
        
        with open(Ruta,'r') as archivo:# abrir archivo para lectura
              
            try:
                # leer archivo
                Print( ('Abrir_archivo @ Ruta:', Ruta),log )
                #Archivo = pickle.load(archivo)
                #templist = json.load(temp_op)
                #Archivo = archivo.read()#.splitlines()
                Archivo = json.load(archivo)
                Print(Archivo,log)

                return Archivo

            except Exception as e:
                Print(('¡¡¡Abrir_archivo   Exception¡¡¡¡',e),1)
                Log_Error(('¡¡¡Abrir_archivo   Exception¡¡¡¡',e),1)
                return False
   
    return False
    
    
print ('funciones Abrir_archivo creada ')  
    


# In[11]:


import json

itemlist = [21, "Tokyo", 3.4]
with open('opfile.txt', 'w') as temp_op:
    json.dump(itemlist,temp_op)
with open('opfile.txt', 'r') as temp_op:
    templist = json.load(temp_op)
print(templist,type(templist))


# In[12]:


def Guardar_archivo (Archivo ,Ruta ,Nombre_archivo,log=1):
   Ruta=RutaCompuesta(Ruta,Nombre_archivo) # obtengo ruta final del archivo 
   Ruta=Path(Ruta)
   print(Ruta)
   if Ruta.exists() or not Ruta.exists() :# si ruta existe se preguntará si desea sobrescribir (cambios futuros)

        with open(Ruta,'w') as archivo:# abrir archivo
               try:
                   print('guardar archivo')
                   #pickle.dump(Archivo, archivo)
                   json.dump(Archivo,archivo)
                   #archivo.write(Archivo)
                   print('Archivo',type(Archivo))

               except Exception as e:
                   Print(('Guardar_archivo: error ====>',e))
print ('funciones Guardar_archivo creada ')                   


# In[13]:


# Precarga *** carga e inicialización de variables y  datos  
#Inicializar variables
control=0
log=1   
# establezco fechas en español  nombre del mes  dia etc
Print('estabecer fechas en español',log=1)
locale.setlocale(locale.LC_TIME, "es_ES") 
# para mostrar las url completas  en el dataframe
pd.set_option('display.max_colwidth', 155)
# para forzar a descargar de nuevo las estaciones que dan error 
reintentar=False
# definir diccionario de dirección viento calma=0, norte:1,etc,etc  Nordeste  Noroeste
Direccion_viento={'Calma':0,'Norte':1,'Noroeste':2,'Oeste': 3,'Sudoeste':4,'Sur':5,'Sudeste':6,'Este':7,'Nordeste':8}
Print(('Dic Direccion_viento',Direccion_viento),log=1)
ln='\n'
lntab='\n\t'
tab='\t'

#intento obtener los datos de congig y si no los establezco con valores default.
if Exist_Archivo_Ruta(Directorio_config,Archivo_conf):
    
    config=Abrir_archivo(Directorio_config,Archivo_conf)
    
    
    Minutos=config[0]['Minutos']
    En_ejecucion=config[0]['En_ejecucion']
    Direccion_viento=config[1]
    print('Minutos',Minutos,'En_ejecucion',En_ejecucion)
else:
    
  
    Minutos=15 # 1cada 15 minutos por defecto
    En_ejecucion=False
    config_dic={'Minutos':Minutos,'En_ejecucion':En_ejecucion}
    Direccion_viento={'Calma':0,'Norte':1,'Noroeste':2,'Oeste': 3,'Sudoeste':4,'Sur':5,'Sudeste':6,'Este':7,'Nordeste':8}
    config=[]
    config.append(config_dic)
    config.append(Direccion_viento)
    #config=str(config)
    Guardar_archivo(config,Directorio_config,Archivo_conf)   
    print(config_dic)
    


# In[14]:


type(Direccion_viento)


# In[15]:


# crear config de estaciones con url 
def crear_Estaciones_df(Estaciones_df): # crea el archivo de estaciones(en config) y añade la URL
    print ('@@@@@',Estaciones_df)
    x=datetime.datetime.now()
    
    #str(x.strftime('%F')+' '+x.strftime("%H%M%S%f")
   
    Estaciones_df['ACTUALIZADO']=(x.strftime('%F')+' '+x.strftime("%H:%M:%S"))
    
    # añadir las URL
    Estaciones_df['URL']=list(map(lambda url:'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos_'\
                +url+'_datos-horarios.csv?k=coo&l='\
                +url+'&datos=det&w=0&f=temperatura&x=',Estaciones_df['INDCLIM']))
    return Estaciones_df
print ('funciones crear_Estaciones_df creada ') 


# In[16]:


# descargar los datos de la url

def Descagar_data_URL(remote_url,log=0):
    try:
        data = requests.get(remote_url) # descargar  la URL
        if data :
            return data.text # retorna los datos en texto
        else:
            return False # si  falla retorna falso 
        
    except Exception as e:
            Print(('¡¡¡Descagar_data_URL   Exception¡¡¡¡',e),1)
            Log_Error(('¡¡¡Descagar_data_URL   Exception¡¡¡¡¡¡',e),1)
            return False
    return data.text
print ('funciones Descagar_data_URL creada ') 


# In[17]:


# lista de estaciones extraer de la web los INDCLIM y resto de datos
#comparar con las existentes y actualizar el listado 4
# inicializo dataframe de estaciones 
Estaciones_df=''
columnas='INDCLIM','INDSINOP','NOMBRE','PROVINCIA','LATITUD','LONGITUD','ALTITUD','ACTUALIZADO','URL'
Estaciones_df=pd.DataFrame(columns =columnas)

#Estaciones_df.reindex


def Actualizar_estaciones(Estaciones_dfNew=Estaciones_df ,log=1):
    
        if 'Empty DataFrame' in Estaciones_dfNew : # si no tiene valores anteriores 
            print(' vacio de ')
            sys.exit('detener aqui  stop')
        else:
            print ('numero de Estaciones_df actuales',len(Estaciones_dfNew))
            
        Urlcomunidades=(['https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=esp&w=0',
                         'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=and&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=mur&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=val&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=clm&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=ext&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=mad&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=arn&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=cat&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=cle&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=rio&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=nav&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=pva&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=can&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=ast&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=gal&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=bal&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=coo&w=0',
                        'https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=and&l=6302A&w=0&datos=det&f=temperatura'])
        Estaciones=[]
        for URL in Urlcomunidades[1:-1]:

            # descargo la web de la comunidad para obtener lista e estaciones de cada comunidad 
            data=Descagar_data_URL(URL,log)
            Print (('Actualizar_estaciones url comunidades ',URL),1)
           

            #print ('data sin reducir tiene tamaño de :',len(data))
            
            #reduzco el tamaño de data solo con lo que necesito desde pos a pos2
            pos=data.find('<optgroup label=')
            
            pos2=data.find('</select>',pos) #</optgroup>
            
            
            data=data[pos:pos2] # data ¡ya esta reducida 
            
            esplit=data.split('<optgroup label="') # separo por provincias 
            
            
            
                
            #busco las provincias 
            #ProvinciaFind='<optgroup label="'
            
            control =0


            for data in esplit[1:]:
                provincia=data[0:data.find('">')]
                PosFinal=len(provincia)
                maxData=len(data)
                control=0
                Print (('Provincia', provincia),log)
                while  PosFinal<maxData and PosFinal>0:

                    control+=1

                    cadena='<option value="'
                    posIni=data.find(cadena,PosFinal)+len(cadena)
                    if posIni<0 :
                        break
                    cadena='</option>'
                    PosFinal=data.find(cadena,posIni)
                    
                    datasalida=data[posIni:PosFinal]
                    
                    datasalida=[provincia]+datasalida.split('">')
                    Estaciones.append(datasalida)
                    

                    if data.find(cadena,PosFinal+10)<0 :
                        break
                Print(('Encontradas ',control,'Estaciones en:',provincia ),log)
                Print('Total por ahora  {} '.format(len(Estaciones)),1)
                
            # obtener ahora el resto de parametros de cada estacion , latitud, longitud, altura
        
        control=len(Estaciones)+1
        Totalestaciones=len(Estaciones)
        Print ('Preparado para agregar{} Estaciones '.format (str(len(Estaciones))),log)
        #Print(str(len(Estaciones)),log)
        #Print(Estaciones,0)
        for INDCLIM in Estaciones:
            
            #  Control para pruebas y limite de busquedas a 200 staciones 
            control-=1
            Print(('Control',control),0)
            if control==0:
                break 
            if INDCLIM[1] in Estaciones_df.INDCLIM.values :
                Print(( INDCLIM[1], ' ya existe en dataframe '),3)
                continue 
            URL='https://www.aemet.es/es/eltiempo/observacion/ultimosdatos?k=and&l={INDCLIM}&w=0&datos=det&f=temperatura'
            URL=URL.format(INDCLIM=INDCLIM[1])
           # descargar url datos de la estacion 
            data=Descagar_data_URL(URL.format(INDCLIM=INDCLIM),log)


            if data :

                #print(INDCLIM, len(data)) solo necesito la informacion entre inicio y fin 
                # inicio Actualizado:</span>&nbsp;
                # fin /abbr>&nbsp;-&nbsp;
               
                # reducir data a los valores extrictamente necesarios ( reducir memoria )
                pos=data.find('Actualizado:</span>&nbsp;')+len('Actualizado:</span>&nbsp;')
                pos2=data.rfind('/abbr>&nbsp;-&nbsp;',pos) 
            
                data=data[pos:pos2] # data ¡ya esta reducida 

               
                #buscando la FechaActualizado
                pos2=data.find('&nbsp')
                FechaActualizado=data[:pos2]  # FechaActualizado
                #print(FechaActualizado)
                
                #buscando la altitud
                pos=data.find('Altitud (m)</span>:&nbsp;')+len('Altitud (m)</span>:&nbsp;')
                pos2=data.find('<br/>',pos)
                altitud=data[pos:pos2]       # altitud
                #print(altitud)

                
                pos=data.find('&#176;',pos2)
                posIni=data.find('>',(pos-5))
                PosFinal=data.find('<',pos)
               # print(pos,posIni,PosFinal)
                Latitud=data[posIni+1:PosFinal]   #Latitud
               # print(Latitud)
                Latitud=Latitud.replace('&#176;',',').replace("''",',').replace("'",',').replace(' ','')
                esplit=Latitud.split(',')
                Latitud=esplit[0].zfill(2)+esplit[1].zfill(2)+esplit[2].zfill(2)+esplit[3]
               # print(Latitud)

            
                # buscando la Longitud
                pos=data.find('&#176;',PosFinal)
                posIni=data.find('>',pos-5)
                PosFinal=data.find('<',pos)
                Longitud=data[posIni+1:PosFinal]   #Longitud
                # print(Longitud)
                Longitud=Longitud.replace('&#176;',',').replace("''",',').replace("'",',').replace(' ','')
                esplit=Longitud.split(',')
                Longitud=esplit[0].zfill(2)+esplit[1].zfill(2)+esplit[2].zfill(2)+esplit[3]
                # print(Longitud)
                
                
                #calcular la URL a partir de INDCLIM
                URL='https://www.aemet.es/es/eltiempo/observacion/ultimosdatos_'\
                +INDCLIM[1]+'_datos-horarios.csv?k=coo&l='\
                +INDCLIM[1]+'&datos=det&w=0&f=temperatura&x='
            
            # ahora la pasamos al dataframe 
            # ..........pensar si se deberia actualizar siempre aunque ya exista .....
               
                
                if len(Estaciones_dfNew)==0: # si no existia el dataframe será 0
                    # agrego lA primera estación
                    Print('añadir primera linea  , Estaciones_df',log) 
                    fila=len(Estaciones_dfNew.index)#+1 len es cero para el primero , y asi ssucesivamente 
                    Estaciones_dfNew.loc[fila] = [INDCLIM[1],'',INDCLIM[2],INDCLIM[0],Latitud,Longitud,altitud,'',URL]
                    Print( Estaciones_dfNew.loc[fila][2],log)
                else:#(len(Estaciones_df)==0) # si ya existia verifico si existe o se ha de guardar 
                    
                    #print('******', INDCLIM[1])
                    if INDCLIM[1] in Estaciones_df.INDCLIM.values : # verifico si ya existe
                    
                        Print(('Progreso {:.2f}'.format((100*(control)/Totalestaciones)),'%', INDCLIM[1], ' ya existe en dataframe '),3)
                        #print('fila   *******************  ', fila )

                    else :#(INDCLIM[1] in Estaciones_df[INDCLIM].values)

                        Print(('Progreso {:.2f}'.format((100*(control)/Totalestaciones)),'agregando a Estaciones_df'),3) 
                        Print(len(Estaciones_dfNew),0)
                        Print(len(Estaciones_dfNew.index),0)
                        fila=len(Estaciones_dfNew.index)#+1 len es cero para el primero , y asi ssucesivamente 
                        #Agrego la serie ([INDCLIM[1],'',INDCLIM[2],INDCLIM[0],Latitud,Longitud,altitud,'',URL])

                        Estaciones_dfNew.loc[fila] = [INDCLIM[1],'',INDCLIM[2],INDCLIM[0],Latitud,Longitud,altitud,'',URL]
                        #Print('aqui estoy1 ',3)
                        #Print( Estaciones_dfNew.loc[fila][2],log)
                        #Print('aqui estoy2 ',3)
                        #print('fila', fila )
            else: #(if data)  
                Print(('*****NO se pudo obtener **********',INDCLIM),log)
                    
        Print (('Nº estaciones resultantes ',len(Estaciones_dfNew.index)),log)           
        #Estaciones_df=Estaciones_df.reset_index(drop= True)              
        #print(Estaciones)
        #Print (('Nº estaciones ',len(Estaciones_df)),log)
        #Log=0
        #return Estaciones
        print(len(Estaciones_dfNew))
        #sys.exit('parar aqui  de momento stop') 
        if len(Estaciones_dfNew)>0:
            return Estaciones_dfNew
        print ('retorno l mismo que me han entregado')
        return Estaciones_df
        
        #a partir de aqui no se ejecuta nunca
        
        archivo='Estaciones_df.csv'
        
        if Guardar_archivo_df(Estaciones_df,Directorio_config,archivo,log=0):
            print ('Guardando ',archivo) # guardarlo a disco 
        else :
            print ('No se ha podido guardar' )
            
        ##INDCLIM,INDSINOP,NOMBRE,PROVINCIA,LATITUD,LONGITUD,ALTITUD,ACTUALIZADO,URL
print ('funciones Actualizar_estaciones creada ') 


# In[ ]:






# In[18]:


# para poder ejecutar cada cierto tiempo el programa 

from time import sleep
from threading import Timer
#from datetime import datetime
import time

# iniciar cada cierto tiempo 
Minutos=15 # tiempo para ejecutar próxima actualización 

class MyInfiniteTimer():
    """
    A Thread that executes infinitely
    """
    ############################################################################################
    # averiguar como puedo poner codigo para pulsar una tecla y que detenga automaticamente el programa 
    # ejemplo saber cual es la ultima tecla pulsada en el sistema y si es tal hacer cual ....
    #print (self.t)
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)
        
    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()
        
    def start(self):
        print(datetime.datetime.now(),'Iniciar cada ',self.t ,'seg.',self.t/60,'Minutos')
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()
        return True
        
    def cancel(self):
        print(datetime.datetime.today(),'Parar Temporizador ',self.hFunction )
        self.thread.cancel()
        return False

print ('funciones Class MyInfiniteTimer creada ') 


# In[19]:


def Inicio_automatico(Minutos,t=0):
    
    En_ejecucion=False
    if Minutos>0 :
        if not t:
            t = MyInfiniteTimer(Minutos*60, Programa_ejecutar) # valor en segundos >>>> 30*60 = 30 minutos 
            En_ejecucion=t.start()
            Print (('Ejecutandose cada ',Minutos,'Minutos =',En_ejecucion),log)
            thread = Timer(1, Programa_ejecutar() )# se ejcuta una vez en el momento de activarlo
        else:
            En_ejecucion=t.start()
            
    
    return t,En_ejecucion
# iniciar cada cierto tiempo 
print ('funciones Inicio_automatico creada ') 


# In[28]:


def Stop_automatico(t):
    # detener programa 
    print('t antes es  es :',t)
    En_ejecucion=t.cancel()
    Print (('Ejecutandose =',En_ejecucion),log)
    print('t ahora es :',t,En_ejecucion)
    
    return En_ejecucion
    # detener programa 
print ('funciones Stop_automatico creada ') 


# In[21]:


def Programa_ejecutar(reintentar=False, log=1):
    Print(('Inicio de programa '),log)
    #print(reintentar)
    TInicio=datetime.datetime.now() # tiempo de inicio para determinar la duracion del proceso al final 
    Print (TInicio,1)
    N=0
    data=False
    Errores_descargas=""
    Totalestaciones=len(Estaciones_df)
    # descarga los datos de cada estación de la web 
    for index,INDCLIM in  enumerate( Estaciones_df['INDCLIM']): # itera por cada estación metereológica
        
        Print(('Estación nº {} INDCLIM '.format(index)+INDCLIM+'  Progreso {:.2f}'.format((100*(1+index)/Totalestaciones)),' %'),3) # numero ordinal de estacion e index del dataframe
        
        Print (('Obteniendo información nueva de:',INDCLIM, Estaciones_df.loc[index]['NOMBRE']),log)
        
        
        #Print(end='\r')
        URL=Estaciones_df.loc[index]['URL'] # extraemos la URL de Estaciones_df
        
        if Estaciones_df.loc[index, 'ACTUALIZADO']=='0000-00-00 00:00' and reintentar==False : # tiene problemas de descarga
            Print ('No descagado porque esta marcado como  Erróneo ',1)
            continue # reinicia/continua proxima estación
        
        data=Descagar_data_URL(URL,log) # descargar los datos de la web y guardarlos en data
        
        if data==False or 'html'  in data:# verificar si la descarga es correcta Html indicaria una pagina web,no un csv.

                Print ((INDCLIM, ' ***** No se ha podido descargar *****'),log)
                Log_Error((INDCLIM, ' ***** No se ha podido descargar de su url *****', ),log)
                Errores_descargas += '\n'+INDCLIM+' '+str( Estaciones_df.loc[index][2])+'\t\t** No se ha podido descargar ****'
                #Log_Error(Errores_descargas)
                Print ('Estableciendo como  estación  descarga incorrecta',1)
                Estaciones_df.loc[index, 'ACTUALIZADO']='0000-00-00 00:00'
                continue # reinicia/continua proxima estación
       
        
        Data_Estacion_df=pd.read_csv(StringIO(data),header=2) # pasar los datos a un dataframe llamado Data_Estacion_df

        archivo_principal=INDCLIM+'.csv' # utilizo el INDCLIM (indicador climatico) para determinar el archivo general
        
        # creo el index con las fechas-hora y las ordeno 
       

        Data_Estacion_df['INDEX']=Data_Estacion_df['Fecha y hora oficial']
        Data_Estacion_df.set_index('INDEX',inplace = True)
        Data_Estacion_df.sort_index(inplace=True)
       
        # comprobar si existe el archivo en disco para añexar la información o bien crarlo 
        if Exist_Archivo_Ruta(Directorio_datos,archivo_principal,log) :

            # si existe se agrega 
            Print('Agregar info al archivo ',log)
            # obtener(leer) el archivo 

            DataDisco_Estacion_df=Abrir_archivo_df(Directorio_datos,archivo_principal,Delimt=',',log=1)
           

            # si no tiene la columna INDEX la agrego ( uso la fecha['Fecha y hora oficial'] como indice de cada dato)
            if DataDisco_Estacion_df.columns[0]=='Fecha y hora oficial' :
                #print(archivo_principal)
                #duplico la columna 'Fecha y hora oficial' a la INDEX
                DataDisco_Estacion_df['INDEX']=DataDisco_Estacion_df['Fecha y hora oficial']
            else:
                # el archivo existe pero no es un dataframe correcto 
                Print ('Existe pero no es un dataframe válido y lo vamos  a crear ',log)
            
                # como no existe el archivo en disco se guarda el dataframe de datos actual
                if Guardar_archivo_df(Data_Estacion_df,Directorio_datos,archivo_principal,log=0):
                    Print (('Guardando/sobreescribir :',archivo_principal),1) # guardarlo a disco 
                    #DataDisco_Estacion_df['INDEX']=DataDisco_Estacion_df['Fecha y hora oficial']
                    continue
                else :
                    Print ('No se ha podido guardar',1 )
                    Log_Error('No se ha podido guardar DataDisco_Estacion_df')
                    continue
                #Fecha y hora oficial
            #Establezco como indice del dataframe la columna index (para poder agregar directamente por la fecha ) 
            DataDisco_Estacion_df.set_index('INDEX',inplace = True)
            
            #recorro cada dato nuevo obtenido 
            for fila in Data_Estacion_df.iterrows():
              
                # guardo directamente cada linea de datos por su fecha en el dataframe del disco.
                # si ya existe se actauliza a la ultima lectura y si no existe se añade al Dataframe.
                DataDisco_Estacion_df.loc[fila[0]]=fila[1]

             


            # ordeno el df no necesaro porque ordenamos de primeras los datos de antiguo a nuevo 
            # mantengo estas lineas de comnetario por si en algun momento es interesante ordenar a la inversa.
            #DataDisco_Estacion_df.sort_index(inplace=True)

           
            # guardamos el dataframe de disco al disco 
            if Guardar_archivo_df(DataDisco_Estacion_df,Directorio_datos,archivo_principal,log=0):
                Print (('Guardando/actualizando : ',archivo_principal),log) # guardarlo a disco 
            else :
                Print ('No se ha podido guardar DataDisco_Estacion_df',log )
                Log_Error('No se ha podido guardar DataDisco_Estacion_df')
        else:

            # cuando no existe DataDisco_Estacion_df'   se crea el archivo 
            Print ('no encontrado se va a crear ',log)
            
            # como no existe el archivo en disco se guarda el dataframe de datos actual
            if Guardar_archivo_df(Data_Estacion_df,Directorio_datos,archivo_principal,log=0):
                Print (('Guardando/creando :',archivo_principal),1) # guardarlo a disco 
            else :
                Print ('No se ha podido guardar',1 )
                Log_Error('No se ha podido guardar DataDisco_Estacion_df')
        
        # fonalmente actualizamos la fecha de atualizacion en el Estaciones_df
        
        x=datetime.datetime.now()
    
        #Estaciones_df['ACTUALIZADO']=(x.strftime('%F')+' '+x.strftime("%H:%M"))
        ##INDCLIM,INDSINOP,NOMBRE,PROVINCIA,LATITUD,LONGITUD,ALTITUD,ACTUALIZADO,URL
        control=0 # para activar pruebas con 10 estaciones 
        serie=Estaciones_df.loc[index, 'ACTUALIZADO']
        #print ('serie',serie)
        Estaciones_df.loc[index, 'ACTUALIZADO']=(x.strftime('%F')+' '+x.strftime("%H:%M"))
       # y guardamos Estaciones_df
        if Guardar_archivo_df(Estaciones_df,Directorio_config,archivo,log=0):
            Print ('Guardando Estaciones_df',log) # guardarlo a disco 
        else :
            Print ('No se ha podido guardar Estaciones_df final de programa' ,log)
            Log_Error ('No se ha podido guardar Estaciones_df final de programa' ,log)
        # usado en las pruebas rapidas para descargar solo algunas estaciones en vez de todas ....
        if N==10 and control!=0:
            break
        N+=1
    Errores_descargas+='   '  
    log=2
    Print ('\nEjecutado en : {}  '.format(str(datetime.datetime.now()-TInicio)),log)
    #Print(datetime.datetime.now()-TInicio,1)
    
    Print('Errores descargas :{}'.format(Errores_descargas),log)
    #Print(Errores_descargas,log)
    Log_Error(Errores_descargas)
    return 
    winsound.PlaySound("SystemBeep", winsound.SND_ALIAS)   
print ('funciones Programa_ejecutar creada ') 


# In[22]:


def Duplicados(log=1):
    D=0
    # buscar duplicados 
    for index,valor in    enumerate(Estaciones_df['INDCLIM'].duplicated()):
        if valor==True:
            Print ((index,valor),log)
            Print (Estaciones_df.loc[index],log)
            D=+1
        else:
            Print (('No hay duplicados',valor,),log)
    Print('{} duplicados encontrados '.format(str(D)),log)    
print ('funciones Duplicados creada ')           


# In[ ]:





# In[23]:


# cargar la configuracion previa o inicializarla 

# si hay archivos CFG de configuracion los cargo y si no,  los cargo a partir del archivo estaciones csv

archivo='Estaciones_df.csv' # Determino archivo de configuración
if Exist_Archivo_Ruta(Directorio_config,archivo,log=1):
    Print (('Leer configuracion de archivos en disco:',archivo),log=1)
    Estaciones_df=Abrir_archivo_df(Directorio_config,archivo,Delimt=',',log=1)
    
else:
    # si no existe hay que crearlo el archivo maestro propio o de la web 
    archivo='Estaciones.csv' 
    if Path(RutaCompuesta(Directorio_config,archivo)).exists():
        
        Print (('Leer configuracion de archivos en disco:',archivo),log=1)
        # Crearlo a partir de estaciones.csv añadiendo las url
        Estaciones=Abrir_archivo_df(Directorio_config,archivo,Delimt=';',log=1)
        print ('@',Estaciones)
        Estaciones_df=crear_Estaciones_df(Estaciones)
        archivo='Estaciones_df.csv'
        #Estaciones_df=crear_Estaciones_df(Abrir_archivo_df(Directorio_config,archivo,log=0)) 
       
    else : # si no existen archivos de estaciones guardados lo creamos desde la web 
        archivo='Estaciones_df.csv'
        Print (('Leer configuracion de estaciones desde la web ....:'),log=1)
        Estaciones_df=Actualizar_estaciones() # actualiza el archivo a partir de la web 
    
    # guardamos el archivo Estaciones_df (contienen listado de estaciones y información sobre estas )
    if Guardar_archivo_df(Estaciones_df,Directorio_config,archivo,log=1):
        Print (('Guardando ',archivo),1) # guardarlo a disco 
    else :
        Log_Error ('No se ha podido guardar Estaciones_df' )

print (' Inicializar variables  listo') 


# In[24]:


menus=[]
for n in range(15):
    menus.append('menu' + str(n))
#menus[]=
menus[0]='0-Reintentar estaciones fallidas? {} '.format(reintentar)
menus[1]='1-Actualizar datos mas recientes  ' 
menus[2]='2-Actualizar lista de  Estaciones'
menus[3]='3-Actualizar automaticamente cada {} minutos'.format(Minutos)
menus[4]='4-Verificar si hay estaciones duplicadas '
menus[5]='5-***opcion 3 Establecer tiempo para  datos automáticos'
menus[6]='6-Mostrar Estaciones Metereológicas'
menus[7]='7-***opcion 3 y enter general Detener captura automática'
menus[8]='8-***opcion 3 Estado de ejecución automática=>{}'.format(En_ejecucion)
menus[9]='9-  **Finalizar** '
menus[10]=ln+'\n**********  Programa para leer datos de {} estaciones\
metereológicas ("Fuente web de Aemet") *******\n\n\t-Menú de opciones:\n'.format(len(Estaciones_df))
menus[11]='valores posibles:  \n => 0 Actualizar 1 vez  \n => X(5 a 1430) \
Actualiza a intervalos de X minutos \n => "Enter" volver a menú '

def menu_lista():
   
    print (menus[10]) 
    print (menus[0] +int(8-round(1+len(menus[0]))/8)*tab +menus[5])
    print (menus[1] +int(8-round(1+len(menus[1]))/8)*tab +menus[6])
    print (menus[2] +int(8-round(1+len(menus[2]))/8)*tab +menus[7])
    print (menus[3] +int(8-round(1+len(menus[3]))/8)*tab +menus[8])
    print (menus[4] +int(8-round(1+len(menus[4]))/8)*tab +menus[9])

    


# In[ ]:





# In[ ]:


# clear_output()(wait=True)
menu='?'
import os

t=0
retorno='\r'*15
Onetime=True
    
while menu!=9:
    try:
        menus[8]='8-***opcion 3Estado de ejecución automática=>{}'.format(En_ejecucion)
        
        if not  En_ejecucion:
               
            menus[3]='3-Actualizar automaticamente cada {} minutos :OFF'.format(Minutos) 
        else:
            
            menus[3]='3-Descargando automaticamente cada {} minutos :ON'.format(Minutos)
            
         
       
        menus[0]='0-Reintentar estaciones fallidas? {} '.format(reintentar)
        sleep(1.1)
        menu_lista()
        
        sleep(0.5)
       
        print('',end=retorno)
        
        if En_ejecucion and Onetime:
            Onetime=False # solo lo ejecutamos al iniciar una vez 
            if t:
                t,En_ejecucion=Inicio_automatico(Minutos,t)
            else:
                t,En_ejecucion=Inicio_automatico(Minutos)
                
            
        menu=input ('Selecciona una opción(0-9) o "Enter" activa/desactiva descarga automática',).lower()
        
         # Intentando borrar consola en pantalla
        #print("\033c", end='')
        clear_output()
        #system('clear') 
        os.system('cls' if os.name == 'nt' else 'clear')
        sleep(0.1)  # Time in seconds
        
        
        
        
        if len(menu)==1 and menu.isnumeric():
            
            menu=int(menu)
            
            if menu==1:
                print('Opción 1 --- Actualizar datos ultimas 24 hrs ')
                Programa_ejecutar(reintentar)
                
            elif menu==2:
                print('Opción 2 --- Actualizar_estaciones  ahora hay :',len(Estaciones_df))
                archivo='Estaciones_df.csv'
                Estaciones_df2=Actualizar_estaciones(Estaciones_df,log=3)
                if Guardar_archivo_df(Estaciones_df2,Directorio_config,archivo,log=1):
                    Print (('Guardando ',archivo),1) # guardarlo a disco 
                else :
                    Log_Error ('No se ha podido guardar Estaciones_df' )
           
            elif menu==3:
                minuto=str(Minutos)
                print (menus[3]+ln+menus[11]) # submenu en pantalla 
                sleep(0.01)
                minuto=input ('Tiempo actual {} min.¿Cada cuantos minutos quieres? "0"= 1 vez'.format(minuto))
                
                if minuto=='':
                    minuto=str(Minutos)
                    
                if minuto.isnumeric:
                    minuto=int(minuto)
                    
                    if minuto==0: # paramos la descarga automatica y realizamos una sola descarga(en)
                        Minutos=int(minuto)
                        t,En_ejecucion=Inicio_automatico(Minutos,t)
                       
                    else:    # activamos la captura automatica 
                        minuto+=(5-int(minuto))*(minuto<5)
                        Minutos=int(minuto)
                        t.t=Minutos
                        clear_output()
                        print ('Tomaremos datos cada {} min '.format(minuto))

                        if not t:# si está activa no se activa de nuevo 
                  
                            t,En_ejecucion=Inicio_automatico(Minutos)
                   
                
                
            elif menu==4:
                print('Opción 4 --- buscar duplicados en Estaciones_df')
                Duplicados(3)
                
            elif menu==5:
                minuto=str(Minutos)
                minuto=input ('T.actual {} min.¿Cada cuantos minutos quieres?'.format(minuto))
                if minuto.isnumeric:
                    Minutos=int(minuto)
                    Minutos+=(5-int(Minutos))*(Minutos<5)
                    t.t=Minutos
                    clear_output()
                    #print ('Establecido a {} minutos'.format(Minutos))
                   
                    
                    sleep(0.1)
                    #menu_lista()
            
            elif menu==6:
                print (Estaciones_df)
            
            elif menu==7:
                En_ejecucion=Stop_automatico(t)
                
            
            elif menu==8:
                
                #9print ('Opción 8')
                Print ( 'estado de ejecución automática=>{}'.format(En_ejecucion),2 )
                
                continue
                
            elif menu==9:
               
                    Stop_automatico(t)
                    if not En_ejecucion:
                        print ( ' No se ha podido detener el subproceso ')
                        
                    print ('Opción 9 >> salir <<')
                    break  
                
            elif menu==0:
                reintentar=not reintentar
                continue
                
        else:  #len(menu)==1 and menu.isnumeric()
            
            if menu=='':
                
                if En_ejecucion:
                    
                    En_ejecucion=Stop_automatico(t)
                    sleep(0.1) 
                    
                else:
                    print ('Tomaremos datos cada {} min '.format(Minutos))
                    
                    t,En_ejecucion=Inicio_automatico(Minutos,t)
            
            
            else: #  menu=='grdfdh'
                print(menu,'opción no válida ')
            
            
        reintentar=False    
            
    except Exception as e:
        Print(('¡¡¡ Menú de opciones¡¡¡¡',e),2)
        Log_Error(('¡¡¡ Menú de opciones¡¡¡¡',e),2) 
        break  
print('guardando config')
config[0]={'Minutos':Minutos,'En_ejecucion':En_ejecucion}
Guardar_archivo(config,Directorio_config,Archivo_conf)     
# menu_lista()   

print('\n\n****************************   Programa finalizado   ***************************************')
sys.exit("bye, bye ")  


# menu_lista()
# 

# In[ ]:


def buscar_estaciones_forzado():
    lista=[]
    clear_output()
    import string
    print('Iniciando estaciones a lo bruto')
    for INDCLI in range (9999):
        INDCLIM = str(INDCLI).zfill(4)
        print (INDCLIM,' ',end ='\r')
        for letra in list(''+string.ascii_uppercase):

           #print (str(INDCLIM)+' '+letra , end='\r')
            url=str(INDCLIM)+letra
            #print(url)#,end='\r')
            URL='https://www.aemet.es/es/eltiempo/observacion/ultimosdatos_'\
                    +url+'_datos-horarios.csv?k=coo&l='\
                    +url+'&datos=det&w=0&f=temperatura&x='
            data=Descagar_data_URL(URL,log) # descargar los datos de la web y guardarlos en data
            #print(url, URL)
            if data==False or 'html'  in data:
                continue

            else :
                lista.append(url)
                print('\n',url)
                #sleep(0.1)
                
    Print (lista,1)
    lista       


# In[ ]:


En_ejecucion


# In[ ]:


t.t=6*60
t.t


# In[ ]:





# In[ ]:



    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




