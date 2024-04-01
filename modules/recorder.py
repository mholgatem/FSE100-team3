import pyaudio
import wave


# Audio recording parameters
FORMAT = pyaudio.paInt16  # Data type
CHANNELS = 1  # Adjust this if your mic is stereo
RATE = 44100  # Sample rate
CHUNK = 1024  # Data chunks
WAVE_OUTPUT_FILENAME = "output.wav"  # Output file

def InitRecorder():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    return audio


def RecordAudio(audio, record_seconds):
    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
