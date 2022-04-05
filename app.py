import os
from pickle import GLOBAL
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from xml.etree import ElementTree
from Lista import Lista
from Nodo import Nodo
from Ciudad import Ciudad
from Casilla import Casilla  # VALOR DE LA MATRIZ Y CARACTERISTICA
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
  for item in table1.get_children():
        table1.delete(item)

#----------------------- SE AGREGAN CIUDAD A LISTA DE CIUDADES ----------------
  for ciudades in root.iter("listaCiudades"):
    pass
    for ciudad in ciudades:
      pass
      for nombre in ciudad.iter("nombre"):
        name = nombre.text
        Nofilas = nombre.attrib["filas"]
        Nocolumnas = nombre.attrib["columnas"]

        if Lista_ciudades.length() > 0:
          for i in range(Lista_ciudades.length()):
            ciudadName = Lista_ciudades[i].nombre
            if name == ciudadName:
              Lista_ciudades.reset(i)
              break
        


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
      
      if Lista_robots.length() > 0:
          for i in range(Lista_robots.length()):
            robotdName = Lista_robots[i].nombre
            if nombre == robotdName:
              Lista_robots.reset(i)
              break
        

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


def cargarPisos():  # METODO PARA SELCCION DEL ARCHIVO
    archivo = Buscar_archivo()
    cofiguracion(archivo)


def graficarCiudad(ciudad):
    inicio = """digraph structs {
    node [shape=none fontname=Helvetica];

     struct1 [label=<<TABLE border="2" CELLBORDER="1" CELLSPACING="2" bgcolor="white" color="black">
     <TR>
        <TD  BGCOLOR="white">     </TD>
        """

# ------------------------- COLUMNAS IDENTIFIACION --------------------------------
    for i in range(ciudad.columna):
        inicio += """<TD  BGCOLOR="white">  """+str(i+1)+""" </TD>
    """
    inicio += """</TR>
  """
# ---------------------------------------------------------------------------------

# --------------------------- INTEGRANDO FILAS Y COLUMNAS*------------------------
    for i in range(ciudad.fila):
        inicio += """<TR>
        <TD  BGCOLOR="white">"""+str(i+1)+"""</TD>
    """
        for j in range(ciudad.columna):
            casilla = ciudad.obtener_elem(i, j).caracteristica
            if casilla == "Intransitable":
                inicio += """<TD  BGCOLOR="black">   </TD>
        """

            if casilla == "Transitable":
                inicio += """<TD  BGCOLOR="white">   </TD>
        """

            if casilla == "Entrada":
                inicio += """<TD  BGCOLOR="green">   </TD>
        """

            if casilla == "Civil":
                inicio += """<TD  BGCOLOR="#81FFE5">   </TD>
        """

            if casilla == "Recurso":
                inicio += """<TD  BGCOLOR="grey57">   </TD>
        """

            if casilla == "Unidad Militar":
                inicio += """<TD  BGCOLOR="#F1724">   </TD>
        """

        inicio += """</TR>"""
    inicio += """</TABLE>>];
       }
   """
# ---------------------------------------------------------------------------------

    crearArchivo("CiudadGraphviz.dot", inicio)
    os.system('dot.exe -Tpng CiudadGraphviz.dot -o Ciudad.png')


def crearArchivo(ruta, contenido):
    archivo = open(ruta, 'w')
    archivo.write(contenido)
    archivo.close


def Ciudades():
    for i in range(Lista_ciudades.length()):
        dimension = str(Lista_ciudades[i].fila)
        dimension += "X"
        dimension += str(Lista_ciudades[i].columna)
        table1.insert("", END, text=str(
            Lista_ciudades[i].nombre), values=(dimension))


