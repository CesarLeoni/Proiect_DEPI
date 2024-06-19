import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from mightypy.make import sine_wave_from_sample, sine_wave_from_timesteps

style.use('ggplot')

time_step = 0.001

# GENERATING NOISY SIGNAL
# amplitude parameter can be added , default is 1
wave1, time1, freqs1  = sine_wave_from_timesteps(signal_freq=50, time_step=time_step)
wave2, time2, freqs2  = sine_wave_from_timesteps(signal_freq=70, time_step=time_step)
original_signal = wave1 + wave2

N = len(original_signal)

noise = 2 * np.random.randn(N)

noisy_signal = original_signal + noise  # adding random noise here

fig = plt.figure(figsize=(13, 8))

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, (3, 4))

ax1.plot(original_signal)
ax1.set_title("original")
ax1.set_xlim(200, 400)  # Set x-axis limits to zoom in

ax2.plot(noise)
ax2.set_title("noise")
ax2.set_xlim(200, 400)  # Set x-axis limits to zoom in

ax3.plot(noisy_signal, label="noisy")
ax3.plot(original_signal, label="original")
ax3.set_xlim(200, 400)  # Set x-axis limits to zoom in

plt.legend()
plt.show()



# CALCULATING FFT - FOURIER FAST TRANSFORM
f_hat = np.fft.fft(noisy_signal, N)
n = int(np.floor(N / 2))  # frequencies till N/2 can be used for this processing

new_freqs = (1 / (N * time_step)) * np.arange(N)
psd = (f_hat * np.conjugate(f_hat) / N).real  # imag is already 0
mag = (np.abs(f_hat) / N).real  # imag is already 0


fig, ax = plt.subplots(3, 1, figsize=(10, 7))
#plt.axvline(50)
#plt.axvline(70)
ax[0].plot(new_freqs[:n], psd[:n], 'g', label='PSD')
ax[1].plot(new_freqs[:n], mag[:n], 'b', label="magnitude")

Thold = 100  # threshold for getting components
# cleaning based on threshold
threshold_idxs = (psd > Thold)

cleaned_psd = psd * threshold_idxs
ax[2].plot(new_freqs[:n], cleaned_psd[:n],'y',label='cleaned PSD')

fig.legend()
fig.show()



cleaned_f_hat = f_hat * threshold_idxs

# regenerating signal based on cleaned spectrum using inverse fourier
regen_signal = np.fft.ifft(cleaned_f_hat).real
fig, ax = plt.subplots(3, 1, figsize=(15, 15))

ax[0].plot(noisy_signal, label="noisy signal")
ax[0].plot(original_signal, label="original signal")
ax[0].legend()
ax[0].set_xlim(200, 400)  # Set x-axis limits to zoom in

ax[1].plot(noisy_signal, label="noisy signal")
ax[1].plot(regen_signal, label="recovered signal")
ax[1].legend()
ax[1].set_xlim(200, 400)  # Set x-axis limits to zoom in

ax[2].plot(original_signal, label="original signal")
ax[2].plot(regen_signal, label="recovered signal")
ax[2].legend()
ax[2].set_xlim(200, 400)  # Set x-axis limits to zoom in

plt.show()
