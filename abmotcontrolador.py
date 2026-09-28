from tkinter import messagebox
from datetime import date
import tkinter as tk
from tkinter import ttk
import abmotvista as vista

from abmotmodelo import (
    insertar_ot,
    actualizar_ot,
    obtener_sectores_por_planta,
    obtener_mecanicos,
    obtener_proximo_id
)

def iniciar_abmot(parent, conexion, estado="AGREGAR", datos_ot=None):

    # =============================
    # CAMPOS POST SOLUCIÓN
    # =============================
    CAMPOS_POST = [
        "Solucion",
        "Fecha cierre ot",
        "Descripcion solucion",
        "Material utilizado",
        "NombreRealizo",
        "Aprobo solicitante",
        "Aprobo mant",
        "Aprobo calidad"
    ]

    # =============================
    # GUARDAR
    # =============================
    def guardar():
        try:
            datos = {}
            for campo, widget in campos.items():
                if campo == "ID":
                    continue

                if widget.__class__.__name__ == "Text":
                    valor = widget.get("1.0", "end").strip()
                else:
                    valor = widget.get().strip()

                datos[campo] = valor

            # Limpiar campos POST si no está realizada
            if datos.get("Realizada", "").upper() != "SI":
                for campo in CAMPOS_POST:
                    datos[campo] = ""

            if estado == "AGREGAR":
                insertar_ot(conexion, datos)
                mensaje = "Orden de trabajo agregada correctamente."
            else:
                # Usamos el ID que viene en datos_ot
                actualizar_ot(conexion, datos_ot["ID"], datos)
                mensaje = "Orden de trabajo modificada correctamente."

            messagebox.showinfo("Éxito", mensaje, parent=ventana)
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    # =============================
    # CAMBIO REALIZADA (Para interacción del usuario)
    # =============================
    def cambio_realizada(event=None):
        valor = campos["Realizada"].get().upper()
        if valor == "SI":
            vista.habilitar_campos(campos, CAMPOS_POST)
            if not campos["Fecha cierre ot"].get():
                campos["Fecha cierre ot"].set_date(date.today())
        else:
            vista.limpiar_campos(campos, CAMPOS_POST)
            vista.deshabilitar_campos(campos, CAMPOS_POST)

    # =============================
    # CARGAR SECTORES
    # =============================
    def cargar_sectores(event=None):
        planta = campos["Planta"].get()
        sectores = obtener_sectores_por_planta(conexion, planta)
        campos["Sector"]["values"] = sectores
        if sectores and estado == "AGREGAR": # Solo forzar el primero si es nueva OT
            campos["Sector"].current(0)

    # =============================
    # INICIALIZACIÓN DE VISTA
    # =============================
    ventana = vista.crear_ventana(parent)

    vista.crear_toolstrip(
        ventana=ventana,
        estado_texto="Agregando" if estado == "AGREGAR" else "Modificando",
        comando_guardar=guardar,
        comando_cancelar=ventana.destroy
    )

    campos = vista.crear_formulario(ventana)

    # Configuración de Combos
    campos["Planta"]["state"] = "readonly"
    campos["Planta"]["values"] = ["Chocolate", "Golosinas"]
    campos["Planta"].bind("<<ComboboxSelected>>", cargar_sectores)

    campos["Sector"]["state"] = "readonly"

    mecanicos_lista = obtener_mecanicos(conexion)
    campos["NombreRealizo"]["values"] = mecanicos_lista

    campos["Realizada"]["values"] = ["NO", "SI"]
    campos["Realizada"].bind("<<ComboboxSelected>>", cambio_realizada)

    # =============================
    # LÓGICA AGREGAR
    # =============================
    if estado == "AGREGAR":
        proximo_id = obtener_proximo_id(conexion)
        campos["ID"].insert(0, str(proximo_id))
        campos["ID"].config(state="disabled")
        campos["Planta"].current(0)
        cargar_sectores()
        campos["Realizada"].set("NO")
        cambio_realizada()

    # ===========================================================
    # LÓGICA MODIFICAR (SÚPER CORREGIDA)
    # ===========================================================
    elif estado == "MODIFICAR" and datos_ot:
        # 1. Cargar planta y sectores primero
        planta_db = datos_ot.get("Planta", "")
        campos["Planta"].set(planta_db)
        cargar_sectores()

        # 2. Volcar datos de la DB al formulario de forma flexible
        for campo_db, valor in datos_ot.items():
            # Buscamos el widget ignorando mayúsculas/minúsculas
            widget = None
            for nombre_widget in campos.keys():
                if nombre_widget.lower() == campo_db.lower():
                    widget = campos[nombre_widget]
                    break
            
            if not widget:
                continue

            # Habilitar momentáneamente para insertar
            widget.configure(state="normal")

            # Tratamiento según tipo de widget
            if widget.__class__.__name__ == "Text":
                widget.delete("1.0", "end")
                widget.insert("1.0", str(valor) if valor else "")
            
            elif isinstance(widget, ttk.Combobox):
                val_str = str(valor) if valor else ""
                # Si el valor de la DB no está en la lista actual del combo, lo agregamos
                opciones = list(widget["values"])
                if val_str and val_str not in opciones:
                    opciones.append(val_str)
                    widget["values"] = opciones
                widget.set(val_str)
            
            elif hasattr(widget, 'set_date'): # Para DateEntry
                if valor:
                    try: widget.set_date(valor)
                    except: pass
            
            else: # Entry común
                try:
                    widget.delete(0, "end")
                    widget.insert(0, str(valor) if valor else "")
                except:
                    try: widget.set(str(valor) if valor else "")
                    except: pass

        # 3. Bloqueos finales
        if "ID" in campos:
            campos["ID"].config(state="disabled")

        # 4. Ajustar visibilidad final según la base de datos
        # No usamos cambio_realizada() para evitar que el 'limpiar_campos' borre la carga
        realizada_db = str(datos_ot.get("Realizada", "")).upper()
        if realizada_db == "SI":
            vista.habilitar_campos(campos, CAMPOS_POST)
        else:
            vista.deshabilitar_campos(campos, CAMPOS_POST)

    # Esperar a que se cierre para retornar el control
    parent.wait_window(ventana)
    return ventana