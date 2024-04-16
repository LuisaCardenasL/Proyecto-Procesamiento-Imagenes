import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageDraw, ImageTk
from ventanas.preprocesamiento import preprocesamiento
from ventanas.segmentacion_ventana import segmentacion_ventana
from ventanas.histograma import histograma

class VentanaInicial(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Procesamiento de imagenes")
        self.etiqueta = Label(self, text="Procesamiento de imagenes")
        self.etiqueta.pack()
        self.etiqueta.config(font=('Arial', 44))
        self.etiqueta.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.etiqueta.config(bg="grey")

        # Ajustar el ancho de la ventana
        self.update_idletasks()  # Actualizar la ventana antes de obtener el ancho requerido
        titulo_ancho = self.etiqueta.winfo_reqwidth()
        ventana_ancho = titulo_ancho + 20  # Ajustar el ancho de la ventana según tus necesidades

        # Definir los componentes de la interfaz
        self.botonPreprocesamiento = Button(self, text="Pre-procesamiento", command=self.VentanaPreprocesamiento)
        self.botonPreprocesamiento.pack()
        self.botonPreprocesamiento.config(bg="white")
        self.botonPreprocesamiento.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.botonSegmentacion = Button(self, text="Segmentación", command=self.VentanaSegmentacion)
        self.botonSegmentacion.pack()
        self.botonSegmentacion.config(bg="white")
        self.botonSegmentacion.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.botonHistograma = Button(self, text="Histograma", command=self.VentanaHistograma)
        self.botonHistograma.pack()
        self.botonHistograma.config(bg="white")
        self.botonHistograma.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.geometry(f"{ventana_ancho}x550")  # Ajustar el ancho de la ventana
        self.config(bg="grey")
        self.mainloop()

    def VentanaPreprocesamiento(self):
        ventana_image = preprocesamiento(self)

    def VentanaSegmentacion(self):
        ventana_image = segmentacion_ventana(self)

    def VentanaHistograma(self):
        ventana_image = histograma(self)

if __name__ == "__main__":
    app = VentanaInicial()