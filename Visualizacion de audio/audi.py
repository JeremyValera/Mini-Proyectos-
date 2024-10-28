import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

# Constantes
CHUNK = 1024 * 2            # Muestras por marco
FORMAT = pyaudio.paInt16    # Formato de audio (bytes por muestra)
CHANNELS = 1                # Canal único para el micrófono 
RATE = 44100                # Muestras por segundo

# Crear figura y ejes en matplotlib 
fig, ax = plt.subplots(1, figsize=(15, 7))

# Instancia de la clase PyAudio 
p = pyaudio.PyAudio()

# Objeto de transmisión para obtener datos del micrófono
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK,
)

# Variable para graficar
x = np.arange(0, 2 * CHUNK, 2)

# Crear un objeto de línea con datos aleatorios
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# Formateo básico para los ejes
ax.set_title('FORMATO DE OLA DE AUDIO')
ax.set_xlabel('muestras')
ax.set_ylabel('volumen')
ax.set_ylim(-128, 127)  # Ajustado para datos de 8 bits con signo
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-128, 0, 127])

# Mostrar la gráfica
plt.show(block=False)
print('transmisión iniciada')

# Para medir la tasa de cuadros
frame_count = 0
start_time = time.time()

try:
    while True:
        # Datos binarios
        data = stream.read(CHUNK)
        # Convertir los datos a enteros, hacer un arreglo np y luego ajustar por 127
        data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
        # Crear arreglo np y ajustar por 128
        data_np = np.array(data_int, dtype='b')[::2]  # Ajuste corregido
        line.set_ydata(data_np)
        # Actualizar el lienzo de la figura
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
except TclError:
    # Calcular la tasa de cuadros promedio
    frame_rate = frame_count / (time.time() - start_time)

    print('transmisión detenida')
    print('tasa de cuadros promedio = {:.0f} FPS'.format(frame_rate))
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()  # Cerrar correctamente la instancia de PyAudio
