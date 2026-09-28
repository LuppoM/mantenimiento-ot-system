# mantenimiento-ot-system
Sistema CMMS en Python y SQL (MVC) para gestión de Órdenes de Trabajo, trazabilidad operacional ,presentaciones y reportes automáticos en PDF.

Sistema CMMS & Gestión Integral de Mantenimiento Industrial
Solución de software de escritorio desarrollada en Python y SQL bajo arquitectura MVC (Model-View-Controller) para la digitalización, control operativo, trazabilidad y automatización de reportes en plantas industriales.

Módulos del Sistema
Gestión de Órdenes de Trabajo (OT): Ciclo de vida completo de OTs, asignación a mecánicos, prioridades y estados.

Parte Diario Operativo: Registro y seguimiento diario de novedades, incidencias y paradas no programadas.

Planificación de Tareas (Fin de Semana / Paradas): Módulo para gestión, programación y exportación en PDF de planes de trabajo intensivo.

Notas de Pedido (Insumos & Repuestos): Emisión y trazabilidad de solicitudes de materiales para intervenciones de mantenimiento.

Analítica & Gráficos: Visualización de métricas y tendencias operativas para control de gestión (OEE / Paradas).

Gestión de Entidades: ABM estructurado para Plantas, Sectores y Personal Mecánico.

Servicios de Impresión & Exportación: Generación dinámica de reportes consolidados y fichas técnicas en PDF (ReportLab).

Arquitectura del Proyecto (Patrón MVC Modular)
El proyecto implementa una clara separación de responsabilidades para garantizar la mantenibilidad y escalabilidad del código:

Plaintext
├── Módulos Core
│   ├── principal*.py           # Punto de entrada y orquestación de interfaz
│   ├── ot*.py / abmot*.py      # Dominio de Órdenes de Trabajo
│   ├── partediario*.py         # Dominio de Partes Diarios
│   ├── np*.py / abmnp*.py      # Dominio de Notas de Pedido
│   ├── tareas*.py              # Dominio de Tareas Programadas
│   ├── otgraficos*.py          # Módulo de analítica y visualización
│   └── sectores* / mecanicos*  # Administración de recursos y estructura
├── Servicios & Persistencia
│   ├── otrepositorio.py        # Capa de acceso y abstracción de datos
│   ├── pdfservice.py           # Servicio de maquetación y generación de PDF
│   └── seleccionbd.py          # Configuración y conexión SQL
Tecnologías Utilizadas
Lenguaje: Python 3.x

Interfaz Gráfica: Tkinter / ttk

Base de Datos: SQLite / MySQL

Reportes & Gráficos: ReportLab / Matplotlib

Empaquetado: PyInstaller (.exe)

Control de Versiones: Git & GitHub
