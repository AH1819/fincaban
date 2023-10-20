from tkinter import *
from Registro_Facial_Empleado import RFE
from Tomar_asistencia_entrada import AsistenciaEntrada
from Tomar_asistencia_salida import AsistenciaSalida
from cat_empleado import CatEmpleadoModel
from cat_empleado_controller import CatEmpleadoController


class Menu:
    def __init__(self, panel):
        self.root = panel
        self.root.title("Menu principal")
        self.root.geometry("800x400")
        self.root.iconbitmap("SetUp/icono.ico")
        self.root.resizable(False, False)

        self.fondo = PhotoImage(file="Recursos/Fondos/fondo.png")
        self.background = Label(self.root, image=self.fondo, text="Inicio")
        self.background.place(x=0, y=0, relwidth=1, relheight=1)

        self.Info = Label(self.root, text="Control de Asistencia", font=("Helvetica", 30))
        self.Info.pack(side=TOP, pady=50)

        button_frame = Frame(self.root, bg="")
        button_frame.pack(side=TOP)

        self.BtnEntrada = Button(button_frame, text="Registro de Entradas", bg="#72DE0D", font=("Helvetica", 18),
                                 command=self.asistencia_entrada)
        self.BtnEntrada.pack(side=LEFT, padx=10, pady=10)

        self.BtnSalida = Button(button_frame, text="Registro de Salidas", bg="#DE430D", font=("Helvetica", 18),
                                command=self.asistencia_salida)
        self.BtnSalida.pack(side=LEFT, padx=10, pady=10)

        self.BtnRegistro = Button(self.root, text="Capturar Datos Biométricos", bg="#DEC80D", font=("Helvetica", 18),
                                  command=self.registrar)
        self.BtnRegistro.pack(side=TOP, pady=10)

    def registrar(self):
        self.root.withdraw()
        panel = Toplevel()
        view = RFE(panel)
        model = CatEmpleadoModel()
        CatEmpleadoController(model, view)
        panel.deiconify()
        panel.protocol("WM_DELETE_WINDOW", lambda: self.mostrar_root(panel))
        panel.mainloop()

    def asistencia_entrada(self):
        self.root.withdraw()
        panel = Toplevel()
        AsistenciaEntrada(panel)
        panel.deiconify()
        panel.protocol("WM_DELETE_WINDOW", lambda: self.mostrar_root(panel))
        panel.mainloop()

    def asistencia_salida(self):
        self.root.withdraw()
        panel = Toplevel()
        AsistenciaSalida(panel)
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
