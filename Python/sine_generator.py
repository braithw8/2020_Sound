import math
import wave
import struct
import array

nSamples = 200000
freq = 440

nChannels = 1
sampleRate = 48000
bitDepth = 2


pi2 = 2* math.pi

freqRad = pi2 / sampleRate

phase = 0
volume = 1

phaseInc = freqRad * freq


sampleGen = []

for x in range(nSamples):
    currentSampleFloat = volume * math.sin(phase)
    currentSampleInt = int(round(currentSampleFloat * 32767))
    sampleGen.append(currentSampleInt)
    phase += phaseInc
    if phase >= pi2:
        phase -= pi2


byteArrayWave = bytearray()



for x in range(len(sampleGen)):

    currentInt = sampleGen[x]
    byteArrayWave.append(struct.pack("<h", currentInt)[0])
    byteArrayWave.append(struct.pack("<h", currentInt)[1])

destinationWave = 'sineGenerator.wav'

wFile = wave.open(destinationWave, mode='wb')
wFile.setnchannels(nChannels)
wFile.setsampwidth(bitDepth)
wFile.setframerate(sampleRate)
wFile.writeframesraw(byteArrayWave)
wFile.close()
