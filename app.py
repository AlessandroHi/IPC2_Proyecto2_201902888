from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from xml.etree import ElementTree
from Lista import Lista
from Nodo import Nodo
from Ciudad import Ciudad
from Casilla import Casilla #VALOR DE LA MATRIZ Y CARACTERISTICA
from Recurso import Recurso 
from UnidadCivil import UnidadCivil
from Entrada import Entrada
from UnidadesMilitar import UnidadesMilitar
from Robot import Robot

def cofiguracion(ruta): #ANALIZADOR DEL ARCHIVO 
  global Lista_ciudades, Lista_robots #SE HACE EL LLAMADO DE LAS VARIABLES GLOBALES GENERALES

  archivoXML = ElementTree.parse(ruta)
  root = archivoXML.getroot()

#----------------------- SE AGREGAN CIUDAD A LISTA DE CIUDADES ----------------
  for ciudades in root.iter("listaCiudades"):
    pass
    for ciudad in ciudades:
      pass
      for nombre in ciudad.iter("nombre"):
        name = nombre.text
        Nofilas = nombre.attrib["filas"]
        Nocolumnas = nombre.attrib["columnas"]

        listaRecursos = Lista()
        listaCiviles = Lista()
        listaEntradas = Lista()

      for fila in ciudad.iter("fila"):
        
        columnas = fila.text.replace('\n', "").replace('"', "")
        noFila = fila.attrib["numero"]

        contcolumna = 1
        for columna in columnas:
          if columna == "R":
           listaRecursos.append(Recurso(contcolumna,int(noFila))) 
          if columna == "E":
            listaEntradas.append(Entrada(contcolumna,int(noFila)))
          if columna == "C":
            listaCiviles.append(UnidadCivil(contcolumna,int(noFila)))
          contcolumna +=1

      Lista_ciudades.append(Ciudad(name,int(Nofilas),int(Nocolumnas),listaEntradas,listaCiviles,listaRecursos))

#----------------------- SE AGREGAN NODOS A CADA CIUDAD ----------------
  cont_ciudades = 0
  listaUnidadesMilitares = Lista()
  for ciudades in root.iter("listaCiudades"):
    pass
    for ciudad in ciudades:
      cont2 = 0
      listaUnidadesMilitares = Lista()
      for unidaMilitar in ciudad.iter("unidadMilitar"):
          filaUnidadMilitar = unidaMilitar.attrib["fila"]
          columnaUnidadmilitar = unidaMilitar.attrib["columna"]
          capacidad = unidaMilitar.text
          listaUnidadesMilitares.append(UnidadesMilitar(int(columnaUnidadmilitar), int(filaUnidadMilitar), int(capacidad)))

      for fila in ciudad.iter("fila"):
        columnas = fila.text.replace('\n', "").replace('"', "")
        noFila = fila.attrib["numero"]

        listaNodo = Lista()

        cont = 1
       
        for nodo in columnas:    
         FilaMilitar = listaUnidadesMilitares[cont2].y
         ColumMilitar = listaUnidadesMilitares[cont2].x
         capa = listaUnidadesMilitares[cont2].valor
         if int(noFila) == FilaMilitar and cont == ColumMilitar:   
            listaNodo.append(Nodo(Casilla("Unidad Militar",capa)))
            cont +=1
            cont2 +=1
            if cont2 > listaUnidadesMilitares.length() - 1: 
              cont2 -=1
         
         else:
           if nodo == "*":
            listaNodo.append(Nodo(Casilla("Intransitable",0)))
            cont +=1
           if nodo == " ":
            listaNodo.append(Nodo(Casilla("Transitable",0)))   
            cont +=1
           if nodo == "E":
            listaNodo.append(Nodo(Casilla("Entrada",0)))   
            cont +=1
           if nodo == "C":
            listaNodo.append(Nodo(Casilla("Civil",0)))   
            cont +=1
           if nodo == "R":
            listaNodo.append(Nodo(Casilla("Recurso",0)))   
            cont +=1
        
        Lista_ciudades[cont_ciudades].append(listaNodo)
        
      cont_ciudades +=1 
#----------------------- SE AGREGAN ROBOTS A LA LISTA DE ROBOTS ----------------
  for robots in root.iter("robots"):
    pass
    for robot in robots.iter("nombre"):
      nombre = robot.text
      tipo = robot.attrib["tipo"]
      if tipo == "ChapinFighter":
        capacidad = robot.attrib["capacidad"]
      else:
        capacidad = "0"
      Lista_robots.append(Robot(nombre,tipo,int(capacidad)))
  
          
def Buscar_archivo():  # FUNCION QUE REALIZAR LA SELECCION DEL ARCHIVO A CARGAR 
  
    Tk().withdraw()
    archivo = filedialog.askopenfile(
        title="Seleccionar un archivo",
        initialdir="./",
        filetypes=(
            ("Archivos xml", "*.xml"),
        )
    )
    if archivo is None:
        print('No se seleccionó ningun archivo\n')
        return None
    else:
        return archivo
  


def cargarPisos():#METODO PARA SELCCION DEL ARCHIVO
    archivo = Buscar_archivo()
    cofiguracion(archivo)
    

if __name__ == '__main__':
 global Lista_ciudades, Lista_robots
 Lista_ciudades = Lista()
 Lista_robots = Lista()

 
 print("--------- BIENVENIDO ---------")
 menuprincipal = input(
  "\n       Chapin Warrios S.A. \n\n------- MENU PRINCIPAL-------- \n 1- Cargar archivo de configuración  \n 2- Ejecutar misiones \n 3- Salir \nPOR FAVOR ELIJA UNA OPCION: ")
 while menuprincipal != "4":
 
  if menuprincipal == "1":
   cargarPisos()

  elif menuprincipal == "2":
   pass

  elif menuprincipal == "3":
    pass

  else:
    print("Opcion ingresa invalida!")

  menuprincipal = input(
  "\n--------------------------------\n       Chapin Warrios S.A. \n\n------- MENU PRINCIPAL-------- \n 1- Cargar archivo de configuración  \n 2- Ejecutar misiones \n 3- Salir \nPOR FAVOR ELIJA UNA OPCION: ")