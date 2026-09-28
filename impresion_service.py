import os
import win32print
import win32api


class ImpresionService:

    # --------------------------
    def listar_impresoras(self):

        impresoras = []

        flags = (
            win32print.PRINTER_ENUM_LOCAL |
            win32print.PRINTER_ENUM_CONNECTIONS
        )

        for printer in win32print.EnumPrinters(flags):
            impresoras.append(printer[2])

        return impresoras

    # --------------------------
    def imprimir(self, ruta_pdf, impresora=None):

        if not os.path.exists(ruta_pdf):
            raise FileNotFoundError("No existe el PDF")

        if impresora:
            win32print.SetDefaultPrinter(impresora)

        win32api.ShellExecute(
            0,
            "print",
            ruta_pdf,
            None,
            ".",
            0
        )
