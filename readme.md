Reproductor de Medios en Raspberry Pi
Este proyecto es un reproductor de medios (imágenes y videos) diseñado para ejecutarse en una Raspberry Pi. La aplicación obtiene una lista de medios desde una API, los ordena por prioridad y los reproduce en pantalla completa. Además, se actualiza automáticamente cada 30 segundos para obtener nuevos medios.

Requisitos
Hardware
Raspberry Pi (preferiblemente Raspberry Pi 3, 4 o Zero con conectividad Wi-Fi).

Pantalla conectada a la Raspberry Pi.

Software
Python 3.x instalado.

Las siguientes bibliotecas de Python:

pygame

opencv-python

numpy

requests

Instalación
1. Clonar el repositorio
Si tienes el código en un repositorio, clónalo en tu Raspberry Pi:

bash
Copy
git clone https://github.com/Jesman12/jaison-viewer-v2.git
cd tu-repositorio
2. Instalar dependencias
Instala las bibliotecas necesarias usando pip:

bash
Copy
pip install pygame opencv-python numpy requests
Si estás en un entorno con restricciones (como Raspberry Pi OS con PEP 668), usa un entorno virtual:

bash
Copy
python3 -m venv mi_entorno
source mi_entorno/bin/activate
pip install pygame opencv-python numpy requests
3. Configurar la API
Asegúrate de que la URL de la API en la función obtener_medios sea correcta:

python
Copy
url = "https://api.domint.com.mx/rasp-web/api/rutas.php/get_media"
Ejecución
Para ejecutar la aplicación, usa el siguiente comando:

bash
Copy
python3 mi_aplicacion.py
La aplicación se ejecutará en pantalla completa y comenzará a reproducir los medios obtenidos desde la API.

Funcionamiento
1. Obtención de medios
La aplicación obtiene una lista de medios desde la API utilizando la función obtener_medios. Los medios pueden ser imágenes (.png, .jpg, etc.) o videos (.mp4, .avi, etc.).

2. Reproducción de medios
Imágenes: Las imágenes se descargan y muestran en pantalla completa usando pygame.

Videos: Los videos se descargan temporalmente, se reproducen usando opencv-python y se muestran en pantalla completa.

3. Actualización automática
Cada 30 segundos, la aplicación verifica si hay nuevos medios disponibles en la API y los reproduce según su prioridad.

4. Manejo de eventos
La aplicación detecta clics en la pantalla y los registra en la consola.

Si se cierra la ventana, la aplicación termina correctamente.

Estructura del código
Funciones principales
obtener_medios():

Realiza una solicitud HTTP GET a la API para obtener la lista de medios.

Devuelve una lista de medios en formato JSON.

mostrar_media_desde_url(screen, url, duracion):

Muestra una imagen o reproduce un video desde una URL.

Usa pygame para imágenes y opencv-python para videos.

Espera el tiempo especificado en duracion antes de continuar.

Bucle principal:

Obtiene y reproduce los medios en un bucle infinito.

Actualiza la lista de medios cada 30 segundos.

Configuración avanzada
Personalizar la API
Si deseas usar una API diferente, modifica la URL en la función obtener_medios:

python
Copy
url = "https://tu-api.com/endpoint"
Cambiar la duración de reproducción
La duración de cada medio se define en la lista de medios obtenida desde la API. Si deseas cambiar la duración predeterminada, modifica el valor de duracion en el bucle principal.

Ejecutar al inicio
Para que la aplicación se ejecute automáticamente al iniciar la Raspberry Pi, crea un servicio systemd:

Crea un archivo de servicio:

bash
Copy
sudo nano /etc/systemd/system/mi_aplicacion.service
Añade el siguiente contenido:

ini
Copy
[Unit]
Description=Reproductor de Medios
After=network.target

[Service]
ExecStart=/usr/bin/python3 /ruta/a/mi_aplicacion.py
WorkingDirectory=/ruta/a/tu-proyecto
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
Habilita y arranca el servicio:

bash
Copy
sudo systemctl daemon-reload
sudo systemctl enable mi_aplicacion.service
sudo systemctl start mi_aplicacion.service
Solución de problemas
1. Errores de conexión con la API
Verifica que la Raspberry Pi tenga conexión a Internet.

Asegúrate de que la URL de la API sea correcta.

2. Problemas con la reproducción de videos
Asegúrate de que opencv-python esté instalado correctamente.

Verifica que los videos estén en un formato compatible (.mp4, .avi, etc.).

3. La aplicación no se ejecuta en pantalla completa
Asegúrate de que la Raspberry Pi esté configurada para iniciar en modo gráfico.

Deshabilita el protector de pantalla:

bash
Copy
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
Añade las siguientes líneas:

bash
Copy
@xset s off
@xset -dpms
@xset s noblank
Licencia
Este proyecto está bajo la licencia MIT. Siéntete libre de usarlo y modificarlo según tus necesidades.

Contribuciones
Si deseas contribuir a este proyecto, ¡abre un issue o envía un pull request! Todas las contribuciones son bienvenidas.

Contacto
Si tienes alguna pregunta o sugerencia, no dudes en contactarme:

Nombre: [Salvador Emmanuel Galicia Zambrano]

Email: [em.ga.za.03@gmail.com]

GitHub: Salvador145

¡Gracias por usar este reproductor de medios! 😊