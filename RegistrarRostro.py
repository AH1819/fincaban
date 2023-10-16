from tkinter import *
from tkinter import messagebox
from datos_biometricos import DatosBiometricos
import cv2
from PIL import Image, ImageTk
import imutils
import mediapipe as mp
import os


class RegistroFace:
    def __init__(self, panel, lista):
        self.OutFolderPathUser = 'DataBase/Users'
        self.PathUserCheck = 'DataBase/Users/'
        self.OutFolderPathFace = 'DataBase/Faces Recognition'
        self.img_step0 = cv2.imread("SetUp/Step0.png")
        self.img_step1 = cv2.imread("SetUp/Step1.png")
        self.img_check = cv2.imread("SetUp/check.png")
        self.img_liche = cv2.imread("SetUp/LivenessCheck.png")
        self.registro = None
        self.lblVideo = None
        self.cap = None
        self.capturar = False
        self.root = panel
        self.empleado = lista
        self.muestra = 0
        self.step = 0

        # Margen
        self.offsety = 30
        self.offsetx = 20

        # Umbral
        self.confThreshold = 0.5
        self.blurThreshold = 15

        # Tool Draw
        self.mpDraw = mp.solutions.drawing_utils
        self.ConfigDraw = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)  # Ajustamos la configuration de dibujo

        # Object Face Mesh
        self.FacemeshObject = mp.solutions.face_mesh
        self.FaceMesh = self.FacemeshObject.FaceMesh(max_num_faces=1)

        # Object Detect
        self.FaceObject = mp.solutions.face_detection
        self.detector = self.FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)

        self.root.title("Registro de Empleados")
        self.root.geometry("1280x620")
        self.root.iconbitmap("SetUp/icono.ico")

        self.frame_video = Frame(self.root, bg="black")
        self.frame_video.pack(side="left", fill="both", expand=True)

        self.frame_options = Frame(self.root, bg="lightblue")
        self.frame_options.pack(side="right", fill="both")

        self.btnCapturarFoto = Button(self.frame_options, text="Capturar Foto", command=self.capturar_foto,
                                      state="disabled")
        self.btnCapturarFoto.pack(padx=20, pady=20)

        self.log()

    def guardar_user(self):
        # Save Info
        f = open(f"{self.OutFolderPathUser}/{self.empleado[0]}.txt", 'w')
        f.writelines(str(self.empleado[0]) + ',')
        f.writelines(self.empleado[1] + ',')
        f.writelines(self.empleado[2] + ',')
        f.writelines(self.empleado[3] + ',')
        f.close()

    def capturar_foto(self):
        self.capturar = True

    def log(self):
        print("Log")
        if self.empleado:
            print("Empleado pasado")
            # Info Completed
            # Check users
            UserList = os.listdir(self.PathUserCheck)
            # Ids Users
            UserId = []
            for lis in UserList:
                # Extract Id
                id_emp = lis
                id_emp = id_emp.split('.')
                # Save
                UserId.append(id_emp[0])
            # Check Names
            print(f"{self.empleado[0]} == {UserId}")
            if str(self.empleado[0]) in UserId:
                # Registrado
                print("USUARIO REGISTRADO ANTERIORMENTE")
            else:
                # Video
                self.lblVideo = Label(self.frame_video)
                self.lblVideo.place(rely=0.5, relx=0.5, anchor="center")
                # lblVideo.place(x=320, y=115)

                # Elegimos la camara
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                self.cap.set(3, 1280)
                self.cap.set(4, 720)
                self.log_biometric()

    def log_biometric(self):
        # Leemos la video captura
        global step
        step = 0

        if self.cap is not None:
            ret, frame = self.cap.read()

            # Frame Save
            frameSave = frame.copy()

            # RGB
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Show
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Si es correcta
            if ret:

                # Inference
                res = self.FaceMesh.process(frameRGB)

                # List Results
                px = []
                py = []
                lista = []

                # Resultados
                if res.multi_face_landmarks:
                    # Iteramos
                    for rostros in res.multi_face_landmarks:

                        # Draw Face Mesh
                        self.mpDraw.draw_landmarks(frame, rostros, self.FacemeshObject.FACEMESH_CONTOURS,
                                                   self.ConfigDraw, self.ConfigDraw)

                        # Extract KeyPoints
                        for id, puntos in enumerate(rostros.landmark):

                            # Info IMG
                            al, an, c = frame.shape
                            x, y = int(puntos.x * an), int(puntos.y * al)
                            px.append(x)
                            py.append(y)
                            lista.append([id, x, y])

                            # 468 KeyPoints
                            if len(lista) == 468:

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

                                        # Threshold
                                        if score > self.confThreshold:
                                            # Info IMG
                                            alimg, animg, c = frame.shape

                                            # Coordenates
                                            xi, yi, an, al = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                            xi, yi, an, al = int(xi * animg), int(yi * alimg), int(
                                                an * animg), int(al * alimg)

                                            # Width
                                            offsetan = (self.offsetx / 100) * an
                                            xi = int(xi - int(offsetan / 2))
                                            an = int(an + offsetan)
                                            xf = xi + an

                                            # Height
                                            offsetal = (self.offsety / 100) * al
                                            yi = int(yi - offsetal)
                                            al = int(al + offsetal)
                                            yf = yi + al

                                            # Error < 0
                                            if xi < 0: xi = 0
                                            if yi < 0: yi = 0
                                            if an < 0: an = 0
                                            if al < 0: al = 0

                                        # Steps
                                        if step == 0:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)
                                            cv2.rectangle(frame, (xi - 100, yi - 100, xf - 350, yf + 50), (255, 0, 0),
                                                          2)
                                            # IMG Step0
                                            alis0, anis0, c = self.img_step0.shape
                                            frame[50:50 + alis0, 50:50 + anis0] = self.img_step0

                                            # IMG Step1
                                            alis1, anis1, c = self.img_step1.shape
                                            frame[50:50 + alis1, 1030:1030 + anis1] = self.img_step1

                                            # Condiciones
                                            print(f"x7: {x7} x5: {x5} x8: {x8} x6: {x6}")
                                            if x7 > x5 and x8 < x6:
                                                # IMG check
                                                alich, anich, c = self.img_check.shape
                                                frame[165:165 + alich, 1105:1105 + anich] = self.img_check
                                                self.btnCapturarFoto.config(state="active")
                                                if self.capturar:
                                                    # Cut
                                                    cut = frameSave[yi:yf, xi:xf]
                                                    # Save Image Without Draw
                                                    cv2.imwrite(f"{self.OutFolderPathFace}/{self.empleado[0]}.png", cut)
                                                    db = DatosBiometricos()
                                                    self.registro = db.insertar_rostro(self.empleado[0], f"{self.OutFolderPathFace}/{self.empleado[0]}.png")
                                                    # Cerramos
                                                    step = 1

                                        if step == 1:
                                            self.cap.release()
                                            if self.registro:
                                                messagebox.showinfo(message="Registrado con éxito", title="Registro")
                                                self.guardar_user()
                                            else:
                                                messagebox.showerror(message="Error al registrar", title="Registro")
                                            return

                # Redimensionamos el video
                frame = imutils.resize(frame, width=1150)

                # Convertimos el video
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                # Mostramos en el GUI
                self.lblVideo.configure(image=img)
                self.lblVideo.image = img
                self.lblVideo.after(10, self.log_biometric)

            else:
                self.cap.release()

