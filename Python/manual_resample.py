import wave
import struct
import array

resampleRate = 76543

integerWave = []

writeIntWave = []
#writeIntWave = array.array('h')


byteArrayWave = bytearray()

rFile = wave.open('wave.wav', mode='rb')

rParams = rFile.getparams()

rChannels =rFile.getnchannels()
print("source channels: " + str(rChannels))

rFrameRate =rFile.getframerate()
print("source frame rate: " + str(rFrameRate))

rNFrames =rFile.getnframes()
print("source # of frames " + str(rNFrames))

rSampleWidth = rFile.getsampwidth()
print("source sample width: " + str(rSampleWidth))

rawDump = rFile.readframes(rFile.getnframes())

for x in range(rFile.getnframes()*2):
    if x % 2 != 0:
        y = x + 1
        integerWave.append(int.from_bytes(rawDump[x:y], byteorder='big', signed=True))


resampleRatioA = resampleRate / rFrameRate
print("resampleRatioA: " + str(resampleRatioA))
resampleRatioB = rFrameRate / resampleRate
print("resampleRatioB: " + str(resampleRatioB))
resampleNFrames = int(rNFrames * resampleRatioA)
print("resampleNFrames: " + str(resampleNFrames))

newSample = 0


for x in range(resampleNFrames - 1):

    xPointer = x * resampleRatioB
    samplePointer = int(xPointer)

    linearIntPoint = (xPointer) % 1
    currentSample = integerWave[samplePointer]
    nextSample = integerWave[samplePointer + 1]
    nextSampleDiff = nextSample - currentSample
    amountBetween = nextSampleDiff * linearIntPoint
    currentInterpolation = currentSample + amountBetween
    newSample = int(round(currentInterpolation))

    writeIntWave.append(newSample)

lowPassResample = []

for x in range(len(writeIntWave) -1)
    lowPassSample = (writeIntWave[x] + writeIntWave[x+1]) / 2
    lowPassResample.append(lowPassSample)


for x in range(len(writeIntWave)):
    currentInt = writeIntWave[x]
    currentByte = struct.pack('>h', currentInt)
    #print(currentByte)
    #print(type(currentByte))
    byteArrayWave.append(currentByte[0])
    byteArrayWave.append(currentByte[1])

wFile = wave.open('newWave.wav', mode='wb')

#wFile.setparams(rParams)

wFile.setnchannels(rChannels)
wFile.setsampwidth(rSampleWidth)
wFile.setframerate(rFrameRate)
wFile.writeframesraw(byteArrayWave)
wFile.close()
