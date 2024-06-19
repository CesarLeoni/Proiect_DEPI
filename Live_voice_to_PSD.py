import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyaudio

# Constants
CHUNK_SIZE = 1024 * 4 # Number of audio samples per frame
FORMAT = pyaudio.paInt16 # 16-bit audio format
CHANNELS = 1
RATE = 44100 # Sample rate (44.1 kHz)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(
format=FORMAT,
channels=CHANNELS,
rate=RATE,
input=True,
output=True,
frames_per_buffer=CHUNK_SIZE
)

# Set up the main window
root = tk.Tk()
root.title("Real-Time Audio Plot")

fig = plt.figure(figsize=(10,10))

ax1 = fig.add_subplot(2,2,(1,2))
ax2 = fig.add_subplot(2,2,(3,4))

ax1.set_ylim(-2**15 ,2**15)
ax2.set_ylim(0,2*1e9)

ax1.set_title('Audio Signal')
ax2.set_title('Power Spectral Density')

m = int(np.floor(CHUNK_SIZE/10))

line1, = ax1.plot(range(CHUNK_SIZE),range(CHUNK_SIZE))
line2, = ax2.plot(range(m),range(m))

# Embed the plot in the tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def update_plot():
    try:
        bit_data = stream.read(CHUNK_SIZE)
        data_int = np.frombuffer(bit_data, dtype=np.int16)

# Copiază codul
        f_hat = np.fft.fft(data_int, CHUNK_SIZE)
        psd = (f_hat * np.conjugate(f_hat) / CHUNK_SIZE).real

        line1.set_ydata(data_int)
        line2.set_ydata(psd[:m])

        canvas.draw()
    except Exception as e:
        print(e)
    root.after(10, update_plot)

# Start the plot update loop
root.after(10, update_plot)

# Start the t# Clean upkinter main loop
root.mainloop()

stream.stop_stream()
stream.close()
p.terminate()