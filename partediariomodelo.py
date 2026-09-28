from datetime import datetime

class ParteDiarioModelo:
    def __init__(self, conexion):
        self.conexion = conexion

    # -------------------------
    # HELPERS
    # -------------------------
    def _texto(self, v):
        return str(v).strip() if v else ""

    def _fecha(self, f):
        if not f:
            return None

        formatos = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d")
        for fmt in formatos:
            try:
                return datetime.strptime(str(f), fmt)
            except ValueError:
                pass
        return None

    # -------------------------
    # OBTENER TODOS (para tabla)
    # -------------------------
    def obtener_todos(self):
        cur = self.conexion.cursor()
        cur.execute("""
            SELECT
                ID,
                Fecha,
                Nombre,
                Turno,
                "Codigo maquina",
                Reporte
            FROM Partediario
            ORDER BY ID
        """)

        datos = []
        for fila in cur.fetchall():
            id_, fecha_raw, nombre, turno, codigo, reporte = fila
            fecha_dt = self._fecha(fecha_raw)
            if not fecha_dt:
                continue

            datos.append({
                "id": id_,
                "fecha": fecha_dt,
                "nombre": self._texto(nombre),
                "turno": self._texto(turno),
                "codigo": self._texto(codigo),
                "reporte": self._texto(reporte)
            })

        cur.close()
        return datos

    # -------------------------
    # FILTRO (tabla)
    # -------------------------
    def filtrar(self, campo, valor):
        registros = self.obtener_todos()

        if not campo or not valor:
            return registros

        campo = campo.lower()
        valor = valor.strip().lower()
        resultado = []

        for r in registros:
            if campo == "id":
                # permite buscar ID exacto o parcial
                if valor.isdigit() and valor in str(r["id"]):
                    resultado.append(r)

            elif campo == "fecha":
                fecha_filtro = self._fecha(valor)
                if fecha_filtro and r["fecha"].date() == fecha_filtro.date():
                    resultado.append(r)

            elif campo == "nombre" and valor in r["nombre"].lower():
                resultado.append(r)

            elif campo == "turno" and valor in r["turno"].lower():
                resultado.append(r)

            elif campo == "codigo maquina" and valor in r["codigo"].lower():
                resultado.append(r)

            elif campo == "reporte" and valor in r["reporte"].lower():
                resultado.append(r)

        return resultado

    # -------------------------
    # OBTENER POR ID (ABM)
    # -------------------------
    def obtener_por_id(self, id_pd):
        cur = self.conexion.cursor()
        cur.execute("""
            SELECT
                ID,
                Fecha,
                Nombre,
                Turno,
                "Codigo maquina",
                Reporte
            FROM Partediario
            WHERE ID = ?
        """, (id_pd,))

        fila = cur.fetchone()
        cur.close()

        if not fila:
            return None

        id_, fecha_raw, nombre, turno, codigo, reporte = fila

        return {
            "ID": id_,
            "Fecha": fecha_raw,  # string → DateEntry
            "Nombre": self._texto(nombre),
            "Turno": self._texto(turno),
            "Codigo maquina": self._texto(codigo),
            "Reporte": self._texto(reporte)
        }

    # -------------------------
    # ELIMINAR REGISTRO
    # -------------------------
    def eliminar_partediario(self, id_pd):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("DELETE FROM Partediario WHERE ID = ?", (id_pd,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print("Error al eliminar parte diario:", e)
            return False
        finally:
            cursor.close()