def Robots():
    for item in table2.get_children():
        table2.delete(item)
    tipoMison = comboMision.get()
    for i in range(Lista_robots.length()):
        tipo = str(Lista_robots[i].tipo)
        capacidad = str(Lista_robots[i].capacidad)
        if tipoMison == "Rescate" and tipo == "ChapinRescue":
            table2.insert("", END, text=str(
                Lista_robots[i].nombre), values=(tipo, capacidad))

        if tipoMison == "Extraccion Recurso" and tipo == "ChapinFighter":
            table2.insert("", END, text=str(
                Lista_robots[i].nombre), values=(tipo, capacidad))


def get_data():  # METODO PARA GRAFICAR CIUDADADES EN GUI
    ciudad = table1.item(table1.selection())["text"]
    entradas = []
    for i in range(Lista_ciudades.length()):
        nombre = Lista_ciudades[i].nombre
        if nombre == ciudad:
            graficarCiudad(Lista_ciudades[i])
            MostrarImagen("Ciudad.png")
            for j in range(Lista_ciudades[i].entradas.length()):
                cordenada = "Fila: " + str(Lista_ciudades[i].entradas[j].y)
                cordenada += " Columna: " + \
                    str(Lista_ciudades[i].entradas[j].x)
                entradas.append(cordenada)
            comboEntradas["values"] = entradas


def change_civiles():
    mision = comboMision.get()
    ciudad = table1.item(table1.selection())["text"]
    unidades = []
    for i in range(Lista_ciudades.length()):
        nombre = Lista_ciudades[i].nombre
        if nombre == ciudad and mision == "Rescate":
            for j in range(Lista_ciudades[i].unidadCiviles.length()):
                cordenada = "Fila: " + \
                    str(Lista_ciudades[i].unidadCiviles[j].y)
                cordenada += " Columna: " + \
                    str(Lista_ciudades[i].unidadCiviles[j].x)
                unidades.append(cordenada)
            comboCiviles["values"] = unidades
        if mision == "Extraccion Recurso":
            comboCiviles["values"] = ["---"]


def change_recurso():
    mision = comboMision.get()
    ciudad = table1.item(table1.selection())["text"]
    recurso = []
    for i in range(Lista_ciudades.length()):
        nombre = Lista_ciudades[i].nombre
        if nombre == ciudad and mision == "Extraccion Recurso":
            for j in range(Lista_ciudades[i].recursos.length()):
                cordenada = "Fila: " + str(Lista_ciudades[i].recursos[j].y)
                cordenada += " Columna: " + \
                    str(Lista_ciudades[i].recursos[j].x)
                recurso.append(cordenada)
            comboRecursos["values"] = recurso


def MostrarImagen(ruta):  # METODO PARA GRAFICAR CIUDADADES EN GUI
    img = Image.open(ruta)
    new_img = img.resize((420, 380))
    render = ImageTk.PhotoImage(new_img)
    img2 = Label(ventana, image=render)
    img2.image = render
    img2.place(x=290, y=90)


if __name__ == '__main__':
    global Lista_ciudades, Lista_robots
    Lista_ciudades = Lista()
    Lista_robots = Lista()

    ventana = Tk()
    ventana.title("Chapin Warrios, S.A")
    btnCargar = Button(ventana, text="CARGAR CONFIGURACION",
                       width=22, height=2, command=cargarPisos)
    btnCargar.config(fg="Black", bg="#FC7643",
                     font=("Bahnschrift SemiBold", 10))
    btnCargar.place(x=10, y=10)

    img2 = Image.open("IMG\\robot.png")
    new_img1 = img2.resize((85, 75))
    render1 = ImageTk.PhotoImage(new_img1)
    img3 = Label(ventana, image=render1)
    img3.config(bg="#273248")
    img3.image = render1
    img3.place(x=610, y=0)

    label1 = Label(ventana, text="Chapin Warrios, S.A", width=17, height=1)
    label1.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 24))
    label1.place(x=320, y=13)

    img = Image.open("IMG\\CASILLAS.png")
    new_img = img.resize((150, 150))
    render = ImageTk.PhotoImage(new_img)
    img1 = Label(ventana, image=render)
    img1.image = render
    img1.place(x=420, y=485)

