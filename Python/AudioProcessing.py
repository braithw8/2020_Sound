
# Finlay Braithwaite 2018


# Brute force with a try-except block
import wave
import struct
import math

def openWaveFile():
    inputWaveFile = ''
    inputWaveFile = input("Which wave file do you want to process?")
    try:
        rawFile = wave.open(inputWaveFile, mode='rb')
    except FileNotFoundError:
        pass
    rawDump = rawFile.readframes(rawFile.getnframes())
    parameters = rawFile.getparams()
    integerWave = []
    for x in range(rawFile.getnframes()*2):
        if x % 2 == 0:
            y = x + 2
            integerWave.append(int.from_bytes(rawDump[x:y], byteorder='little', signed=True))
    return integerWave, parameters

def exportAudio(inputAudio, parameters, outputWave):
    byteArrayWave = bytearray()
    for x in range(len(inputAudio)):
        currentInt = inputAudio[x]
        currentByte = struct.pack('<h', currentInt)
        byteArrayWave.append(currentByte[0])
        byteArrayWave.append(currentByte[1])

    wFile = wave.open(outputWave, mode='wb')
    wFile.setparams(parameters)
    wFile.writeframesraw(byteArrayWave)
    wFile.close()

def varispeed(inputWave, parameters, resampleRate):
    inputSampleRate = parameters[2]
    resampleRelativeRate = (1/(float(resampleRate)/100)) * inputSampleRate
    inputSampleCount = len(inputWave)

    resampleRatioA = resampleRelativeRate / inputSampleRate
    resampleRatioB = inputSampleRate / resampleRelativeRate
    resampleSampleCount = int(inputSampleCount * resampleRatioA)

    newSample = 0
    processedWave = []
    for x in range(resampleSampleCount):

        if x < resampleSampleCount - 1:
            xPointer = x * resampleRatioB
            samplePointer = int(xPointer)
            linearIntPoint = (xPointer) % 1
            currentSample = inputWave[samplePointer]
            nextSample = inputWave[samplePointer + 1]
            nextSampleDiff = nextSample - currentSample
            amountBetween = nextSampleDiff * linearIntPoint
            currentInterpolation = currentSample + amountBetween
            newSample = int(round(currentInterpolation))

        elif x == resampleSampleCount - 1:
            newSample = inputWave[-1]

        processedWave.append(newSample)
    return processedWave

def vibratoAudio(inputWave, parameters, vibratoFrequency, vibratoIntensity):

    vibratoFrequency = float(vibratoFrequency)
    vibratoIntensity = float(vibratoIntensity)

    inputSampleRate = parameters[2]
    inputSampleCount = len(inputWave)

    freqRad = math.tau / inputSampleRate
    phaseIncr = freqRad * vibratoFrequency
    phase = 0

    processedWave = []

    for x in range(inputSampleCount):

        currentIndex = x + math.sin(phase) * vibratoIntensity
        phase = phase + phaseIncr
        if phase >= math.tau:
            phase = phase - math.tau
        if currentIndex <= inputSampleCount - 1:
            xPointer = currentIndex
            samplePointer = int(xPointer)
            linearIntPoint = (xPointer) % 1
            currentSample = inputWave[samplePointer]
            nextSample = inputWave[samplePointer + 1]
            nextSampleDiff = nextSample - currentSample
            amountBetween = nextSampleDiff * linearIntPoint
            currentInterpolation = currentSample + amountBetween
            newSample = int(round(currentInterpolation))
            processedWave.append(newSample)

    return processedWave

def variVibrato(inputWave, parameters, vibratoFrequency, vibratoIntensity, modFrequency, modIntensity):

    inputSampleRate = parameters[2]
    inputSampleCount = len(inputWave)

    vibratoFrequency = float(vibratoFrequency)
    vibratoIntensity = float(vibratoIntensity)
    modFrequency = float(modFrequency)
    modIntensity = float(modIntensity)

    freqRad = math.tau / inputSampleRate
    phaseIncr = freqRad * vibratoFrequency
    modPhaseIncr = freqRad * modFrequency
    phase = 0
    modPhase = 0

    processedWave = []

    for x in range(inputSampleCount):

        currentIndex = x + math.sin(phase) * vibratoIntensity
        modValue = modIntensity * math.sin(modPhase)
        phase = phase + phaseIncr + modValue
        modPhase = modPhase + modPhaseIncr
        #print(currentIndex)
        if phase >= math.tau:
            phase = phase - math.tau
        if currentIndex <= inputSampleCount - 1:
            xPointer = currentIndex
            samplePointer = int(xPointer)
            linearIntPoint = (xPointer) % 1
            currentSample = inputWave[samplePointer]
            nextSample = inputWave[samplePointer + 1]
            nextSampleDiff = nextSample - currentSample
            amountBetween = nextSampleDiff * linearIntPoint
            currentInterpolation = currentSample + amountBetween
            newSample = int(round(currentInterpolation))
            processedWave.append(newSample)

    return processedWave

if __name__ == "__main__":
    print('Welcome to the Audio Processor')
    print('0 to exit')
    integerWave, parameters = openWaveFile()
    prompt = ''
    while prompt != '0':
        prompt = input("\t1: Varispeed\n\t2: Vibrato\n\t3: VariVibrato\n\t4: SimpleFilter\n\t5: ButterworthFilter\n\t6: Mix\n\t7: Export to file\nSelect a process: ")
        if prompt == '7':
            outputWave = ''
            outputWave = input("Name the output file: ")
            exportAudio(integerWave, parameters, outputWave)
        if prompt == '1':
            resampleRate = ''
            resampleRate = input("Specify Speed (100 is normal): ")
            integerWave = varispeed(integerWave, parameters, resampleRate)
        if prompt == '2':
            vibratoRate = ''
            vibratoRate = input("Enter Vibrato Frequency: ")
            vibratoAmount = ''
            vibratoAmount = input("Enter Vibrato Amount: ")
            integerWave = vibratoAudio(integerWave, parameters, vibratoRate, vibratoAmount)
        if prompt == '3':
            vibratoRate = ''
            vibratoRate = input("Enter Vibrato Frequency: ")
            vibratoAmount = ''
            vibratoAmount = input("Enter Vibrato Amount: ")
            modFrequency = ''
            modFrequency = input("Enter Modulation Frequency: ")
            modIntensity = ''
            modIntensity = input("Enter Modulation Intensity: ")
            integerWave = variVibrato(integerWave, parameters, vibratoRate, vibratoAmount, modFrequency, modIntensity)
