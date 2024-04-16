import tkinter as tk
from tkinter import Tk, Label, Button, filedialog, Entry
import nibabel as nib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from metodos.segmentacion import segmentacion
import os
import numpy as np

class segmentacion_ventana(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Segmentación")
        self.config(bg="grey")
        self.geometry("1200x610")

        self.titulo = tk.Label(self, text="NRL-DSKT")
        self.titulo.pack()
        self.titulo.config(font=('Times new roman', 35))
        self.titulo.place(x=400, y=30)
        self.titulo.config(bg="grey")

        self.subtitulo = tk.Label(self, text="Segmentación")
        self.subtitulo.pack()
        self.subtitulo.config(font=('Times new roman', 15))
        self.subtitulo.place(x=100, y=75)
        self.subtitulo.config(bg="grey")

        self.botonCargar = Button(
            self, text="Cargar imagen", command=self.cargar_imagen)
        self.botonCargar.pack()
        self.botonCargar.place(x=100, y=570)

        # Crear un lienzo para mostrar la imagen
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.place(x=100, y=100, width=450, height=450)

        # Seleccionar Ejes
        self.variable = tk.StringVar()
        self.variable.set("Seleccionar")
        self.labelAxis = tk.Label(
            self, text="Movimientos de ejes: ", bg="grey", fg="black")
        self.labelAxis.place(x=580, y=200)
        self.labelAxis.config(font=('Times new roman', 12))

        self.w = tk.OptionMenu(self, self.variable, 'Eje x',
                               'Eje y', 'Eje z', command=self.ejes)
        self.w.place(x=740, y=200)

        # Seleccionar Segmentacion
        self.segmentacion_m = tk.StringVar()
        self.segmentacion_m.set("Seleccionar")
        self.labelMethod1 = tk.Label(
            self, text="Segmentación: ", bg="grey", fg="black")
        self.labelMethod1.place(x=580, y=350)
        self.labelMethod1.config(font=('Times new roman', 12))

        self.opc1 = tk.OptionMenu(self, self.segmentacion_m, "Umbralización",
                      "ISODATA", "K-means", "Region Growing", command=self.seleccion_segmentacion)
        self.opc1.pack()
        self.opc1.place(x=700, y=350)

        self.labelNombre = Label(self, text="Nombre de la imagen:" , bg="grey", fg="black")
        self.labelNombre.pack()
        self.labelNombre.config(font=('Times new roman', 12))
        self.labelNombre.place(x=200, y=570)

        self.entryNombre = Entry(self)
        self.entryNombre.pack()
        self.entryNombre.place(x=350, y=570)

        self.botonGuardar = Button(self, text="Guardar imagen", command=self.guardar_imagen)
        self.botonGuardar.pack()
        self.botonGuardar.place(x=500, y=570)

    def cargar_imagen(self):

        initial_dir = "Resources/images"
        self.file_path = filedialog.askopenfilename(initialdir=initial_dir)
        self.rutaImage = self.file_path
        self.img = nib.load(self.rutaImage)
        self.imagen = self.img.get_fdata()
        self.iniciar()

    def click(self, event):

        if self.ax.contains(event)[0]:
            x = int(event.xdata)
            y = int(event.ydata)

    def iniciar(self):

        self.canvas.delete("all")
        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.imagen[:, :, 0])
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().place(x=0, y=0, width=450, height=450)
        cid = self.fig.canvas.mpl_connect('button_press_event', self.click)

    def escala(self, *args):

        if self.rutaImage != "":
            self.canvas.delete("all")
            if self.variable.get() == 'Eje x':
                self.ax.imshow(self.imagen[self.escalaEjes.get(), :, :])
            elif self.variable.get() == 'Eje y':
                self.ax.imshow(self.imagen[:, self.escalaEjes.get(), :])
            elif self.variable.get() == 'Eje z':
                self.ax.imshow(self.imagen[:, :, self.escalaEjes.get()])
            else:
                self.ax.imshow(self.imagen[:, :, 0])
            self.canvas_widget.draw()
        else:
            pass

    def ejes(self, *args):

        if self.variable.get() == 'X' and self.rutaImage != "":
            self.size = (self.imagen.shape[0])-1
        elif self.variable.get() == 'Y' and self.rutaImage != "":
            self.size = (self.imagen.shape[1])-1
        elif self.variable.get() == 'Z' and self.rutaImage != "":
            self.size = (self.imagen.shape[2])-1
        else:
            self.size = 10
        self.escalaEjes = tk.Scale(self, label=self.variable.get(
        ), from_=0, to=self.size, orient='vertical', bg="grey", fg="black", command=self.escala)
        self.escalaEjes.place(x=20, y=100)

    def seleccion_segmentacion(self, *args):

        canvasSegmentacion = tk.Canvas(
            self, width=300, height=200, bg="grey", highlightbackground="grey", highlightthickness=2)
        canvasSegmentacion.pack()
        canvasSegmentacion.place(x=850, y=200)

        if self.segmentacion_m.get() == 'Umbralización' and self.rutaImage != "":
            self.tautext = tk.Label(
                canvasSegmentacion, text="Tau:", bg="grey", fg="black")
            self.tautext.place(x=100, y=10)
            self.Tau = tk.Entry(canvasSegmentacion, justify="center")
            self.Tau.insert(0, "110")
            self.Tau.place(x=100, y=50)

            self.toletext = tk.Label(
                canvasSegmentacion, text="Tolerancia:", bg="grey", fg="black")
            self.toletext.place(x=100, y=90)
            self.Tol = tk.Entry(canvasSegmentacion, justify="center")
            self.Tol.insert(0, "1")
            self.Tol.place(x=100, y=130)

            self.btn = tk.Button(canvasSegmentacion, text="Aceptar", bg="white",
                                 borderwidth=0, command=lambda: self.confirmacion("1"))
            self.btn.place(x=130, y=160)

        if self.segmentacion_m.get() == 'K-medianas' and self.rutaImage != "":

            self.ks = tk.Label(
                canvasSegmentacion, text="Cantidad de clusters: ", bg="grey", fg="black")
            self.ks.place(x=100, y=10)
            self.clusters = tk.Entry(canvasSegmentacion, justify="center")
            self.clusters.insert(0, "")
            self.clusters.place(x=100, y=50)

            self.iter = tk.Label(
                canvasSegmentacion, text="Número de iteraciones: ", bg="grey", fg="black")
            self.iter.place(x=100, y=90)
            self.num_iteraciones = tk.Entry(
                canvasSegmentacion, justify="center")
            self.num_iteraciones.insert(0, "")
            self.num_iteraciones.place(x=100, y=130)

            self.btn = tk.Button(canvasSegmentacion, text="Aceptar", bg="white",
                                 borderwidth=0, command=lambda: self.confirmacion("2"))
            self.btn.place(x=150, y=170)
        if self.segmentacion_m.get() == 'GMM' and self.rutaImage != "":
            self.imagen = self.img.get_fdata()
            self.imagen = segmentacion.gmm(self.imagen)
            self.escala()

    def confirmacion(self, metodo):

        if metodo == "1":

            self.imagen = self.img.get_fdata()
            self.imagen = segmentacion.thresholding(
                self.imagen, int(self.Tau.get()), int(self.Tol.get()))
            self.escala()

        elif metodo == "2":

            self.imagen = self.img.get_fdata()
            self.imagen = segmentacion.segmentation_kmeans(
                self.imagen, int(self.clusters.get()), int(self.num_iteraciones.get()))
            self.escala()

    # Guardar imagen generada en una carpeta
    def guardar_imagen(self):
        # Abre el cuadro de diálogo para seleccionar la carpeta de destino
        directorio_destino = filedialog.askdirectory()

        # Verifica si se seleccionó una carpeta
        if directorio_destino:
            # Obtiene el nombre ingresado por el usuario en la caja de entrada de texto
            nombre_archivo = self.entryNombre.get()

            # Verifica si se ingresó un nombre de archivo
            if nombre_archivo:
                # Convertir la imagen a un tipo de dato compatible
                imagen_nifti = np.uint8(self.imagen)

                # Construir la imagen NIfTI
                nifti_image = nib.Nifti1Image(imagen_nifti, self.img.affine)

                # Construir la ruta de guardado utilizando la carpeta de destino y el nombre del archivo
                ruta_guardado = os.path.join(directorio_destino, nombre_archivo + ".nii.gz")

                # Guardar la imagen NIfTI
                nib.save(nifti_image, ruta_guardado)
                print("Imagen guardada en:", ruta_guardado)
            else:
                print("Por favor, ingrese un nombre de archivo.")
