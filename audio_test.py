import sounddevice as sd

def callback(indata, frames, time, status):
    if status:
        print(status)
    print(indata)

# Open a stream with the above parameters
stream = sd.InputStream(callback=callback, channels=1, samplerate=44100, blocksize=1024)
stream.start()

# Run for a few seconds to capture some audio
sd.sleep(5000)

stream.stop()
stream.close()
