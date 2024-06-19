import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import wavfile
from scipy.signal import butter, lfilter

sns.set_style("darkgrid")
sns.set_context("talk")

def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Read the audio file (assuming a .wav file)
samplerate, data = wavfile.read('files/input_audio.wav')

# Ensure mono audio by averaging channels if necessary
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Define filter parameters
cutoff_freq = 1000  # Adjust the cutoff frequency as needed
order = 6

# Apply the low-pass filter
filtered_data = lowpass_filter(data, cutoff_freq, samplerate, order)

# Save the filtered audio
wavfile.write('files/output_audio.wav', samplerate, filtered_data.astype(np.int16))

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(15, 10))

# Original signal
axs[0].plot(data)
axs[0].set_title('Original Signal')

# Filtered signal
axs[1].plot(filtered_data)
axs[1].set_title('Filtered Signal')

plt.show()
