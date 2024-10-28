import sounddevice
from scipy.io.wavfile import write

fs = 44100
segundos = 10
print('grabando...')
record_voice=sounddevice.rec(int(segundos * fs), samplerate=fs,channels=2)
sounddevice.wait()
write('out.wav',fs,record_voice)