from tkinter import messagebox
import plantasmodelo as modelo
import plantasvista as vista
import abmplantas  # El puente

def iniciar_plantas(parent, conexion):
    # 1. Creamos la ventana primero
    ventana = vista.crear_ventana(parent)

    # 2. Definimos la lógica de refresco (necesaria para las acciones)
    def cargar_datos():
        tree.delete(*tree.get_children())
        for fila in modelo.obtener_plantas(conexion):
            tree.insert("", "end", values=fila)

    # 3. Funciones de Acción (definidas antes para pasarlas a la vista)
    def agregar():
        abmplantas.abrir_abmplantas(
            parent=ventana,
            conexion=conexion,
            estado="AGREGAR"
        )
        cargar_datos()

    def modificar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una planta", parent=ventana)
            return

        item = tree.item(seleccionado)["values"]
        datos_planta = {"id": item[0], "nombre": item[1]}
        
        abmplantas.abrir_abmplantas(
            parent=ventana,
            conexion=conexion,
            estado="MODIFICAR",
            datos_planta=datos_planta
        )
        cargar_datos()

    def eliminar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una planta para eliminar", parent=ventana)
            return

        planta_id = tree.item(seleccionado)["values"][0]
        nombre = tree.item(seleccionado)["values"][1]

        if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?", parent=ventana):
            try:
                modelo.eliminar_planta(conexion, planta_id)
                cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=ventana)

    # 4. Inicializar la interfaz pasando las funciones
    # Esto soluciona el TypeError porque plantasvista.crear_toolstrip ahora recibe los comandos
    vista.crear_toolstrip(ventana, agregar, modificar, eliminar)
    
    # 5. Creamos la tabla y cargamos los datos
    tree = vista.crear_tabla(ventana)
    cargar_datos()