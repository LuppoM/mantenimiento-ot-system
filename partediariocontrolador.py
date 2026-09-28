from abmpartediariocontrolador import iniciar_abmpartediario
from tkinter import messagebox, simpledialog
from partediariomodelo import ParteDiarioModelo
from partediariovista import (
    crear_ventana,
    crear_toolstrip,
    crear_filtro,
    crear_tabla
)

CLAVE_ELIMINAR_PD = "Mario456"


class ParteDiarioControlador:
    def __init__(self, parent, conexion):
        self.parent = parent
        self.modelo = ParteDiarioModelo(conexion)
        self.ventana = crear_ventana(parent)

        # =====================================================
        # TOOLSTRIP
        # =====================================================
        crear_toolstrip(
            self.ventana,
            abrir_agregar=self.agregar,
            abrir_modificar=self.modificar,
            abrir_eliminar=self.eliminar
        )

        # =====================================================
        # FILTRO
        # =====================================================
        self.combo, self.entry = crear_filtro(
            self.ventana,
            self.aplicar_filtro
        )

        # =====================================================
        # TABLA
        # =====================================================
        self.tree = crear_tabla(self.ventana)

        # =====================================================
        # CARGA INICIAL
        # =====================================================
        self.cargar()

    # =====================================================
    # CARGAR
    # =====================================================
    def cargar(self, filas=None):
        self.tree.delete(*self.tree.get_children())

        datos = filas if filas is not None else self.modelo.obtener_todos()

        for d in datos:
            self.tree.insert(
                "",
                "end",
                iid=d["id"],
                values=(
                    d["id"],  # ID visible
                    d["fecha"].strftime("%d/%m/%Y"),
                    d["nombre"],
                    d["turno"],
                    d["codigo"],
                    d["reporte"]
                )
            )

    # =====================================================
    # FILTRAR
    # =====================================================
    def aplicar_filtro(self, campo, valor):
        filas = self.modelo.filtrar(campo, valor)
        self.cargar(filas)

    # =====================================================
    # AGREGAR
    # =====================================================
    def agregar(self):
        guardado = iniciar_abmpartediario(
            parent=self.ventana,
            conexion=self.modelo.conexion,
            estado="AGREGAR"
        )
        if guardado:
            self.cargar()

    # =====================================================
    # MODIFICAR
    # =====================================================
    def modificar(self):
        seleccionado = self.tree.focus()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccione un parte diario para modificar",
                parent=self.ventana
            )
            return

        datos_pd = self.modelo.obtener_por_id(seleccionado)

        guardado = iniciar_abmpartediario(
            parent=self.ventana,
            conexion=self.modelo.conexion,
            estado="MODIFICAR",
            datos_pd=datos_pd
        )

        if guardado:
            self.cargar()

    # =====================================================
    # ELIMINAR (CON CONTRASEÑA)
    # =====================================================
    def eliminar(self):
        seleccionado = self.tree.focus()

        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccione un parte diario para eliminar",
                parent=self.ventana
            )
            return

        password = simpledialog.askstring(
            "Seguridad",
            "Ingrese la contraseña para eliminar:",
            show="*",
            parent=self.ventana
        )

        if password != CLAVE_ELIMINAR_PD:
            messagebox.showerror(
                "Acceso denegado",
                "Contraseña incorrecta",
                parent=self.ventana
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar el parte diario ID {seleccionado}?",
            parent=self.ventana
        )

        if not confirmar:
            return

        # 🔹 Llamada al método de la clase modelo
        if self.modelo.eliminar_partediario(seleccionado):
            messagebox.showinfo(
                "Éxito",
                "Parte diario eliminado correctamente",
                parent=self.ventana
            )
            self.cargar()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el parte diario",
                parent=self.ventana
            )
