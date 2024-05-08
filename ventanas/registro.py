import tkinter as tk
from tkinter import Label, Button, filedialog, Entry
import nibabel as nib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from metodos.registro import Registro
from tkinter import ttk
import os
import numpy as np
import shutil

class registro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro")
        self.config(bg="grey")
        self.geometry("1500x610")

        self.titulo = tk.Label(self, text="NRL-DSKT")
        self.titulo.pack()
        self.titulo.config(font=('Times new roman', 35))
        self.titulo.place(x=600, y=30)
        self.titulo.config(bg="grey")

        self.subtitulo = tk.Label(self, text="Registro - escoge una imagen FLAIR.nii")
        self.subtitulo.pack()
        self.subtitulo.config(font=('Times new roman', 15))
        self.subtitulo.place(x=100, y=75)
        self.subtitulo.config(bg="grey")

        self.subtitulo2 = tk.Label(self, text="Resultado")
        self.subtitulo2.pack()
        self.subtitulo2.config(font=('Times new roman', 15))
        self.subtitulo2.place(x=1010, y=75)
        self.subtitulo2.config(bg="grey")

        self.botonCargar = Button(
            self, text="Cargar imagen", command=self.cargar_imagen)
        self.botonCargar.pack()
        self.botonCargar.place(x=420, y=570)

        # Crear un lienzo para mostrar la imagen
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.place(x=100, y=100, width=450, height=450)

        # Crear un lienzo para mostrar el histograma
        self.canvasResultado = tk.Canvas(self, bg='white')
        self.canvasResultado.place(x=1010, y=100, width=450, height=450)
        
        # Seleccionar Ejes
        self.variable = tk.StringVar()
        self.variable.set("Seleccionar")
        self.labelAxis = tk.Label(
            self, text="Movimientos de ejes: ", bg="grey", fg="black")
        self.labelAxis.place(x=580, y=100)
        self.labelAxis.config(font=('Times new roman', 12))

        self.w = tk.OptionMenu(self, self.variable, 'Eje x',
                               'Eje y', 'Eje z', command=self.ejes)
        self.w.place(x=740, y=100)
        
        # Seleccionar ruido
        self.registro_m = tk.StringVar()
        self.registro_m.set("Seleccionar")
        self.labelMethod1 = tk.Label(
            self, text="Que desea escoger : ", bg="grey", fg="black")
        self.labelMethod1.place(x=580, y=210)
        self.labelMethod1.config(font=('Times new roman', 12))

        self.opc1 = tk.OptionMenu(self, self.registro_m, "Registro",
                                  "Calcular volumen", command=self.seleccionar_registro)
        self.opc1.place(x=730, y=210)
    
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

    def seleccionar_registro(self, *args):

        if self.registro_m.get() == 'Registro' and self.rutaImage != "":

            self.btnRegistro = tk.Button(self, text="Hacer registro", bg="white",
                                 borderwidth=0, command=lambda: self.confirmacion("1"))
            self.btnRegistro.place(x=1010, y=570)
            self.canvasSegmentacion = tk.Canvas(
            self, width=300, height=300, bg="grey", highlightbackground="black", highlightthickness=2)
            self.canvasSegmentacion.pack()
            self.canvasSegmentacion.place(x=600, y=250)

            self.botonCargarSegundaImagen = Button(
            self, text="Cargar imagen", command=self.cargar_imagenSecundaria)
            self.botonCargarSegundaImagen.pack()
            self.botonCargarSegundaImagen.place(x=790, y=570)

            self.variable2 = tk.StringVar()
            self.variable2.set("Seleccionar")
            self.w2 = tk.OptionMenu(self, self.variable2, 'Eje x',
                                    'Eje y', 'Eje z', command=self.ejes2)
            self.w2.place(x=905, y=250)
            self.btnVolumen.destroy()
            self.vol.destroy()
            self.EntryVolumen.destroy()

        if self.registro_m.get() == 'Calcular volumen' and self.rutaImage != "":

            self.btnVolumen = tk.Button(self, text="Calcular volumen", bg="white", borderwidth=0, command=lambda: self.confirmacion("2"))
            self.btnVolumen.place(x=1010, y=570)
            self.w2.destroy()
            self.botonCargarSegundaImagen.destroy()
            self.canvasSegmentacion.destroy()

    def click2(self, event):
        if self.ax2.contains(event)[0]:
            x = int(event.xdata)
            y = int(event.ydata)

    def iniciar2(self):
        self.canvasSegmentacion.delete("all")  # Use self.canvasSegmentacion instead of self.canvasSegmentacion
        self.fig2, self.ax2 = plt.subplots()
        self.ax2.imshow(self.imagen2[:, :, 0])
        self.canvas_widget2 = FigureCanvasTkAgg(self.fig2, self.canvasSegmentacion)  # Use self.canvasImagen
        self.canvas_widget2.draw()
        self.canvas_widget2.get_tk_widget().place(x=0, y=0, width=300, height=300)
        cid = self.fig2.canvas.mpl_connect('button_press_event', self.click2)  # Use self.fig2.canvas instead of self.fig2.canvasSegmentacion
                
    def cargar_imagenSecundaria(self):

        initial_dir = "Resources/images"
        self.file_path2 = filedialog.askopenfilename(initialdir=initial_dir)
        self.rutaImage2 = self.file_path2
        self.img2 = nib.load(self.rutaImage2)
        self.imagen2 = self.img2.get_fdata()
        self.iniciar2()

    def escala2(self, *args):
        if self.rutaImage2 != "":
            self.canvasSegmentacion.delete("all")
            if self.variable2.get() == 'Eje x':
                self.ax2.imshow(self.imagen2[self.escalaEjes2.get(), :, :])
            elif self.variable2.get() == 'Eje y':
                self.ax2.imshow(self.imagen2[:, self.escalaEjes2.get(), :])
            elif self.variable2.get() == 'Eje z':
                self.ax2.imshow(self.imagen2[:, :, self.escalaEjes2.get()])
            else:
                self.ax2.imshow(self.imagen2[:, :, 0])
            self.canvas_widget2.draw()
        else:
            pass

    def ejes2(self, *args):

        if self.variable2.get() == 'X' and self.rutaImage2 != "":
            self.size2 = (self.imagen2.shape[0])-1
        elif self.variable2.get() == 'Y' and self.rutaImage2 != "":
            self.size2 = (self.imagen2.shape[1])-1
        elif self.variable2.get() == 'Z' and self.rutaImage2 != "":
            self.size2 = (self.imagen2.shape[2])-1
        else:
            self.size2 = 10
        self.escalaEjes2 = tk.Scale(self, label=self.variable2.get(
        ), from_=0, to=self.size2, orient='vertical', bg="grey", fg="black", command=self.escala2)
        self.escalaEjes2.place(x=910, y=350)     

    def seleccionar_imagen(self, event):
        imagen_seleccionada = self.dropdown_contenido.get()
        print("imagen seleccionada: ", imagen_seleccionada)
        if imagen_seleccionada:
            self.selected_image_path = os.path.join(
                "./resources/resultadosRegistros", imagen_seleccionada)

            # Load the NIfTI image using nibabel
            img = nib.load(self.selected_image_path)
            data = img.get_fdata()

            # Display the image on the canvas
            plt.figure(figsize=(4.5, 4.5))
            plt.imshow(data[:,:,0])
            plt.axis('on')

            if hasattr(self, "canvas_fig_agg"):
                self.canvas_fig_agg.get_tk_widget().destroy()
                del self.canvas_fig_agg

            self.canvas_fig_agg = FigureCanvasTkAgg(plt.gcf(), master=self.canvasResultado)
            self.canvas_fig_agg.draw()
            self.canvas_fig_agg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def guardar_imagen(self):
        if self.selected_image_path:
            # Get the name entered by the user in the text entry box
            nombre_archivo = self.entryNombre.get()

            # Check if a file name is entered
            if nombre_archivo:
                # Open the file dialog to select the destination folder
                directorio_destino = filedialog.askdirectory()

                # Check if a folder is selected
                if directorio_destino:
                    # Construct the save path using the destination folder and the file name
                    ruta_guardado = os.path.join(directorio_destino, nombre_archivo + ".nii.gz")

                    # Copy the selected image to the destination folder
                    shutil.copyfile(self.selected_image_path, ruta_guardado)
                    print("Imagen guardada en:", ruta_guardado)
                else:
                    print("No se seleccionó una carpeta de destino.")
            else:
                print("Por favor, ingrese un nombre de archivo.")
        else:
            print("Por favor, seleccione una imagen del dropdown.")
    
    def confirmacion(self, metodo):

        if metodo == "1":
            self.imagen = Registro.registro(self.rutaImage, self.rutaImage2)
            self.escala2()
            
            self.current_image = None  # Track the currently displayed image

            ruta_carpeta = "./resources/resultadosRegistros"
            contenido_carpeta = os.listdir(ruta_carpeta)

            self.labelImagenes = tk.Label(self, text="Selecciona el registro")
            self.labelImagenes.pack()
            self.labelImagenes.config(font=('Times new roman', 10))
            self.labelImagenes.place(x=1100, y=70)
            self.labelImagenes.config(bg="grey")

            self.dropdown_contenido = ttk.Combobox(self, values=contenido_carpeta)
            self.dropdown_contenido.bind("<<ComboboxSelected>>", self.seleccionar_imagen)
            self.dropdown_contenido.pack()
            self.dropdown_contenido.place(x=1250, y=70)

            # Almacenar imagen generada
            self.labelNombre = Label(self, text="Nombre de la imagen:" , bg="grey", fg="black")
            self.labelNombre.pack()
            self.labelNombre.config(font=('Times new roman', 10))
            self.labelNombre.place(x=1100, y=570)

            self.entryNombre = Entry(self)
            self.entryNombre.pack()
            self.entryNombre.place(x=1250, y=570)

            self.botonGuardar = Button(self, text="Guardar imagen", command=self.guardar_imagen)
            self.botonGuardar.pack()
            self.botonGuardar.place(x=1380, y=570)

        elif metodo == "2":
            self.imagen = self.img.get_fdata()
            self.resultado_volumen = Registro.calcular_volumen(self.imagen)
            self.escala()

            # label
            self.vol = tk.Label(self, text="El volumen es: ")
            self.vol.pack()
            self.vol.config(font=('Times new roman', 15))
            self.vol.place(x=100, y=570)
            self.vol.config(bg="grey")

            # Crear y ubicar el campo de entrada
            self.EntryVolumen = tk.Entry(self)
            self.EntryVolumen.pack()
            self.EntryVolumen.place(x=250, y=570)

            # Mostrar el valor del volumen en un campo de entrada
            self.EntryVolumen.delete(0, tk.END)  # Borrar el contenido actual del Entry
            self.EntryVolumen.insert(0, str(self.resultado_volumen))  # Insertar el valor del volumen en el Entry

            # Mostrar el valor del volumen en una etiqueta
            self.labelVolumen= tk.Label(self)
            self.labelVolumen.config(text="Volumen: {}".format(self.resultado_volumen))