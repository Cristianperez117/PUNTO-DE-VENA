# -*- encoding: utf-8 -*-
# ------------------------------------------------------------------------#
# Programa: Punto de venta 2.0				                              #
# ------------------------------------------------------------------------#
# Propósito: Administracion para el inventario                            #
# ------------------------------------------------------------------------#
# Autor: Abuelazo                                                         #
# ------------------------------------------------------------------------#
# Fecha: 14/04/2016                                                       #
# ------------------------------------------------------------------------#

#se importan librerias necesarias
from traitlets import CUnicode, Unicode
import conexion
from PyQt5 import QtGui

##################################metodos para ingresar productos###############################################################################
#metodo para cotejar los campos
def campo_vacio(self):
    #se evalua si la longitud del campo producto es 0
    if len(self.ui.producto_nombre.text()) == 0:
        #mensaje falta producto
        QtGui.QMessageBox.warning(self, "Informacion", """Te falta producto""", QtGui.QMessageBox.Ok)
    # se evalua si la longitud del campo precio es 0
    elif len(self.ui.producto_descripcion.text()) == 0:
        # mensaje falta precio
        QtGui.QMessageBox.warning(self, "Informacion", """Te falta descripcion""", QtGui.QMessageBox.Ok)
    #se evalua si la longitud del campo precio es 0
    elif len(self.ui.producto_precio.text()) == 0:
        #mensaje falta precio
        QtGui.QMessageBox.warning(self, "Informacion", """Te falta precio""", QtGui.QMessageBox.Ok)
    # se evalua si la longitud del campo cantidad es 0
    elif len(self.ui.producto_cantidad.text()) == 0:
        #mensaje te falta cantidad
        QtGui.QMessageBox.warning(self, "Informacion", """Te falta cantidad""", QtGui.QMessageBox.Ok)
    else:
        #se llama al metodo ingresar_producto
        ingresar_producto(self)
#-----------------------------------------------------------------------------------------------------------------------------------------------
#metodo para ingresar_producto
def ingresar_producto(self):
    #se toman los valores de los campos
    producto = Unicode(self.ui.producto_nombre.text())
    descripcion = CUnicode(self.ui.producto_descripcion.text())
    precio = float(self.ui.producto_precio.text())
    cantidad = CUnicode(self.ui.producto_cantidad.text())

    #se crea un query para insertar los datos
    query = Unicode("INSERT INTO productos(producto, descripcion, precio, cantidad) VALUES(\"{0}\",\"{1}\",\"{2}\",\"{3}\")").format(producto, descripcion, precio, cantidad)
    #se ejecuta el query
    conexion.consultas(query)
    #se limpian los campos
    self.ui.producto_nombre.setText('')
    self.ui.producto_precio.setText('')
    self.ui.producto_cantidad.setText('')
    self.ui.producto_descripcion.setText('')
################################################################################################################################################


###############################metodos para actualizar productos################################################################################
#metodo para buscar productos
def buscar_producto(self):
    #query para buscar por nombre en caso de que no se escriba nada en el campo se muestran todos los datos
    query = Unicode("SELECT * FROM productos WHERE producto LIKE \"%{0}%\"").format(Unicode(self.ui.actualizar_producto.text()))
    #se ejecuta el query y se almacena en una valriable
    datos_obtenidos = conexion.consultas(query)
    if len(datos_obtenidos) == 0:
        query = Unicode("SELECT * FROM productos WHERE descripcion LIKE \"%{0}%\"").format(Unicode(self.ui.actualizar_producto.text()))
        datos_obtenidos = conexion.consultas(query)
    else:
        pass
    #se toma la longitud de la consulta realizada y se asigna a una variable global para usarla en otros metodos
    self.datos = len(datos_obtenidos)
    #se asignan el numero de columnas para la tabla
    self.ui.actualizar_lista.setColumnCount(5)
    #se asignan el numero de filas para la tabla dado la longitud de la consulta
    self.ui.actualizar_lista.setRowCount(len(datos_obtenidos))
    #bucle para llenar la tabla por fila
    for fila in range(datos_obtenidos):
        #bucle para llenar la tabla por columna
        for columna in range(5):
            #se crea un item
            item = QtGui.QTableWidgetItem()
            #se le asigna el valor a enviar
            item.setText("%s" %(Unicode(datos_obtenidos[fila][columna])))
            #se envia el valor a la tabla por posición fila columna
            self.ui.actualizar_lista.setItem(fila, columna, item)

#-----------------------------------------------------------------------------------------------------------------------------------------------
#metodo para modificar productos
def alterar_producto(self):
    #se crea lista vacia
    datos_obtenidos = []
    #bucle para actualizar los datos de la tabla por fila
    for fila in range(self.datos):
        #bucle para actualizar datos de la tabla por columna
        for columna in range(5):
                #se toma el valor por posición
                dato = Unicode(self.ui.actualizar_lista.item(fila, columna).text())
                #se agrega dato a la lista
                datos_obtenidos.append(dato)
        #se crea query para actualizar productos
        query = Unicode("UPDATE productos SET producto = \"{1}\", descripcion = \"{2}\", precio = \"{3}\", cantidad = \"{4}\" WHERE id = \"{0}\" ").format(*datos_obtenidos)
        #se ejecuta la consulta
        conexion.consultas(query)
        #se limpia la lista
        datos_obtenidos = []

    self.ui.actualizar_actualizar.setEnabled(False)
    self.ui.modificar_lista.clearContents()
    self.ui.modificar_lista.setRowCount(0)
    buscar_producto(self)
#-----------------------------------------------------------------------------------------------------------------------------------------------

##########################metodos para eliminar productos#######################################################################################
#metodo para mostrar productos a eliminar
def eliminar_mostrar(self):
    #se crea un query para seleccionar productos tomando el valor de un qlabel
    query = Unicode("SELECT * FROM productos WHERE producto LIKE \"%{0}%\"").format(Unicode(self.ui.eliminar_producto.text()))
    #se ejecuta la consulta y se almacena en una variable
    datos_obtenidos = conexion.consultas(query)
    if len(datos_obtenidos) == 0:
        query = Unicode("SELECT * FROM productos WHERE descripcion LIKE \"%{0}%\"").format(Unicode(self.ui.eliminar_producto.text()))
        datos_obtenidos = conexion.consultas(query)
    else:
        pass
    #se asignan las columnas para la tabla
    self.ui.eliminar_lista_2.setColumnCount(5)
    #se asignan las filas dad la longitud de la consulta
    self.ui.eliminar_lista_2.setRowCount(len(datos_obtenidos))
    #bucle para llenar tabla por fila
    for fila in range(len(datos_obtenidos)):
        #bucle para llenar tabla por columna
        for columna in range(5):
            #se cre un tem
            dato = QtGui.QTableWidgetItem()
            #se asigna el valor al item
            dato.setText("%s" % (Unicode(datos_obtenidos[fila][columna])))
            #se manda el valor por posición fila columna
            self.ui.eliminar_lista_2.setItem(fila, columna, dato)
#----------------------------------------------------------------------------------------------------------------------------------------------
# metodo para eliminar productos
def eliminar_producto(self):
    #se toma el valor de un qlabel
    id = Unicode(self.ui.eliminar_id_2.text())
    #se crea un query para eliminar productos
    query = Unicode("DELETE FROM productos WHERE id = \"{0}\" ").format(id)
    #se ejecuta el query
    conexion.consultas(query)
    eliminar_mostrar(self)
    self.ui.eliminar_id_2.setText("")
#-----------------------------------------------------------------------------------------------------------------------------------------------