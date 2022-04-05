import os
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
from PIL import ImageTk, Image

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
  Ciudades()
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

def graficarCiudad(ciudad):
  inicio ="""digraph structs {
    node [shape=none fontname=Helvetica];

     struct1 [label=<<TABLE border="2" CELLBORDER="1" CELLSPACING="2" bgcolor="white" color="black">
     <TR>
        <TD  BGCOLOR="white">     </TD>
        """

#------------------------- COLUMNAS IDENTIFIACION --------------------------------
  for i in range(ciudad.columna):
    inicio +="""<TD  BGCOLOR="white">  """+str(i+1)+""" </TD>
    """
  inicio +="""</TR>
  """
#---------------------------------------------------------------------------------

#--------------------------- INTEGRANDO FILAS Y COLUMNAS*------------------------
  for i in range(ciudad.fila):
    inicio +="""<TR>
        <TD  BGCOLOR="white">"""+str(i+1)+"""</TD>
    """
    for j in range(ciudad.columna):
      casilla = ciudad.obtener_elem(i,j).caracteristica
      if casilla == "Intransitable":
        inicio +="""<TD  BGCOLOR="black">   </TD>
        """

      if casilla == "Transitable":
        inicio +="""<TD  BGCOLOR="white">   </TD>
        """

      if casilla == "Entrada":
        inicio +="""<TD  BGCOLOR="green">   </TD>
        """

      if casilla == "Civil":
        inicio +="""<TD  BGCOLOR="#81FFE5">   </TD>
        """

      if casilla == "Recurso":
        inicio +="""<TD  BGCOLOR="grey57">   </TD>
        """
        
      if casilla == "Unidad Militar":
        inicio +="""<TD  BGCOLOR="#F1724">   </TD>
        """

    inicio +="""</TR>"""
  inicio +="""</TABLE>>];
       }
   """
#---------------------------------------------------------------------------------
  
  crearArchivo("CiudadGraphviz.dot",inicio)
  os.system('dot.exe -Tpng CiudadGraphviz.dot -o Ciudad.png')

def crearArchivo(ruta, contenido):
    archivo = open(ruta, 'w')
    archivo.write(contenido)
    archivo.close  
    
def Ciudades():
    for i in range(Lista_ciudades.length()):
        dimension =str(Lista_ciudades[i].fila)
        dimension +="X"
        dimension +=str(Lista_ciudades[i].columna)
        table1.insert("", END,text=str(Lista_ciudades[i].nombre),values=(dimension))

def get_data(): # METODO PARA GRAFICAR CIUDADADES EN GUI
  ciudad = table1.item(table1.selection())["text"]
  for i in range(Lista_ciudades.length()):
    nombre = Lista_ciudades[i].nombre
    if nombre == ciudad:
      graficarCiudad(Lista_ciudades[i])
      MostrarImagen("Ciudad.png")
  
def MostrarImagen(ruta):
  img = Image.open(ruta)
  new_img = img.resize((420,380))
  render = ImageTk.PhotoImage(new_img)
  img2 = Label(ventana, image=render)
  img2.image = render
  img2.place(x=290, y = 90)


if __name__ == '__main__':
 global Lista_ciudades, Lista_robots
 Lista_ciudades = Lista()
 Lista_robots = Lista()

 ventana = Tk()
 ventana.title("Chapin Warrios, S.A")
 btnCargar = Button(ventana, text="CARGAR CONFIGURACION", width=22,height=2, command=cargarPisos)
 btnCargar.config(fg="Black",bg="#FC7643",font=("Bahnschrift SemiBold",10))
 btnCargar.place(x= 10, y=10)

 label1 = Label(ventana,text="Chapin Warrios, S.A", width=17,height=1)
 label1.config(fg="#FFEBD2",bg="#273248", font=("Bahnschrift SemiBold",22))
 label1.place(x = 380,y = 13)

 img = Image.open("IMG\\CASILLAS.png")
 new_img = img.resize((225,150))
 render = ImageTk.PhotoImage(new_img)
 img1 = Label(ventana, image=render)
 img1.image = render
 img1.place(x=400, y = 485)

#------------------------ TABLA CON CIUDADES --------------------------------
 label1 = Label(ventana,text="Lista de ciudades", width=15,height=1)
 label1.config(fg="#FFEBD2",bg="#273248", font=("Bahnschrift SemiBold",15))
 label1.place(x = 30,y = 60)

 table1 = ttk.Treeview(ventana, columns=("Dimenesion") ,height=19)
 table1.column("#0", width=115)
 table1.column("Dimenesion", width=115, anchor=CENTER)
 table1.heading("#0",text="Nombre", anchor=CENTER)
 table1.heading("Dimenesion",text="Dimenesion", anchor=CENTER)
 table1.place(x=30,y=110)

 mostrar = Button(ventana, text="Mostrar Ciudad",width=15, height=2, command = get_data)
 mostrar.config(fg="Black",bg="#FC7643",font=("Bahnschrift SemiBold",10))
 mostrar.place(x= 80, y=530)
#------------------------------------------------------------------------------

 ventana.config( bg="#273248" )
 ventana.geometry('1050x650+200+40')
 ventana.mainloop()
