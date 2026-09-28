import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime # Necesario para procesar la fecha correctamente
import abmtareasvista as vista
import abmtareasmodelo as modelo

def iniciar_abmtareas(parent, conexion, modo, datos_edicion=None):
    # 1. Obtener lista de mecánicos desde la base de datos
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM mecanicos ORDER BY nombre")
        lista_m = [f[0] for f in cursor.fetchall()]
        cursor.close()
    except:
        # Lista de respaldo si falla la conexión
        lista_m = ["Zucarpriel", "Freire Cristian", "Subelza Julio"]

    # 2. Crear la ventana base
    ventana = vista.crear_ventana(parent)
    
    # Definir el título de estado
    if modo == "AGREGAR":
        estado = "Nueva Tarea"
    else:
        id_t = datos_edicion.get('id_tarea', '---')
        estado = f"Editando Tarea {id_t}"

    # 3. Definir comando para guardar
    def guardar():
        try:
            # Capturamos los datos del formulario
            dict_datos = {
                # Guardamos en formato dd-mm-yyyy para mantener consistencia con tu DB
                "fecha": entradas["fecha"].get_date().strftime("%d-%m-%Y"),
                "reporte": entradas["reporte"].get("1.0", "end-1c"), 
                "mecanicos": entradas["mecanicos"].get(),
                "horarios": entradas["horarios"].get()
            }
            
            if modo == "AGREGAR":
                modelo.insertar_tarea(conexion, dict_datos)
            else:
                modelo.actualizar_tarea(conexion, datos_edicion["id_tarea"], dict_datos)
            
            messagebox.showinfo("Éxito", "Registro guardado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    # 4. Construcción de la Interfaz
    vista.crear_toolstrip(ventana, estado, guardar, ventana.destroy)
    entradas = vista.crear_formulario(ventana, lista_m)

    # 5. Carga de datos iniciales / Edición
    if modo == "AGREGAR":
        # Cargar el próximo ID sugerido
        entradas["id_tarea"].config(state="normal")
        entradas["id_tarea"].insert(0, modelo.obtener_proximo_id(conexion))
        entradas["id_tarea"].config(state="readonly")
    else:
        # Carga de datos para MODIFICAR
        for campo, valor in datos_edicion.items():
            if campo in entradas:
                w = entradas[campo]
                
                # CASO ESPECIAL: Fecha (Widget DateEntry)
                if campo == "fecha":
                    try:
                        # Convertimos el texto dd-mm-yyyy a objeto fecha para el widget
                        fecha_obj = datetime.strptime(str(valor), "%d-%m-%Y")
                        w.set_date(fecha_obj)
                    except:
                        pass # Si falla el formato, queda la fecha de hoy por defecto
                
                # CASO ESPECIAL: Reporte (Widget Text)
                elif isinstance(w, tk.Text): 
                    w.delete("1.0", tk.END)
                    w.insert("1.0", str(valor))
                
                # CASO GENERAL: Entrys y Combobox
                elif hasattr(w, "insert"):
                    # Si el widget estaba readonly (como el ID), lo habilitamos para insertar
                    estado_original = w.cget("state")
                    w.config(state="normal")
                    w.delete(0, tk.END)
                    w.insert(0, str(valor))
                    w.config(state=estado_original)
    
    return True