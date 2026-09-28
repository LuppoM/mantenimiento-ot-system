class OTGraficosModelo:
    def __init__(self, repositorio_ot):
        self.repo = repositorio_ot
        self.conexion = repositorio_ot.conexion

    def obtener_todas(self):
        cursor = self.conexion.cursor()
        # Traemos la columna Planta para identificar el origen de los datos
        cursor.execute('SELECT Fecha, Realizada, Planta, Sector, "Mantenimiento correctivo" FROM OT')
        filas = cursor.fetchall()
        resultado = []

        for fila in filas:
            fecha_raw, realizada, planta, linea, tipo_ot = fila
            fecha_dt = self.repo.fecha_segura(fecha_raw)
            if not fecha_dt: continue

            resultado.append({
                "fecha": fecha_dt,
                "cerrada": self.repo.texto_seguro(realizada),
                "planta": self.repo.texto_seguro(planta),
                "linea": self.repo.texto_seguro(linea),
                "tipo_ot": self.repo.texto_seguro(tipo_ot)
            })
        return resultado

    def obtener_planta_bd(self):
        """Busca el nombre de la planta que se repite en la base de datos"""
        cursor = self.conexion.cursor()
        # Buscamos el primer registro que tenga el nombre de la planta cargado
        cursor.execute('SELECT Planta FROM OT WHERE Planta IS NOT NULL AND Planta != "" LIMIT 1')
        fila = cursor.fetchone()
        return fila[0] if fila else "Planta no definida"

    def filtrar(self, planta=None, linea=None, mes=None, anio=None, tipo_ot=None):
        datos = self.obtener_todas()
        # El filtro de planta se mantiene por si el usuario usa el combo, sino usa todos los datos
        if planta and planta != "":
            datos = [x for x in datos if x["planta"] == planta]
            
        filtradas = self.repo.filtrar_lista(datos, None, linea, mes, anio)
        
        if tipo_ot:
            filtradas = [x for x in filtradas if x["tipo_ot"].upper() == tipo_ot.upper()]
        
        return filtradas

    def resumen(self, planta=None, linea=None, mes=None, anio=None, tipo_ot=None):
        ot_filtradas = self.filtrar(planta, linea, mes, anio, tipo_ot)
        gen = len(ot_filtradas)
        cerr = sum(1 for x in ot_filtradas if self.repo.es_cerrada(x["cerrada"]))
        porc = (cerr / gen * 100) if gen else 0
        
        return {
            "generadas": gen, "cerradas": cerr, "pendientes": gen - cerr, 
            "porcentaje_cierre": round(porc, 2),
            "nombre_planta": self.obtener_planta_bd() # Aquí saca el nombre real
        }

    def resumen_anual(self, planta=None, linea=None, anio=None, tipo_ot=None):
        datos = self.filtrar(planta, linea, None, anio, tipo_ot)
        meses_nombre = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        gen = [0] * 12
        cerr = [0] * 12

        for ot in datos:
            idx = ot["fecha"].month - 1
            gen[idx] += 1
            if self.repo.es_cerrada(ot["cerrada"]): cerr[idx] += 1

        total_gen = sum(gen)
        total_cerr = sum(cerr)
        porc_anual = (total_cerr / total_gen * 100) if total_gen > 0 else 0

        return {
            "meses": meses_nombre, "generadas": gen, "cerradas": cerr,
            "pendientes": [gen[i] - cerr[i] for i in range(12)],
            "porcentaje_anual": round(porc_anual, 2),
            "nombre_planta": self.obtener_planta_bd() # Aquí saca el nombre real
        }