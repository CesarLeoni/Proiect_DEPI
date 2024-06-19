import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import librosa
import librosa.display
from funcs import merge_wav_files


def denoise_audio(input_file, output_file, threshold=0.1, frame_length=4*1024, hop_length=512):
    # Read audio file
    data, samplerate = sf.read(input_file)

    # Ensure mono audio
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Perform Short-Time Fourier Transform (STFT)
    stft_data = librosa.stft(data, n_fft=frame_length, hop_length=hop_length)
    magnitude, phase = np.abs(stft_data), np.angle(stft_data)

    # Compute power spectral density (PSD)
    psd = magnitude ** 2

    # Apply threshold to PSD to create a mask
    mask = psd > threshold

    # Apply mask to the magnitude
    cleaned_magnitude = magnitude * mask

    # Reconstruct the denoised STFT
    cleaned_stft = cleaned_magnitude * np.exp(1j * phase)

    # Perform Inverse Short-Time Fourier Transform (ISTFT)
    denoised_signal = librosa.istft(cleaned_stft, hop_length=hop_length)

    # Save the cleaned audio to a new file
    sf.write(output_file, denoised_signal, samplerate)

    # Plot the results
    fig, ax = plt.subplots(3, 1, figsize=(15, 15))

    ax[0].plot(data, label="Original Signal")
    ax[0].legend()

    ax[1].plot(librosa.amplitude_to_db(magnitude, ref=np.max), label='Original Spectrogram')
    ax[1].legend()

    ax[2].plot(denoised_signal, label="Denoised Signal")
    ax[2].legend()

    plt.show()


if __name__ == "__main__":
    input_file = 'files/input_audio.wav'  # Change this to your input file path
    noise_file = 'files/noise1.wav'
    combined_file = 'files/combined_audio.wav'
    merge_wav_files(input_file,noise_file,combined_file)

    output_file = 'files/denoised_audio.wav'  # Change this to your desired output file path
    denoise_audio(combined_file, output_file, threshold=0.13)
