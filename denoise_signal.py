import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

#FIRST TRY
#does denoising but for the entire signel, so it
#outputs a strange sound
#in further versions i will try to do denoising
#on frames to see if that works

def denoise_audio(input_file, output_file, threshold=100):
    # Read audio file
    data, samplerate = sf.read(input_file)

    # Ensure mono audio
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    N = len(data)
    time_step = 1.0 / samplerate

    # Compute FFT
    f_hat = np.fft.fft(data)
    n = int(np.floor(N / 2))

    new_freqs = (1 / (N * time_step)) * np.arange(N)
    psd = (f_hat * np.conjugate(f_hat) / N).real
    mag = (np.abs(f_hat) / N).real

    # Clean based on threshold
    threshold_idxs = (psd > threshold)
    cleaned_psd = psd * threshold_idxs
    cleaned_f_hat = f_hat * threshold_idxs

    # Regenerate signal based on cleaned spectrum using inverse Fourier
    regen_signal = np.fft.ifft(cleaned_f_hat).real

    # Save the cleaned audio to a new file
    sf.write(output_file, regen_signal, samplerate)

    # Plot the results
    fig, ax = plt.subplots(3, 1, figsize=(15, 15))

    ax[0].plot(data, label="original signal")
    ax[0].legend()

    ax[1].plot(np.arange(N)[:n], psd[:n], 'g', label='Original PSD')
    ax[1].plot(np.arange(N)[:n], cleaned_psd[:n], 'b', label='Cleaned PSD')
    ax[1].legend()

    ax[2].plot(regen_signal, label="recovered signal")
    ax[2].legend()

    plt.show()


if __name__ == "__main__":
    input_file = 'files/input_audio.wav'  # Change this to your input file path
    output_file = 'files/output_audio.wav'  # Change this to your desired output file path
    denoise_audio(input_file, output_file,threshold=0.01)
