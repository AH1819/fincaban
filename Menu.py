from tkinter import *
from Registro_Facial_Empleado import RFE
from Tomar_asistencia import Asistencia
from cat_empleado import CatEmpleadoModel
from cat_empleado_controller import CatEmpleadoController


class Menu:
    def __init__(self, panel):
        self.root = panel
        self.root.title("Menu principal")
        self.root.geometry("800x400")
        self.root.resizable(False, False)

        self.fondo = PhotoImage(file="Recursos/Fondos/fondo.png")
        self.background = Label(self.root, image=self.fondo, text="Inicio")
        self.background.place(x=0, y=0, relwidth=1, relheight=1)

        self.Info = Label(self.root, text="Control de Asistencia", bg="#99FF99", font=("Helvetica", 30))
        self.Info.place(y=50, relx=0.5, anchor="center")

        self.BtnRegistro = Button(self.root, text="Capturar Datos Biométricos", font=("Helvetica", 18),
                                  command=self.registrar)
        self.BtnRegistro.place(y=120, relx=0.5, anchor="center")

        self.BtnAsistencia = Button(self.root, text="Registro de Asistencia", font=("Helvetica", 18),
                                    command=self.asistencia)
        self.BtnAsistencia.place(y=190, relx=0.5, anchor="center")

    def registrar(self):
        self.root.withdraw()
        panel = Toplevel()
        view = RFE(panel)
        model = CatEmpleadoModel()
        CatEmpleadoController(model, view)
        panel.deiconify()
        panel.protocol("WM_DELETE_WINDOW", lambda: self.mostrar_root(panel))
        panel.mainloop()

    def asistencia(self):
        self.root.withdraw()
        panel = Toplevel()
        Asistencia(panel)
        panel.deiconify()
        panel.protocol("WM_DELETE_WINDOW", lambda: self.mostrar_root(panel))
        panel.mainloop()

    def mostrar_root(self, panel):
        self.root.deiconify()
        panel.destroy()


if __name__ == "__main__":
    root = Tk()
    app = Menu(root)
    root.mainloop()