# ------------------------ TABLA CON CIUDADES --------------------------------
    label1 = Label(ventana, text="Lista de ciudades", width=15, height=1)
    label1.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 17))
    label1.place(x=50, y=62)

    table1 = ttk.Treeview(ventana, columns=("Dimenesion"), height=19)
    table1.column("#0", width=115)
    table1.column("Dimenesion", width=115, anchor=CENTER)
    table1.heading("#0", text="Nombre", anchor=CENTER)
    table1.heading("Dimenesion", text="Dimenesion", anchor=CENTER)
    table1.place(x=30, y=110)

    label7 = Label(ventana, text="MAPA", width=15, height=1)
    label7.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 14))
    label7.place(x=420, y=62)

    mostrar = Button(ventana, text="Mostrar Ciudad",
                     width=22, height=2, command=get_data)
    mostrar.config(fg="Black", bg="#FC7643", font=("Bahnschrift SemiBold", 12))
    mostrar.place(x=40, y=542)

# ------------------------------OPCIONES PARA MISIONES -----------------------------
    label2 = Label(ventana, text="Tipo de Mision", width=15, height=1)
    label2.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 11))
    label2.place(x=730, y=62)
    comboMision = ttk.Combobox(ventana, height=1, width=19, values=[
                               '---', 'Rescate', 'Extraccion Recurso'], state="readonly", postcommand=Robots)
    comboMision.current(0)
    comboMision.place(x=740, y=90)

    label3 = Label(ventana, text="Punto de entrada", width=15, height=1)
    label3.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 11))
    label3.place(x=900, y=62)
    comboEntradas = ttk.Combobox(ventana, height=1, width=19, values=[
                                 '---'], state="readonly")
    comboEntradas.current(0)
    comboEntradas.place(x=900, y=90)

    label4 = Label(ventana, text="Punto Civil", width=15, height=1)
    label4.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 11))
    label4.place(x=730, y=120)
    comboCiviles = ttk.Combobox(ventana, height=1, width=19, values=[
                                '---'], state="readonly", postcommand=change_civiles)
    comboCiviles.current(0)
    comboCiviles.place(x=740, y=150)

    label5 = Label(ventana, text="Punto de Recurso", width=15, height=1)
    label5.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 11))
    label5.place(x=900, y=120)
    comboRecursos = ttk.Combobox(ventana, height=1, width=19, values=[
                                 '---'], state="readonly", postcommand=change_recurso)
    comboRecursos.current(0)
    comboRecursos.place(x=900, y=150)

# ---------------------------------- OPCIONES DE LISTA DE ROBOTS  ---------------------------------

    label6 = Label(ventana, text="Lista de Robots", width=15, height=1)
    label6.config(fg="#FFEBD2", bg="#273248",
                  font=("Bahnschrift SemiBold", 17))
    label6.place(x=780, y=180)

    table2 = ttk.Treeview(ventana, columns=("Tipo", "Capacidad"), height=14)
    table2.column("#0", width=110)
    table2.column("Tipo", width=105, anchor=CENTER)
    table2.column("Capacidad", width=75, anchor=CENTER)
    table2.heading("#0", text="NOMBRE", anchor=CENTER)
    table2.heading("Tipo", text="TIPO", anchor=CENTER)
    table2.heading("Capacidad", text="Capacidad", anchor=CENTER)
    table2.place(x=740, y=220)

    btnMision = Button(ventana, text="Mostrar Recorrido", width=22, height=2)
    btnMision.config(fg="Black", bg="#FC7643",
                     font=("Bahnschrift SemiBold", 12))
    btnMision.place(x=790, y=560)

    ventana.config(bg="#273248")
    ventana.geometry('1050x650+200+40')
    ventana.mainloop()

