import wave
import numpy as np
import struct
import matplotlib.pyplot as plt

def merge_wav_files(file1_path, file2_path, output_path):
    # Function to read a WAV file
    def read_wav(file_path):
        with wave.open(file_path, 'r') as wav_file:
            params = wav_file.getparams()
            frames = wav_file.readframes(params.nframes)
            signal = np.frombuffer(frames, dtype=np.int16)
        return params, signal

    # Function to write a WAV file
    def write_wav(file_path, params, signal):
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setparams(params)
            frames = struct.pack('<' + ('h' * len(signal)), *signal)
            wav_file.writeframes(frames)

    # Read the WAV files
    params1, signal1 = read_wav(file1_path)
    params2, signal2 = read_wav(file2_path)

    # Make sure both signals have the same length
    min_length = min(len(signal1), len(signal2))
    signal1 = signal1[:min_length]
    signal2 = signal2[:min_length]

    # Merge the signals by adding them
    merged_signal = signal1 + signal2/30

    # Normalize the merged signal to prevent clipping
    merged_signal = np.int16(merged_signal / np.max(np.abs(merged_signal)) * 32767)

    # Write the merged signal to a new WAV file
    write_wav(output_path, params1, merged_signal)

    print(f"Merged WAV file saved as '{output_path}'")

# Usage example:
#merge_wav_files('file1.wav', 'file2.wav', 'merged_file.wav')

def plot_noisy_signals(original, noise, noisy,psd,mag,clean_psd,regenerated,style,err,message):
    time_step = 0.001


    plt.style.use(style)

    fig = plt.figure(figsize=(13, 8))
    fig.suptitle(message+str(err),fontweight='bold')

    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, (3, 4))

    ax1.plot(original)
    ax1.set_title("original")
    ax1.set_xlim(200, 400)  # Set x-axis limits to zoom in

    ax2.plot(noise)
    ax2.set_title("noise")
    ax2.set_xlim(200, 400)  # Set x-axis limits to zoom in

    ax3.plot(noisy, label="noisy")
    ax3.plot(original, label="original")
    ax3.set_xlim(200, 400)  # Set x-axis limits to zoom in

    plt.legend()
    plt.show()


    N = len(original)

    n = int(np.floor(N / 2))  # frequencies till N/2 can be used for this processing
    new_freqs = (1 / (N * time_step)) * np.arange(N)

    fig, ax = plt.subplots(3, 1, figsize=(10, 7))
    fig.suptitle(message + str(err), fontweight='bold')

    ax[0].plot(new_freqs[:n], psd[:n], 'g', label='PSD')
    ax[1].plot(new_freqs[:n], mag[:n], 'b', label="magnitude")
    ax[2].plot(new_freqs[:n], clean_psd[:n], 'y', label='cleaned PSD')

    fig.legend()
    fig.show()


    fig, ax = plt.subplots(3, 1, figsize=(15, 15))
    fig.suptitle(message + str(err), fontweight='bold',fontsize='large')

    ax[0].plot(noisy, label="noisy signal")
    ax[0].plot(original, label="original signal")
    ax[0].legend()
    ax[0].set_xlim(200, 400)  # Set x-axis limits to zoom in

    ax[1].plot(noisy, label="noisy signal")
    ax[1].plot(regenerated, label="recovered signal")
    ax[1].legend()
    ax[1].set_xlim(200, 400)  # Set x-axis limits to zoom in

    ax[2].plot(original, label="original signal")
    ax[2].plot(regenerated, label="recovered signal")
    ax[2].legend()
    ax[2].set_xlim(200, 400)  # Set x-axis limits to zoom in

    plt.show()