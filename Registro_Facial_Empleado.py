from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style


class RFE:
    def __init__(self, panel):
        self.root = panel
        self.root.title("Registro de Empleados")
        self.root.geometry("800x500")
        self.root.iconbitmap("SetUp/icono.ico")

        self.frame = Frame(self.root, width=200, height=200, bg="lightblue")
        self.frameOption = Frame(self.root, width=200, height=200, bg="black")

        self.frame.pack(side="top", fill="both", expand=True)
        self.frameOption.pack(side="bottom", fill="both", expand=True)

        self.label_nombre = Label(self.frame, text="Ingrese un nombre a buscar:")
        self.label_nombre.pack(padx=20, pady=5)

        self.entry_nombre = Entry(self.frame)
        self.entry_nombre.pack(padx=20, pady=5)

        self.id_seleccionado = Label(self.frame, text="N°: ")
        self.id_seleccionado.place(x=0, y=0)

        self.tree = Treeview(self.frame, columns=("N°", "Name", "Finca", "Status"), show="headings")
        self.tree.heading("N°", text="N°")
        self.tree.heading("Name", text="Nombre")
        self.tree.heading("Finca", text="Finca")
        self.tree.heading("Status", text="Estado")
        Style().configure("Treeview.Heading", font=("Arial", 10))
        Style().configure("Treeview", font=("Arial", 10))
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(expand=True, fill=BOTH)

        self.label_nombre = Label(self.root, text="Seleccione el empleado a registrar")
        self.label_nombre.pack(padx=20, pady=5)

        self.btn_registrar_face = Button(self.frameOption, text="Registrar Rostro", bg="lightblue", state="disabled")
        self.btn_registrar_face.pack(padx=20, pady=5)

    def set_tree_data(self, data):
        self.tree.delete(*self.tree.get_children())
        if data:
            for row in data:
                self.tree.insert("", "end", values=row)
        else:
            self.btn_registrar_face.config(state="disabled")
            self.entry_nombre.config(state="disabled")
            messagebox.showwarning(message="No se encontraron datos", title="Consulta")

