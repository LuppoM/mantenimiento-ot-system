import tkinter as tk
from tkinter import messagebox
import abmnpvista as vista
from seleccionot import seleccionar_ot
from abmnpmodelo import insertar_nota_pedido, actualizar_nota_pedido

def iniciar_abmnp(parent, conexion, modo="AGREGAR", datos_nota=None, id_ot_asociada=None):
    ventana = vista.crear_ventana_abm(parent, f"{modo.title()} Nota de Pedido")
    
    def buscar_ot():
        id_ot = seleccionar_ot(ventana, conexion)
        if id_ot:
            entries["id_ot"].delete(0, "end")
            entries["id_ot"].insert(0, str(id_ot))

    entries, entries_item, tree_items, input_frame = vista.crear_formulario_abm(ventana, buscar_ot)

    # --- AGREGAR Y QUITAR ÍTEMS DE LA GRILLA ---
    def agregar_item():
        cant = entries_item["cantidad"].get().strip()
        det = entries_item["detalle"].get().strip()
        dest_eq = entries_item["destino_equipo"].get().strip()

        if not det or not cant:
            messagebox.showwarning("Atención", "Ingrese detalle y cantidad.", parent=ventana)
            return

        try:
            cant_num = float(cant)
        except ValueError:
            messagebox.showwarning("Atención", "La cantidad debe ser un número válido.", parent=ventana)
            return

        num_item = len(tree_items.get_children()) + 1

        # Inserta id_detalle vacío ("") al inicio para mantener el calce de columnas
        tree_items.insert("", "end", values=("", num_item, cant_num, det, dest_eq))
        
        entries_item["cantidad"].delete(0, "end")
        entries_item["detalle"].delete(0, "end")
        entries_item["destino_equipo"].delete(0, "end")

    def quitar_item():
        sel = tree_items.selection()
        for item in sel:
            tree_items.delete(item)
            
        for i, item in enumerate(tree_items.get_children(), start=1):
            vals = list(tree_items.item(item, "values"))
            vals[1] = i  # Renumera num_item (posición 1)
            tree_items.item(item, values=vals)

    btn_add = tk.Button(input_frame, text="+ Agregar Ítem", command=agregar_item, bg="#4CAF50", fg="white", bd=0, font=("Segoe UI", 9, "bold"))
    btn_add.pack(side=tk.LEFT, padx=5)
    btn_del = tk.Button(input_frame, text="- Quitar", command=quitar_item, bg="#f44336", fg="white", bd=0, font=("Segoe UI", 9, "bold"))
    btn_del.pack(side=tk.LEFT, padx=5)

    # --- GUARDAR ---
    guardado_exitoso = [False]

    def guardar():
        id_ot_val = entries["id_ot"].get().strip() or None
        if id_ot_val is not None:
            try:
                id_ot_val = int(id_ot_val)
            except ValueError:
                id_ot_val = None

        f_ped = entries["fecha_pedido"].get()
        f_req = entries["fecha_requerida"].get()
        dest = entries["destino"].get()
        autor = entries["autor"].get().strip()
        tipo_gasto = entries["tipo_gasto"].get()
        mo = entries["mano_de_obra"].get()
        estado = entries["estado"].get()
        just = entries["justificacion"].get("1.0", "end-1c").strip()

        if not autor:
            messagebox.showwarning("Atención", "El campo Solicitante/Autor es obligatorio.", parent=ventana)
            return

        if not tipo_gasto or not mo or not estado:
            messagebox.showwarning("Atención", "Los campos Tipo de Gasto, Mano de Obra y Estado no pueden estar vacíos.", parent=ventana)
            return

        cabecera = {
            "id_ot": id_ot_val,
            "fecha_pedido": f_ped,
            "fecha_requerida": f_req,
            "destino": dest,
            "autor": autor,
            "tipo_gasto": tipo_gasto,
            "mano_de_obra": mo,
            "estado": estado,
            "justificacion": just
        }

        detalles = []
        for item in tree_items.get_children():
            v = tree_items.item(item, "values")
            # v[0]=id_detalle, v[1]=num_item, v[2]=cantidad, v[3]=detalle, v[4]=destino_equipo
            detalles.append({
                "num_item": int(v[1]),
                "cantidad": float(v[2]),
                "detalle": str(v[3]),
                "destino_equipo": str(v[4])
            })

        try:
            if modo == "AGREGAR":
                insertar_nota_pedido(conexion, cabecera, detalles)
            elif modo == "MODIFICAR":
                id_nota = entries["id_nota"].get()
                actualizar_nota_pedido(conexion, id_nota, cabecera, detalles)

            guardado_exitoso[0] = True
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}", parent=ventana)

    # --- CARGA DE DATOS INICIAL ---
    if id_ot_asociada and "id_ot" in entries:
        entries["id_ot"].insert(0, str(id_ot_asociada))

    if modo == "MODIFICAR" and datos_nota:
        cab = datos_nota.get("cabecera", {})
        
        if "id_nota" in entries:
            entries["id_nota"].config(state="normal")
            entries["id_nota"].insert(0, str(cab.get("id_nota", "")))
            entries["id_nota"].config(state="disabled")
        
        if "id_ot" in entries and cab.get("id_ot"): 
            entries["id_ot"].insert(0, str(cab.get("id_ot")))
            
        if "destino" in entries:
            entries["destino"].set(cab.get("destino") or "Planta Golosinas")
            
        if "autor" in entries:
            entries["autor"].insert(0, cab.get("autor", "") or "")
            
        if "tipo_gasto" in entries:
            entries["tipo_gasto"].set(cab.get("tipo_gasto") or "Gasto de Mantenimiento")
            
        if "mano_de_obra" in entries:
            entries["mano_de_obra"].set(cab.get("mano_de_obra") or "Mano de Obra Interna")

        if "estado" in entries:
            entries["estado"].set(cab.get("estado") or "PENDIENTE")

        if "justificacion" in entries and cab.get("justificacion"):
            entries["justificacion"].insert("1.0", cab.get("justificacion"))

        for det in datos_nota.get("detalles", []):
            if isinstance(det, (list, tuple)):
                if len(det) == 6:
                    # id_detalle (0), id_nota (1), num_item (2), cantidad (3), detalle (4), destino_equipo (5)
                    tree_items.insert("", "end", values=(det[0], det[2], det[3], det[4], det[5]))
                else:
                    tree_items.insert("", "end", values=det)
            elif isinstance(det, dict):
                tree_items.insert("", "end", values=(
                    det.get("id_detalle", ""),
                    det.get("num_item", 1),
                    det.get("cantidad", 1),
                    det.get("detalle", ""),
                    det.get("destino_equipo", "")
                ))

    # --- BOTONES DE ACCIÓN ---
    btn_box = tk.Frame(ventana, bg="#f0f4f8")
    btn_box.pack(fill=tk.X, padx=15, pady=10)
    tk.Button(btn_box, text="Guardar", command=guardar, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side=tk.RIGHT, padx=5)
    tk.Button(btn_box, text="Cancelar", command=ventana.destroy, bg="#f44336", fg="white", font=("Segoe UI", 10, "bold"), width=12).pack(side=tk.RIGHT, padx=5)

    parent.wait_window(ventana)
    return guardado_exitoso[0]