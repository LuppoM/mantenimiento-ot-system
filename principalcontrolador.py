from principalmodelo import obtener_conexion, realizar_backup
import ot, sectores, mecanicos, partediario, plantas, tareas, time
import Notapedido  # Módulo puente / controlador de Notas de Pedido
from tkinter import messagebox

def inicializar_app(vista):
    # 1. Preparar la ventana
    root = vista.crear_ventana_principal()
    vista.configurar_estilos(root)

    # 2. Conexión única para toda la sesión
    conexion = obtener_conexion()

    # --- LÓGICA DE INACTIVIDAD (10 MINUTOS) ---
    TIEMPO_LIMITE_MS = 10 * 60 * 1000  
    id_timer = [None] 

    def reset_timer(event=None):
        """Reinicia el contador de cierre cada vez que el usuario realiza una acción"""
        if id_timer[0]:
            root.after_cancel(id_timer[0])
        # Si pasan 10 min sin actividad, se dispara el cierre automático
        id_timer[0] = root.after(TIEMPO_LIMITE_MS, lambda: salir(automatico=True))

    # Detectar actividad en cualquier parte de la pantalla
    root.bind_all("<Any-KeyPress>", reset_timer)
    root.bind_all("<Any-ButtonPress>", reset_timer)
    root.bind_all("<Motion>", reset_timer)

    # --- FUNCIONES DE NAVEGACIÓN ---
    def abrir_ordenes_trabajo():
        reset_timer()
        ot.iniciar_ot(root, conexion)

    def abrir_tareas():
        reset_timer()
        tareas.abrir_tareas(root, conexion)

    def abrir_parte_diario():
        reset_timer()
        partediario.abrir_parte_diario(root, conexion)

    def abrir_notas_pedido():
        reset_timer()
        Notapedido.iniciar_notas_pedido(root, conexion)

    def abrir_sectores():
        reset_timer()
        sectores.abrir_sectores(root, conexion)

    def abrir_mecanicos():
        reset_timer()
        mecanicos.abrir_mecanicos(root, conexion)

    def abrir_plantas():
        reset_timer()
        plantas.abrir_plantas(root, conexion)

    # --- CIERRE SEGURO ---
    def salir(automatico=False):
        if not automatico:
            if not messagebox.askyesno("Salir", "¿Desea cerrar el sistema?\nSe realizará una copia de seguridad automática."):
                return

        try:
            # Primero cerramos conexión para liberar el archivo .db
            if conexion:
                conexion.close()
            
            # Ejecución del Backup
            exito, mensaje = realizar_backup()
            
            if not exito and not automatico:
                messagebox.showwarning("Copia de seguridad", f"Atención: No se pudo realizar el backup.\n{mensaje}")
            elif automatico:
                print("Cierre automático por inactividad. Backup realizado.")

        except Exception as e:
            if not automatico:
                messagebox.showerror("Error al cerrar", f"Ocurrió un error: {e}")
        finally:
            root.destroy()

    # --- CONFIGURACIÓN DE BOTONES ---
    botones_lista = [
        ("Órdenes de Trabajo", abrir_ordenes_trabajo),
        ("Tareas fin de semana", abrir_tareas),
        ("Parte Diario", abrir_parte_diario),
        ("Notas de Pedido", abrir_notas_pedido),
        ("Salir", lambda: salir(False))
    ]

    # --- ARMADO DE INTERFAZ ---
    vista.crear_botones(
        root, 
        botones_lista, 
        abrir_sectores=abrir_sectores, 
        abrir_mecanicos=abrir_mecanicos, 
        abrir_plantas=abrir_plantas,
        abrir_notas_pedido=abrir_notas_pedido
    )
    
    # Manejar el cierre desde la "X" de Windows
    root.protocol("WM_DELETE_WINDOW", lambda: salir(False))
    
    # Iniciar el temporizador
    reset_timer()

    # Lanzar el bucle principal
    root.mainloop()