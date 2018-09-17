import wave
import struct

resampleRate = 48000

intWave = []
dropResampleIntWave= []
linearResampleIntWave= []

byteArrayWave = bytearray()

rFile = wave.open('wave.wav', mode='rb')

rParams = rFile.getparams()
#print(rParams)

rChannels =rFile.getnchannels()
print("source channels: " + str(rChannels))

rFrameRate =rFile.getframerate()
print("source frame rate: " + str(rFrameRate))

rNFrames =rFile.getnframes()
print("source # of frames " + str(rNFrames))

rSampleWidth = rFile.getsampwidth()
print("source sample width: " + str(rSampleWidth))

#print(type(rFile.getsampwidth()))

rawDump = rFile.readframes(rFile.getnframes())

#print("rawDump")
#print(rawDump)


#new resampling work

for x in range(rFile.getnframes()*2):
    if x % 2 == 0:
        intWave.append(int.from_bytes(rawDump[x:(x+2)], byteorder='big', signed=True))

resampleRatioA = resampleRate / rFrameRate
print("resampleRatioA: " + str(resampleRatioA))
resampleRatioB = rFrameRate / resampleRate
print("resampleRatioB: " + str(resampleRatioB))
resampleNFrames = int(rNFrames * resampleRatioA)
print("resampleNFrames: " + str(resampleNFrames))

newSample = 0

testRange = 44100

for x in range(testRange):

    #print(x * resampleRatioB)
    xPointer = x * resampleRatioB
    samplePointer = int(xPointer)

    #print(samplePointer)
    linearIntPoint = (xPointer) % 1

    currentSample = intWave[samplePointer]

    nextSample = intWave[samplePointer + 1]

    nextSampleDiff = nextSample - currentSample

    amountBetween = nextSampleDiff * linearIntPoint

    currentInterpolation = currentSample + amountBetween


    #print(samplePointer)


    #print(linearIntPoint)

    #if x == resampleNFrames:
    #    newSample = intWave[samplePointer]



    newSample = int(currentInterpolation)

    '''
    if abs(newSample) > 32767:
        print("\n" + str(x) + " is hot")
    '''

    #print("\nx\t" + str(x) + "\nxPointer\t" + str(xPointer) + "\nsamplePointer\t" + str(samplePointer) + "\nlinearIntPoint\t" + str(linearIntPoint) + "\ncurrentSample\t" + str(currentSample) + "\nnextSample\t" + str(nextSample) + "\nnextSampleDiff\t" + str(nextSampleDiff) + "\namountBetween" +str(amountBetween) + "\ncurrentInterpolation" + str(currentInterpolation) + "\nnewSample" + str(newSample) + str(type(newSample)))




    linearResampleIntWave.append(newSample)
    dropResampleIntWave.append(currentSample)

    #previousSample = samplePointer

print(dropResampleIntWave)
print(linearResampleIntWave)
print(intWave[0:testRange])







for x in range(len(linearResampleIntWave)):
    currentInt = linearResampleIntWave[x]
    currentByte = struct.pack('>h', currentInt)
    #print(currentByte)
    #print(type(currentByte))
    byteArrayWave.append(currentByte[0])
    byteArrayWave.append(currentByte[1])

#print(byteArrayWave)


wFile = wave.open('newWave.wav', mode='wb')

#wFile.setparams(rParams)

wFile.setnchannels(rChannels)
wFile.setsampwidth(rSampleWidth)
wFile.setframerate(resampleRate)


#byteWave = bytes(byteArrayWave)


#wFile.writeframesraw(rawDump)
wFile.writeframesraw(byteArrayWave)





wFile.close()
