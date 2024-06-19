import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
from queue import Queue, Empty

# Parameters
CHUNK = 1024  # Number of audio samples per frame
RATE = 44100  # Sampling rate (samples per second)
RUN_TIME = 10  # Time to run in seconds

# Queue to hold audio data
q = Queue()


# Function to capture audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata[:, 0].copy())


# Open a stream with the above parameters
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=RATE, blocksize=CHUNK)
stream.start()


# Function to update the plot
def update(frame):
    try:
        data = q.get_nowait()
    except Empty:
        return line,

    # Compute FFT
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_data), 1 / RATE)

    # Update the line with the new FFT data
    line.set_ydata(np.abs(fft_data)[:CHUNK // 2])
    return line,


# Set up the plot
fig, ax = plt.subplots()
x = np.fft.fftfreq(CHUNK, 1 / RATE)
x = x[:CHUNK // 2]
line, = ax.plot(x, np.zeros(CHUNK // 2))
ax.set_ylim(0, 2)
ax.set_xlim(20, RATE / 2)
ax.set_xscale('log')
ax.set_title('Frequency Spectrum')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude')


# Function to stop the stream after RUN_TIME seconds
def stop_stream():
    stream.stop()
    stream.close()
    plt.close()


# Start a timer to stop the stream
timer = threading.Timer(RUN_TIME, stop_stream)
timer.start()

# Start the animation
ani = FuncAnimation(fig, update, interval=50)
plt.show()

# Close the stream when done
stream.stop()
stream.close()
