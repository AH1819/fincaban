import threading
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from cat_empleado import CatEmpleadoModel
from ListadoAsistencia import Listado
from asistencia import AsistenciaDB
import face_recognition as fr
from PIL import Image, ImageTk
import numpy as np
import mediapipe as mp
import math
import imutils
import cv2
import os


class AsistenciaEntrada:
    def __init__(self, panel):
        self.escaneado = None
        self.FaceMesh = None
        self.FaceObject = None
        self.detector = None
        self.FacemeshObject = None
        self.ConfigDraw = None
        self.mpDraw = None
        self.OutFolderPathFace = 'DataBase/Faces Recognition'
        self.img_step0 = cv2.imread("SetUp/Step0.png")
        self.img_step1 = cv2.imread("SetUp/Step1.png")
        self.img_step2 = cv2.imread("SetUp/Step2.png")
        self.img_check = cv2.imread("SetUp/check.png")
        self.UserName = None
        self.lblVideo = None
        self.cap = None
        self.FaceCode = None
        self.images = []
        self.clases = []
        self.parpadeo = False
        self.conteo = 0
        self.rechazo = 0
        self.step = 0
        # Umbral
        self.confThreshold = 0.5
        self.blurThreshold = 15
        # Margen
        self.offsety = 30
        self.offsetx = 20

        self.root = panel

        # Configurar la geometría de la ventana
        self.root.state('zoomed')
        self.root.resizable(False, False)
        self.root.title("Registro de Empleados")
        self.root.iconbitmap("SetUp/icono.ico")

        self.frame_video = Frame(self.root, bg="black")
        self.frame_video.pack(side="top", fill=BOTH, expand=True)

        self.frame_options = Frame(self.root, bg="lightblue")
        self.frame_options.pack(side="bottom", fill=BOTH)

        self.tree = Treeview(self.frame_options, columns=("N°", "Name", "Finca", "Status"), show="headings", height=1)
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

        self.iniciar = Button(self.frame_options, text="Iniciar Captura", font=("Helvetica", 10),
                              command=self.inicar_captura)
        self.iniciar.pack(side=LEFT, padx=100, pady=10)
        self.detener = Button(self.frame_options, text="Detener Captura", font=("Helvetica", 10),
                              state="disabled", command=self.detener_captura)
        self.detener.pack(side=LEFT, padx=100, pady=10)
        self.confirma = Button(self.frame_options, text="Confirmar Entrada", font=("Helvetica", 10),
                               command=self.registrar_asistencia, state="disabled")
        self.confirma.pack(side=LEFT, padx=100, pady=10)
        self.listado = Button(self.frame_options, text="Mostrar listado actual", font=("Helvetica", 10),
                              command=self.mostrar_listado)
        self.listado.pack(side=LEFT, padx=100, pady=10)

    def code_face(self):
        listacod = []

        # Iteramos
        for img in self.images:
            # Correction de color
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Codificamos la imagen
            cod = fr.face_encodings(img)[0]
            # Almacenamos
            listacod.append(cod)

        return listacod

    def sign(self):
        self.iniciar.config(state="disabled")
        lista = os.listdir(self.OutFolderPathFace)

        for lis in lista:
            imgdb = cv2.imread(f'{self.OutFolderPathFace}/{lis}')
            self.images.append(imgdb)
            self.clases.append(os.path.splitext(lis)[0])

        # Face Code
        self.FaceCode = self.code_face()

        self.lblVideo = Label(self.frame_video)
        self.lblVideo.place(y=20, rely=0.5, relx=0.5, anchor="center")

        # Elegimos la camara
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.detener.config(state="active")
        self.sign_biometric()

    def sign_biometric(self):

        if self.cap is not None:
            ret, frame = self.cap.read()
            frameCopy = frame.copy()
            frameFR = cv2.resize(frameCopy, (0, 0), None, 0.25, 0.25)
            rgb = cv2.cvtColor(frameFR, cv2.COLOR_BGR2RGB)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if ret:
                res = self.FaceMesh.process(frameRGB)
                px = []
                py = []
                lista = []

                if res.multi_face_landmarks and len(res.multi_face_landmarks) > 0:
                    rostros = res.multi_face_landmarks[0]
                    self.mpDraw.draw_landmarks(frame, rostros, self.FacemeshObject.FACEMESH_CONTOURS,
                                               self.ConfigDraw, self.ConfigDraw)

                    for id, puntos in enumerate(rostros.landmark):
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])

                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            longitud1 = math.hypot(x2 - x1, y2 - y1)

                            # Ojo Izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            longitud2 = math.hypot(x4 - x3, y4 - y3)
                            # print(longitud2)

                            # Parietal Derecho
                            x5, y5 = lista[139][1:]
                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            # Ceja Izquierda
                            x8, y8 = lista[300][1:]

                            # Face Detect
                            faces = self.detector.process(frameRGB)

                            if faces.detections is not None:

                                for face in faces.detections:
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    if score > self.confThreshold:
                                        # Info IMG
                                        alimg, animg, c = frame.shape

                                        # Coordinates
                                        xi, yi, an, al = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, an, al = int(xi * animg), int(yi * alimg), int(
                                            an * animg), int(al * alimg)

                                        # Width
                                        offsetan = (self.offsetx / 100) * an
                                        xi = int(xi - int(offsetan / 2))
                                        an = int(an + offsetan)

                                        # Height
                                        offsetal = (self.offsety / 100) * al
                                        yi = int(yi - offsetal)
                                        al = int(al + offsetal)

                                        # Error < 0
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if an < 0: an = 0
                                        if al < 0: al = 0

                                        # Steps
                                        if self.step == 0:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)

                                            # IMG Step0
                                            alis0, anis0, c = self.img_step0.shape
                                            frame[30:30 + alis0, 50:50 + anis0] = self.img_step0

                                            # IMG Step1
                                            alis1, anis1, c = self.img_step1.shape
                                            frame[30:30 + alis1, 1030:1030 + anis1] = self.img_step1

                                            # IMG Step2
                                            alis2, anis2, c = self.img_step2.shape
                                            frame[250:250 + alis2, 1030:1030 + anis2] = self.img_step2

                                            # Condiciones
                                            if x7 > x5 and x8 < x6:
                                                # Cont Parpadeos
                                                if longitud1 <= 10 and longitud2 <= 10 and self.parpadeo == False:
                                                    self.conteo = self.conteo + 1
                                                    self.parpadeo = True

                                                elif longitud2 > 10 and longitud2 > 10 and self.parpadeo == True:
                                                    self.parpadeo = False

                                                # IMG check
                                                alich, anich, c = self.img_check.shape
                                                frame[145:145 + alich, 1105:1105 + anich] = self.img_check
                                                # Parpadeos
                                                # Conteo de parpadeos
                                                cv2.putText(frame, f'Parpadeos: {int(self.conteo)}', (1070, 355),
                                                            cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                                            (255, 255, 255), 1)
                                                if self.conteo >= 3:
                                                    if longitud1 > 12 and longitud2 > 12:
                                                        self.step = 1
                                            else:
                                                self.conteo = 0
                                        if self.step == 1:
                                            # Find Faces
                                            faces = fr.face_locations(rgb)
                                            facescod = fr.face_encodings(rgb, faces)
                                            # Iteramos
                                            for facecod, faceloc in zip(facescod, faces):
                                                # Matching
                                                Match = fr.compare_faces(self.FaceCode, facecod)
                                                if len(Match) > 0:
                                                    # Similitud
                                                    simi = fr.face_distance(self.FaceCode, facecod)
                                                    if simi.size > 0:
                                                        # Min
                                                        min = np.argmin(simi)
                                                        # User
                                                        if Match[min]:
                                                            # UserName
                                                            self.UserName = self.clases[min].upper()
                                                            cem = CatEmpleadoModel()
                                                            if self.escaneado is not None:
                                                                if self.escaneado != self.UserName:
                                                                    print("escaneado")
                                                                    self.escaneado = self.UserName
                                                                    self.set_tree_data(cem.search_emp(self.UserName))
                                                            else:
                                                                print("no escaneado")
                                                                self.escaneado = self.UserName
                                                                self.set_tree_data(cem.search_emp(self.UserName))
                                                            self.conteo = 0
                                                            self.parpadeo = False
                                                            self.step = 0
                                                        else:
                                                            cv2.rectangle(frame, (xi, yi, an, al), (250, 21, 12), 2)
                                                            messagebox.showinfo(
                                                                message="No se encontro similitud", title="Título")
                                                    else:
                                                        messagebox.showinfo(
                                                            message="Lista vacia", title="Título")
                                                        self.detener_captura()
                                                else:
                                                    messagebox.showinfo(
                                                        message="No hay rostros en la base de datos",
                                                        title="Título")
                                                    self.detener_captura()

            frame = imutils.resize(frame, width=1280, height=500)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            self.lblVideo.configure(image=img)
            self.lblVideo.image = img
            self.lblVideo.after(10, self.sign_biometric)

        else:
            self.detener_captura()

    def inicar_captura(self):
        # Tool Draw
        self.mpDraw = mp.solutions.drawing_utils
        self.ConfigDraw = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)  # Ajustamos la configuration de dibujo

        # Object Face Mesh
        self.FacemeshObject = mp.solutions.face_mesh
        self.FaceMesh = self.FacemeshObject.FaceMesh(max_num_faces=1)

        # Object Detect
        self.FaceObject = mp.solutions.face_detection
        self.detector = self.FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)
        hilo = threading.Thread(target=self.sign)
        hilo.start()

    def detener_captura(self):
        self.cap.release()
        self.conteo = 0
        self.parpadeo = False
        self.step = 0
        self.iniciar.config(state="active")
        self.confirma.config(state="disabled")
        self.detener.config(state="disabled")
        self.set_tree_data("None")

    def set_tree_data(self, data):
        self.tree.delete(*self.tree.get_children())
        if data:
            self.confirma.config(state="active")
            for row in data:
                self.tree.insert("", "end", values=row)
        else:
            self.confirma.config(state="disabled")
            messagebox.showwarning(message="No se encontraron datos", title="Consulta")

    def mostrar_listado(self):
        panel = Toplevel()
        Listado(panel)
        panel.mainloop()

    def registrar_asistencia(self):
        ast = AsistenciaDB()
        if ast.validar_existencia_registro(self.UserName):  # Válida existencia
            if ast.validar_registro_entrada(self.UserName):  # Válida sí hay alguna entrada
                if ast.registrar_asistencia_entrada(self.UserName):  # Registra la entrada
                    messagebox.showinfo(message="Entrada capturada correctamente", title="Entrada")
                else:
                    messagebox.showerror(message="Hubo un error al capturar la entrada", title="Entrada")
            else:
                messagebox.showinfo(message="Entrada capturada anteriormente", title="Entrada")
        else:
            messagebox.showwarning(message="El empleado no existe o se encuentra Inactivo", title="Lista de asistencia")


if __name__ == "__main__":
    root = Tk()
    app = AsistenciaEntrada(root)
    root.mainloop()
