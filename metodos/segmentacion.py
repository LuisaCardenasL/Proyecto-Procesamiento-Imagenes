import numpy as np
from skimage import io

class segmentacion():
    def __init__(self,image,metodo,tau,num_iteraciones ):

        self.image = image
        self.metodo = metodo
        self.tau = tau
        self.num_iteraciones = num_iteraciones

        if metodo=="Umbralización":
            self.thresholding()
        elif metodo=="ISODATA":
            self.segmentation_isodata()
        elif metodo=="K-means":
            self.segmentation_kmeans()
        elif metodo=="Region Growing":
            self.region_growing()
    
    def thresholding(self):
        """
        Performs image segmentation using thresholding.
        """
        if self.image is not None:
            # Obtener la rebanada actual según la dimensión seleccionada
            layer = int(self.layer_scale.get())
            data = self.image.get_fdata()
            if self.selected_dimension == 'X':
                image_slice = data[layer, :, :]
            elif self.selected_dimension == 'Y':
                image_slice = data[:, layer, :]
            else:  # 'Z'
                image_slice = data[:, :, layer]

            # Definir el valor inicial del umbral (tau)
            tau = 127
            # Definir el valor de la tolerancia (Delta_tau)
            delta_tau = 1
            while True:
                # Aplicar el umbral actual
                segmented_image = (image_slice > tau).astype(int)
                # Calcular la media del píxel en el primer plano (foreground) y el fondo (background)
                mean_foreground = np.mean(image_slice[segmented_image == 1])
                mean_background = np.mean(image_slice[segmented_image == 0])
                # Calcular el nuevo umbral
                new_tau = 0.5 * (mean_foreground + mean_background)
                # Verificar si la diferencia entre el nuevo umbral y el anterior es menor que la tolerancia
                if abs(new_tau - tau) < delta_tau:
                    break
                # Actualizar el umbral
                tau = new_tau
            # Convertir la imagen binaria a uint8 (0 y 255)
            segmented_image = (segmented_image * 255).astype(np.uint8)

            self.segmented_image = segmented_image
            self.show_segmented_image()
            return segmented_image

    def segmentation_isodata(self):
        """
        Performs image segmentation using ISODATA thresholding.
        """
        if self.image is not None:
            # Obtener la rebanada actual según la dimensión seleccionada
            layer = int(self.layer_scale.get())
            data = self.image.get_fdata()
            if self.selected_dimension == 'X':
                image_slice = data[layer, :, :]
            elif self.selected_dimension == 'Y':
                image_slice = data[:, layer, :]
            else:  # 'Z'
                image_slice = data[:, :, layer]

            # Calcular el umbral ISODATA
            tau = threshold_isodata(image_slice)

            # Segmentar la imagen
            segmented_image = (image_slice > tau).astype(np.uint8) * 255

            self.segmented_image = segmented_image
            self.show_segmented_image()
            return segmented_image

    def segmentation_kmeans(self):
        """
        Performs image segmentation using K-means clustering.
        """
        if self.image is not None:
            # Obtener la rebanada actual según la dimensión seleccionada
            layer = int(self.layer_scale.get())
            data = self.image.get_fdata()
            if self.selected_dimension == 'X':
                image_slice = data[layer, :, :]
            elif self.selected_dimension == 'Y':
                image_slice = data[:, layer, :]
            else:  # 'Z'
                image_slice = data[:, :, layer]

            # Normalizar la imagen para que los valores estén entre 0 y 1
            normalized_image = image_slice / np.max(image_slice)

            # Convertir la imagen a un vector unidimensional
            flattened_image = normalized_image.flatten()

            # Aplicar K-medias con k=2
            kmeans = KMeans(n_clusters=2, random_state=0).fit(flattened_image.reshape(-1, 1))

            # Obtener las etiquetas de los clústeres
            labels = kmeans.labels_

            # Segmentar la imagen según las etiquetas obtenidas
            segmented_image = labels.reshape(normalized_image.shape) * 255

            self.segmented_image = segmented_image.astype(np.uint8)
            self.show_segmented_image()
            return segmented_image
        
    def region_growing(self):
        if self.image is not None:
            # Obtener la rebanada actual según la dimensión seleccionada
            layer = int(self.layer_scale.get())
            data = self.image.get_fdata()
            if self.selected_dimension == 'X':
                image_slice = data[layer, :, :]
            elif self.selected_dimension == 'Y':
                image_slice = data[:, layer, :]
            else:  # 'Z'
                image_slice = data[:, :, layer]

            # Elegir un punto de inicio (semilla) para el crecimiento de regiones
            seed = (image_slice.shape[0] // 2, image_slice.shape[1] // 2)

            # Lista para almacenar las coordenadas de los píxeles pertenecientes a la región
            region = [seed]
            # Lista para almacenar los píxeles ya visitados
            visited = []

            # Umbral para la comparación de intensidades
            threshold = 20

            while region:
                # Tomar el primer píxel de la región
                x, y = region.pop(0)

                # Verificar si el píxel ya ha sido visitado
                if (x, y) in visited:
                    continue

                # Marcar el píxel como visitado
                visited.append((x, y))

                # Verificar la intensidad del píxel con sus vecinos
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        # Coordenadas del vecino
                        neighbor_x = x + i
                        neighbor_y = y + j

                        # Verificar si el vecino está dentro de la imagen
                        if 0 <= neighbor_x < image_slice.shape[0] and 0 <= neighbor_y < image_slice.shape[1]:
                            # Verificar si el vecino no ha sido visitado y su intensidad es similar al punto de inicio
                            if (neighbor_x, neighbor_y) not in visited and abs(image_slice[x, y] - image_slice[neighbor_x, neighbor_y]) < threshold:
                                # Agregar el vecino a la región
                                region.append((neighbor_x, neighbor_y))

            # Crear una matriz de ceros con las mismas dimensiones que la imagen
            segmented_image = np.zeros_like(image_slice)
            # Asignar valor 255 a los píxeles de la región
            for x, y in visited:
                segmented_image[x, y] = 255

            self.segmented_image = segmented_image
            self.show_segmented_image()
            return segmented_image

    def show_segmented_image(self):
        if self.segmented_image is not None:
            plt.imshow(self.segmented_image, cmap='gray')
            plt.axis('off')
            plt.show()