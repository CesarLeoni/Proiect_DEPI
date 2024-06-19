import wave
import numpy as np
import struct

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
