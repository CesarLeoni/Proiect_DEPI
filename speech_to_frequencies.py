import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100  # Sampling rate (samples per second)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream with the above parameters
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Function to update the plot
def update(frame):
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    # Compute FFT
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_data))
    # Update the line with the new FFT data
    line.set_ydata(np.abs(fft_data)[:CHUNK // 2])
    return line,

# Set up the plot
fig, ax = plt.subplots()
x = np.fft.fftfreq(CHUNK, 1/RATE)
x = x[:CHUNK // 2]
line, = ax.plot(x, np.random.rand(CHUNK // 2))
ax.set_ylim(0, 255)
ax.set_xlim(20, RATE / 2)
ax.set_xscale('log')
ax.set_title('Frequency Spectrum')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude')

# Start the animation
ani = FuncAnimation(fig, update, interval=50)
plt.show()

# Close the stream when done
stream.stop_stream()
stream.close()
p.terminate()
