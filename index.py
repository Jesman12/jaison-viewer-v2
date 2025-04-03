import cv2
import pygame
import time
import requests
import numpy as np
from datetime import datetime, timedelta
from io import BytesIO

# Función para obtener medios según reglas activas
def obtener_medios():
    try:
        url = "https://api.domint.com.mx/RASP-API/api/rutas.php/get_media"
        response = requests.get(url)

        # Verificar si la respuesta fue exitosa (código 200)
        if response.status_code == 200:
            return response.json()  # Devuelve la respuesta JSON correctamente
        else:
            print(f"Error en la solicitud: {response.status_code}")
            try:
                error_json = response.json()  # Intenta obtener el mensaje de error en JSON
                print(f"Mensaje de error del servidor: {error_json}")
            except ValueError:
                print(f"Respuesta del servidor: {response.text}")  # Si no es JSON, imprime el texto
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error en la conexión con el API: {e}")
        return []


def mostrar_media_desde_url(screen, url, duracion):
    try:
        print(f"Mostrando media desde URL: {url}")

        # Verificar si la URL es una imagen o un video
        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Obtener la imagen desde la URL
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Convertir el contenido de la imagen a un objeto de imagen de Pygame
                image_data = BytesIO(response.content)
                img = pygame.image.load(image_data)

                # Escalar la imagen para que se ajuste a la pantalla
                img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))

                # Mostrar la imagen en la pantalla
                screen.blit(img, (0, 0))
                pygame.display.flip()

                # Esperar la duración especificada antes de cambiar a la siguiente imagen
                inicio = time.time()
                while time.time() - inicio < duracion:
                    # Manejar eventos de Pygame (como clics o cierres)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return False  # Salir del bucle si se cierra la ventana
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            print("Clic detectado en la pantalla.")
            else:
                print(f"Error al cargar la imagen: {url}")

        elif url.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # Descargar el video desde la URL
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Guardar el video en un archivo temporal
                temp_video_path = "temp_video.mp4"
                with open(temp_video_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Cargar el video con OpenCV
                cap = cv2.VideoCapture(temp_video_path)

                # Obtener la tasa de fotogramas (FPS) del video
                fps = cap.get(cv2.CAP_PROP_FPS)

                # Calcular el tiempo de espera entre fotogramas
                delay = int(1000 / fps)  # Tiempo en milisegundos

                # Bucle para reproducir el video
                inicio = time.time()
                while time.time() - inicio < duracion:
                    ret, frame = cap.read()
                    if not ret:
                        break  # Salir si no hay más fotogramas

                    # Convertir el fotograma de OpenCV (BGR) a Pygame (RGB)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = np.rot90(frame)  # Rotar el fotograma si es necesario
                    frame = pygame.surfarray.make_surface(frame)

                    # Escalar el fotograma para que se ajuste a la pantalla
                    frame = pygame.transform.scale(frame, (screen.get_width(), screen.get_height()))

                    # Mostrar el fotograma en la pantalla
                    screen.blit(frame, (0, 0))
                    pygame.display.flip()

                    # Esperar el tiempo adecuado entre fotogramas
                    pygame.time.delay(delay)

                    # Manejar eventos de Pygame (como clics o cierres)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            cap.release()
                            return False  # Salir del bucle si se cierra la ventana
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            print("Clic detectado en la pantalla.")

                # Liberar el video y eliminar el archivo temporal
                cap.release()
                import os
                os.remove(temp_video_path)
            else:
                print(f"Error al cargar el video: {url}")

        else:
            print(f"Formato de archivo no soportado: {url}")

    except Exception as e:
        print(f"Error en la visualización del media: {e}")

    return True
    
# Bucle principal
import time
# Bucle principal
if __name__ == "__main__":
    # Inicializar Pygame y crear la ventana una sola vez
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.NOFRAME | pygame.FULLSCREEN)

    # Variable para controlar el bucle principal
    running = True

    # Variable para almacenar el tiempo de la última actualización
    ultima_actualizacion = time.time()

    while running:
        try:
            medios = obtener_medios()
            # Verificar si han pasado 30 segundos desde la última actualización
            if time.time() - ultima_actualizacion >= 30:
                print("Actualizando lista de medios...")
                medios = obtener_medios()
                ultima_actualizacion = time.time()

            if not medios:
                print("No hay medios disponibles en este momento.")
                time.sleep(10)  # Esperar antes de volver a intentar
            else:
                # Ordenar los medios por prioridad (de mayor a menor)
                medios_ordenados = sorted(medios, key=lambda x: x.get("prioridad", 0), reverse=True)

                # Bucle para reproducir las imágenes en ciclo
                for medio in medios_ordenados:
                    try:
                        device_id = medio["device_id"]
                        tipo_archivo = medio["tipo_archivo"]
                        src = medio["src"]
                        hora_inicio = medio["hora_inicio"]
                        hora_fin = medio["hora_fin"]
                        fecha_inicio = medio["fecha_inicio"]
                        fecha_fin = medio["fecha_inicio"]
                        duracion = medio["duracion"]  # Duración en segundos
                        prioridad = medio.get("prioridad", 0)  # Prioridad (por defecto 0 si no está presente)

                        print(f"Reproduciendo: {src} ({tipo_archivo}), Prioridad: {prioridad}, Duración: {duracion}s")
                        src_c = f"https://api.domint.com.mx/{src}"

                        # Mostrar la imagen o reproducir el video
                        running = mostrar_media_desde_url(screen, src_c, duracion)

                        # Verificar si han pasado 30 segundos desde la última actualización
                        if time.time() - ultima_actualizacion >= 30:
                            break  # Salir del bucle de reproducción para actualizar la lista

                    except KeyError as e:
                        print(f"Error: Falta un campo en el medio: {e}")
                    except Exception as e:
                        print(f"Error al procesar el medio: {e}")

        except Exception as e:
            print(f"Error al obtener medios: {e}")
            time.sleep(10)  # Esperar antes de volver a intentar

    # Cerrar Pygame correctamente al salir del bucle
    pygame.quit()