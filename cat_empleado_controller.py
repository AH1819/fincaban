from tkinter import *
from cat_empleado import CatEmpleadoModel
from Registro_Facial_Empleado import RFE
from RegistrarRostro import RegistroFace


class CatEmpleadoController:
    def __init__(self, modelo, vista):
        self.model = modelo
        self.view = vista
        self.data_list = []
        self.list_seleccionado = []
        self.id_emp = 0

        self.refresh_tree_data()
        self.view.btn_registrar_face.config(command=self.abrir_registro)
        self.view.entry_nombre.bind("<KeyRelease>", self.buscar_por_nombre)
        self.view.tree.bind("<ButtonRelease-1>", self.recuperar_id)

    def refresh_tree_data(self):
        self.data_list = self.model.fetch_all()
        self.view.set_tree_data(self.data_list)

    def buscar_por_nombre(self, event):
        self.id_emp = 0
        self.view.id_seleccionado.config(text="N°: ")
        self.view.btn_registrar_face.config(state="disabled")

        nombre = self.view.entry_nombre.get()

        if len(nombre) > 2:

            filtered_data = [row for row in self.data_list if nombre.lower() in row[1].lower()]
            if len(filtered_data) > 0:
                self.view.set_tree_data(filtered_data)
            else:
                self.refresh_tree_data()
        elif not nombre:
            self.refresh_tree_data()

    def recuperar_id(self, event):
        selected_item = self.view.tree.selection()
        if selected_item:
            self.list_seleccionado = self.view.tree.item(selected_item, "values")
            self.view.id_seleccionado.config(text=f"N°: {self.list_seleccionado[0]}")
            self.view.btn_registrar_face.config(state="normal")

    def abrir_registro(self):
        panel = Toplevel()
        RegistroFace(panel, self.list_seleccionado)
        panel.mainloop()

