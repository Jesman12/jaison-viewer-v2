import cv2
import pygame
import time
import requests
import numpy as np
from datetime import datetime, timedelta
from io import BytesIO
import os

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


def mostrar_media_desde_url(screen, url, duracion, escalado='original', pos_x=0, pos_y=0):
    try:
        print(f"Mostrando media desde URL: {url} - Escalado: {escalado} - Posición: ({pos_x}, {pos_y})")

        # Obtener dimensiones de pantalla una sola vez
        screen_width, screen_height = screen.get_size()
        
        # Verificar el tipo de archivo por extensión
        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Manejo de imágenes
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                original_img = pygame.image.load(image_data)
                img_width, img_height = original_img.get_size()
                aspect_ratio = img_width / img_height
                screen_aspect = screen_width / screen_height

                # Aplicar escalado según parámetro
                if escalado == 1:
                    img = original_img
                    display_pos = (pos_x, pos_y)
                elif escalado == 2:
                    img = pygame.transform.scale(original_img, (screen_width, screen_height))
                    display_pos = (0, 0)
                elif escalado == 3 or 4:
                    if aspect_ratio > screen_aspect:
                        new_width = screen_width
                        new_height = int(new_width / aspect_ratio)
                    else:
                        new_height = screen_height
                        new_width = int(new_height * aspect_ratio)
                    img = pygame.transform.scale(original_img, (new_width, new_height))
                    display_pos = ((screen_width - new_width) // 2, (screen_height - new_height) // 2)
                else:
                    img = original_img
                    display_pos = (pos_x, pos_y)

                # Mostrar imagen
                inicio = time.time()
                clock = pygame.time.Clock()
                while time.time() - inicio < duracion:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            print("Clic detectado")

                    screen.fill((0, 0, 0))
                    screen.blit(img, display_pos)
                    pygame.display.flip()
                    clock.tick(30)

        elif url.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # Manejo de videos
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                temp_video_path = "temp_video.mp4"
                with open(temp_video_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                cap = cv2.VideoCapture(temp_video_path)
                video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                video_aspect = video_width / video_height
                fps = cap.get(cv2.CAP_PROP_FPS)
                delay = max(1, int(1000 / fps)) if fps > 0 else 30

                inicio = time.time()
                clock = pygame.time.Clock()
                while time.time() - inicio < duracion:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = pygame.surfarray.make_surface(frame)

                    # Aplicar escalado al video
                    if escalado == 'original':
                        scaled_frame = frame
                        frame_pos = (pos_x, pos_y)
                    elif escalado == 'extendido':
                        scaled_frame = pygame.transform.scale(frame, (screen_width, screen_height))
                        frame_pos = (0, 0)
                    elif escalado == 'fit':
                        if video_aspect > screen_aspect:
                            new_width = screen_width
                            new_height = int(new_width / video_aspect)
                        else:
                            new_height = screen_height
                            new_width = int(new_height * video_aspect)
                        scaled_frame = pygame.transform.scale(frame, (new_width, new_height))
                        frame_pos = ((screen_width - new_width) // 2, (screen_height - new_height) // 2)
                    else:
                        scaled_frame = frame
                        frame_pos = (pos_x, pos_y)

                    screen.fill((0, 0, 0))
                    screen.blit(scaled_frame, frame_pos)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            cap.release()
                            os.remove(temp_video_path)
                            return False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            print("Clic detectado")

                    clock.tick(fps if fps > 0 else 30)

                cap.release()
                os.remove(temp_video_path)
            else:
                print(f"Error al cargar video: {url}")

        else:
            print(f"Formato no soportado: {url}")

    except Exception as e:
        print(f"Error en mostrar_media_desde_url: {str(e)}")
        import traceback
        traceback.print_exc()

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
                        escalado = medio["escalado_id"]
                        x = medio["x"]
                        y = medio["y"]

                        print(f"Reproduciendo: {src} ({tipo_archivo}), Prioridad: {prioridad}, Duración: {duracion}s")
                        src_c = f"https://api.domint.com.mx/{src}"

                        # Mostrar la imagen o reproducir el video
                        running = mostrar_media_desde_url(
                                                    screen, 
                                                    src_c, 
                                                    duracion,
                                                    escalado=escalado,  # 'original', 'extendido' o 'fit'
                                                    pos_x=x,           # Posición X (solo para 'original')
                                                    pos_y=y            # Posición Y (solo para 'original')
                                                )

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