import numpy as np

class ruido():
    def __init__(self,image,metodo):

        self.image = image
        self.metodo = metodo

        if metodo=="Filtro medio":
            self.filtro_promedio()
        elif metodo=="Filtro mediano":
            self.filtro_mediana()
    
    def filtro_promedio(imagen):
        depth, height, width = imagen.shape
        imagen_filtrada = np.zeros_like(imagen)
        for x in range(1, depth - 2):
            for y in range(1, height - 2):
                for z in range(1, width - 2):

                    avg = 0
                    for dx in range(-1, 1):
                        for dy in range(-1, 1):
                            for dz in range(-1, 1):
                                avg = avg + imagen[x + dx, y + dy, z + dz]

                    imagen_filtrada[x + 1, y + 1, z + 1] = avg / 27

        return imagen_filtrada
    
    def filtro_mediana(imagen):
        depth, height, width = imagen.shape
        imagen_filtrada = np.zeros_like(imagen)
        for x in range(1, depth - 2):
            for y in range(1, height - 2):
                for z in range(1, width - 2):
                    neightbours = []
                    for dx in range(-1, 1):
                        for dy in range(-1, 1):
                            for dz in range(-1, 1):
                                neightbours.append(imagen[x + dx, y + dy, z + dz])

                    median = np.median(neightbours)
                    imagen_filtrada[x + 1, y + 1, z + 1] = median

        return imagen_filtrada