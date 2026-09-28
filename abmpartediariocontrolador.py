import tkinter as tk
from tkinter import messagebox
import abmpartediariovista as vista
from abmpartediariomodelo import (
    insertar_partediario,
    actualizar_partediario,
    obtener_proximo_id
)


def iniciar_abmpartediario(parent, conexion, estado="AGREGAR", datos_pd=None):

    # ------------------------------
    # GUARDAR
    # ------------------------------
    def guardar():
        try:
            datos = {}

            for campo, widget in campos.items():
                # ID  solo informativo
                if campo == "ID":
                    continue

                if isinstance(widget, tk.Text):
                    valor = widget.get("1.0", "end").strip()
                else:
                    valor = widget.get().strip()

                datos[campo] = valor

            if estado == "AGREGAR":
                insertar_partediario(conexion, datos)
                mensaje = "Parte diario agregado correctamente."
            else:
                actualizar_partediario(conexion, datos_pd["ID"], datos)
                mensaje = "Parte diario modificado correctamente."

            messagebox.showinfo("Éxito", mensaje, parent=ventana)
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    # ------------------------------
    # VENTANA
    # ------------------------------
    ventana = vista.crear_ventana(parent)

    vista.crear_toolstrip(
        ventana=ventana,
        estado_texto="Agregando" if estado == "AGREGAR" else "Modificando",
        comando_guardar=guardar,
        comando_cancelar=ventana.destroy
    )

    campos = vista.crear_formulario(ventana)

    # ------------------------------
    # AGREGAR → ID INFORMATIVO
    # ------------------------------
    if estado == "AGREGAR":
        proximo_id = obtener_proximo_id(conexion)

        if "ID" in campos:
            campos["ID"].insert(0, str(proximo_id))
            campos["ID"].config(state="readonly")

    # ------------------------------
    # MODIFICAR → CARGAR DATOS
    # ------------------------------
    if estado == "MODIFICAR" and datos_pd:
        for campo, valor in datos_pd.items():
            if campo not in campos:
                continue

            widget = campos[campo]
            widget.configure(state="normal")

            if isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
                widget.insert("1.0", valor)
            else:
                widget.delete(0, "end")
                widget.insert(0, valor)

        # ID bloqueado
        if "ID" in campos:
            campos["ID"].config(state="disabled")

 
    return ventana
