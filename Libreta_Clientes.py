# App para registro de clientes | App Client Manager
# - Agregar nuevos clientes     | - Add new clients
# - Actualizar Clientes         | - Update clients
# - Eliminar clientes           | - Delete clients


from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title('Gestor de Clientes')


# ------- Base de Datos ------- BBDD -------
conn = sqlite3.connect('crm.db') # creación de archivo BBDD | file BBDD creation
c = conn.cursor()

c.execute("""
  CREATE TABLE if not exists cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    empresa TEXT NOT NULL
  );
 """)


# -------- Funciones -------- Functions ---------

# Actualiza la vista mostrando los registros | Update of view, render registers
def render():
  rows = c.execute('SELECT * FROM cliente').fetchall()
  tree.delete(*tree.get_children()) # borra todo el tree anterior
    # sin esta línea arrojará el error de que el id 1 ya existe
  for row in rows: # actualiza el tree
    tree.insert('', END, row[0], values= (row[1], row[2], row[3]))
    # atributos de insert
      # '' - el padre se refiere a la tabla misma
      # END - donde queremos agregar el registro, al final
      # row[0] - índice que agregaremos, el de la primera columna
      # values - valores que queremos insertar, row representa a las columnas


# Agregar Nuevos clientes ------- Add a new client -------
def insert_client(client):
  c.execute("""
    INSERT INTO cliente (nombre,telefono,empresa) VALUES (?,?,?)""",
    (client['nombre'], client['telefono'], client['empresa']))
  conn.commit()
  render()
  

def nuevo_cliente():
  def guardar_cliente():  # obtirne los datos del cliente de los entrys
    if not e_nombre.get():  # si el entry está vacío muestra el mensaje
      messagebox.showerror('Error', 'Debe llenar todos los campos')
      return  # regresará a iniciar la función sin cerrar la ventana de los campos
    if not e_telefono.get():  
      messagebox.showerror('Error', 'Debe llenar todos los campos')
      return
    if not e_empresa.get():  
      messagebox.showerror('Error', 'Debe llenar todos los campos')
      return
    client = {
      'nombre' : e_nombre.get(),
      'telefono' : e_telefono.get(),
      'empresa' : e_empresa.get()
    }
    insert_client(client)
    top.destroy()



# Ventana Emergente de Nuevo Cliente -------------------------------------------------------------------
  top = Toplevel()
  top.title('Nuevo Cliente')
  top.iconbitmap('nuevo.ico')

  l_nombre = Label(top, text='nombre')
  l_nombre.grid(row=0, column=0)
  e_nombre = Entry(top, width=40)
  e_nombre.grid(row=0, column=1)

  l_telefono = Label(top, text='telefono')
  l_telefono.grid(row=1, column=0)
  e_telefono = Entry(top, width=40)
  e_telefono.grid(row=1, column=1)

  l_empresa = Label(top, text='empresa')
  l_empresa.grid(row=2, column='0')
  e_empresa = Entry(top, width=40)
  e_empresa.grid(row=2, column=1)

  guardar = Button(top, text='Guardar', command=guardar_cliente)
  guardar.grid(row=3, column=2)

  top.mainloop()

def eliminar_cliente():
  id = tree.selection()[0]  # permite seleccionar elementos dentro del tree, devuelve el ID
    # [0] indica que sólo queremos tomar el primer indice de la tupla  arrojada por selection()
    # esto permitirá eliminar un sólo elemento
  client = c.execute('SELECT * FROM cliente WHERE id=?', (id, )).fetchone()
  respuesta = messagebox.askokcancel('Eliminar Cliente','Desea aliminar al cliente?\n' + client[1])
  # cliente[1] - se refiere al dato de la columna 1 del registro (nombre)
  if respuesta:
    c.execute('DELETE FROM cliente WHERE id=?', (id, ))
    conn.commit()
    render()
  else:
    pass


# Interfaz Gráfica ----------------------------------------------------------------------
btnc = Button(root, text='Nuevo Cliente', command=nuevo_cliente)
btnc.grid(row=0, column=0)

btec = Button(root, text='Eliminar Cliente', command=eliminar_cliente)
btec.grid(row=0, column=1)

espacio = Label(root, text='')
espacio.grid(row=1, column=0, columnspan=3)

tree = ttk.Treeview(root)
tree['columns'] = ('nombre','telefono','empresa')
tree.column('#0', width=0, stretch=NO)
tree.column('nombre')
tree.column('telefono')
tree.column('empresa')

# cabecera de la tabla
tree.heading('nombre', text='nombre')
tree.heading('telefono', text='telefono')
tree.heading('empresa', text='empresa')
tree.grid(row=2, column=0, columnspan=2)


render()
root.mainloop()
