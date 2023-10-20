from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from asistencia import AsistenciaDB


class Listado:
    def __init__(self, panel):
        self.root = panel
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        self.root.title("Listado de Asistencia")
        self.root.iconbitmap("SetUp/icono.ico")

        self.tree = Treeview(self.root, columns=("N°", "Nombre", "Hora de entrada", "Hora de salida"), show="headings", height=1)
        Style().configure("Treeview.Heading", font=("Arial", 10))
        Style().configure("Treeview", font=("Arial", 10))
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(expand=True, fill=BOTH)
        self.recuperar_listado()

    def recuperar_listado(self):
        ast = AsistenciaDB()
        data = ast.getAsistencia()
        if data:
            for row in data:
                self.tree.insert("", "end", values=row)
        else:
            messagebox.showwarning(message="No se encontraron datos", title="Consulta")


if __name__ == "__main__":
    root = Tk()
    app = Listado(root)
    root.mainloop()
