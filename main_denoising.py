import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from mightypy.make import sine_wave_from_sample, sine_wave_from_timesteps
import random
from funcs import plot_noisy_signals

NOISE_MULTIPLIER = 3.5
THRESHOLD = 170  # threshold for getting components

time_step = 0.0005

MinMSE = 1000
MaxMSE = 0

for i in range(1,1000):
    # GENERATING NOISY SIGNAL
    # amplitude parameter can be added , default is 1
    freqs = np.random.randint(1, 101, size=4)
    wave1, time1, freqs1  = sine_wave_from_timesteps(freqs[0], time_step=time_step)
    wave2, time2, freqs2  = sine_wave_from_timesteps(freqs[1], time_step=time_step)
    wave3, time3, freqs3 = sine_wave_from_timesteps(freqs[2], time_step=time_step)
    wave4, time4, freqs4 = sine_wave_from_timesteps(freqs[3], time_step=time_step)
    #we can increase complexity by adding or reducing the waves that compose the original signal

    original_signal = wave1 + wave2 + wave3 + wave4

    N = len(original_signal)
    # print(N)

    noise = NOISE_MULTIPLIER * np.random.randn(N)

    noisy_signal = original_signal + noise  # adding random noise here

    # CALCULATING FFT - FOURIER FAST TRANSFORM
    f_hat = np.fft.fft(noisy_signal, N)
    n = int(np.floor(N / 2))  # frequencies till N/2 can be used for this processing

    new_freqs = (1 / (N * time_step)) * np.arange(N)
    psd = (f_hat * np.conjugate(f_hat) / N).real  # imag is already 0
    mag = (np.abs(f_hat) / N).real  # imag is already 0

    # cleaning based on threshold
    threshold_idxs = (psd > THRESHOLD)

    cleaned_psd = psd * threshold_idxs

    cleaned_f_hat = f_hat * threshold_idxs

    # regenerating signal based on cleaned spectrum using inverse fourier
    regen_signal = np.fft.ifft(cleaned_f_hat).real

    MSE = np.mean((original_signal - regen_signal) ** 2)

    if MSE<MinMSE:
        MinMSE = MSE
        best_noise=noise
        best_original_signal=original_signal
        best_noisy_signal=noisy_signal
        best_psd=psd
        best_mag=mag
        best_cleaned_psd=cleaned_psd
        best_regen_signal=regen_signal
        best_freqs_resulted = threshold_idxs
        best_freqs = freqs

    if MSE>MaxMSE:
        MaxMSE = MSE
        worst_noise=noise
        worst_original_signal=original_signal
        worst_noisy_signal=noisy_signal
        worst_psd=psd
        worst_mag=mag
        worst_cleaned_psd=cleaned_psd
        worst_regen_signal=regen_signal
        worst_freqs_resulted = threshold_idxs
        worst_freqs = freqs


plot_noisy_signals(best_original_signal, best_noise, best_noisy_signal,best_psd,best_mag,best_cleaned_psd,best_regen_signal,
                   'seaborn-v0_8-bright',MinMSE,"Best Signal - lowest error: ")

plot_noisy_signals(worst_original_signal, worst_noise, worst_noisy_signal,worst_psd,worst_mag,worst_cleaned_psd,worst_regen_signal,
                   'seaborn-v0_8-dark-palette',MaxMSE,"Worst Signal - highest error: ")

# print("Eroarea medie patratica minima:",MinMSE)
# print("Eroarea medie patratica maxima:",MaxMSE)

# FOR MORE STYLES TRY THE FOLLOWING PRINT
# print(plt.style.available)

print("Frequencies in the original best signal: ", np.sort(best_freqs))
indexes = np.where(best_freqs_resulted == True)[0]
print("Frequencies in the regenerated best signal: ", indexes)

print()
print("Frequencies in the original worst signal: ", np.sort(worst_freqs))
indexes = np.where(worst_freqs_resulted == True)[0]
print("Frequencies in the regenerated worst signal: ", indexes)

