from tkinter import messagebox
import abmplantasvista as vista
import abmplantasmodelo as modelo

def iniciar_abm_planta(parent, conexion, estado="AGREGAR", datos_planta=None):
    
    titulo = "Nueva Planta" if estado == "AGREGAR" else "Modificar Planta"
    ventana = vista.crear_ventana(parent, titulo)
    
    botones = vista.crear_toolstrip(ventana)
    campos = vista.crear_formulario(ventana)

    # Si es MODIFICAR, cargamos el nombre actual
    if estado == "MODIFICAR" and datos_planta:
        campos["nombre"].insert(0, datos_planta["nombre"])

    def guardar():
        try:
            nombre = campos["nombre"].get().strip()
            if not nombre:
                messagebox.showwarning("Atención", "El nombre es obligatorio", parent=ventana)
                return

            datos = {"nombre": nombre}

            if estado == "AGREGAR":
                modelo.insertar_planta(conexion, datos)
            else:
                modelo.actualizar_planta(conexion, datos_planta["id"], datos)

            messagebox.showinfo("Éxito", "Planta guardada correctamente", parent=ventana)
            ventana.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=ventana)

    botones["guardar"].config(command=guardar)
    botones["cancelar"].config(command=ventana.destroy)

    # IMPORTANTE: Espera a que se cierre para que el listado se refresque
    parent.wait_window(ventana)