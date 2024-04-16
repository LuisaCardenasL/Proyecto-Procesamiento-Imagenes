import numpy as np
from scipy.signal import find_peaks
import scipy.stats as stats

class intensidad():
    def __init__(self,image,metodo):

        self.image = image
        self.metodo = metodo
        
        if metodo=="Reescala":
            self.reescala()
        elif metodo=="z-score":
            self.z_score()
        elif metodo=="Coincidencia de histograma":
            self.histograma()
        elif metodo=="Raya blanca":
            self.white_stripe()
    
    def reescala(imagen):
        valor_minimo = imagen.min()
        valor_maximo = imagen.max()

        imagen_reescalada = (imagen - valor_minimo) / (valor_maximo - valor_minimo)
        return imagen_reescalada

    def z_score(imagen):
        media = imagen[imagen > 10].mean()
        desviacion_estandar = imagen[imagen > 10].std()
        imagen_zscore = (imagen - media) / desviacion_estandar 
        return imagen_zscore

    def histograma(flair_image,imagen):
        k=3
        # Reshape the data arrays to 1D arrays
        referencia = flair_image.flatten()
        entrada = imagen.flatten()


        imagen_referencia = np.percentile(referencia, np.linspace(0, 100, k))
        tranformar_imagen = np.percentile(entrada, np.linspace(0, 100, k))

        combinacion = np.interp(entrada, tranformar_imagen, imagen_referencia)


        resultado = combinacion.reshape(imagen.shape)

        return resultado
    
    def white_stripe(imagen):
        # Calcula el histograma
        hist, bins = np.histogram(imagen.ravel(), bins="auto")

        # Encuentra los picos del histograma
        picos, _ = find_peaks(hist)

        # Si hay al menos tres picos, utiliza el valor moda entre el segundo y el tercer pico como divisor
        if len(picos) >= 3:
            ultimo_pico = picos[-1]
            #segundo_ultimo_pico = picos[-2]
            indice_inicio = max(0, ultimo_pico - 10)
            rango_ultimo_pico = range(int(bins[indice_inicio]), int(bins[-1]) + 1)
            #rango_segundo_ultimo_pico = range(int(bins[segundo_ultimo_pico]), int(bins[ultimo_pico])+1)
            moda, _ = stats.mode(hist[rango_ultimo_pico])
            divisor = moda[0]
        # Si hay menos de tres picos, utiliza el valor moda de todo el histograma como divisor
        else:
            moda, _ = stats.mode(hist)
            divisor = moda[0]

        # Divide la imagen por el valor divisor
        #hist_normalizado = hist / divisor
        imagen_ws = imagen / divisor

        return imagen_ws