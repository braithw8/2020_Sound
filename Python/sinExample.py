import math
import wave
import struct

BITRATE = 44100
FREQUENCY = 440
LENGTH = 1
WIDTH = 2

def GenerateSine(NumberOfFrames):
  wave = bytearray()
  for i in range(NumberOfFrames):
    value = math.sin(i * 2 * math.pi * FREQUENCY / BITRATE)
    value *= 128
    value *= (256 ** (WIDTH - 1)) - 1
    value = int(round(value))
    if WIDTH == 2:
      wave.append(struct.pack("<h", value)[0])
      wave.append(struct.pack("<h", value)[1])
    elif WIDTH == 4:
      wave += struct.pack("<l", value)
  return wave

WaveData = GenerateSine(int(BITRATE * LENGTH))

wf = wave.open("output.wav", 'w')
wf.setnchannels(1)
wf.setsampwidth(WIDTH)
wf.setframerate(BITRATE)
wf.writeframes(WaveData)
wf.close()
