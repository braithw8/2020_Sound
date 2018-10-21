
# Finlay Braithwaite 2018


# Brute force with a try-except block
import wave
import struct
import math
import numpy as np
from scipy import signal

def openWaveFile():
    inputWaveFile = ''
    inputWaveFile = input("\nWhich wave file do you want to process?: ")
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

def exportAudio(inputWave, parameters, outputWave):
    byteArrayWave = bytearray()
    for x in range(len(inputWave)):
        currentInt = inputWave[x]
        if currentInt > 32767:
            currentInt = 32767
        elif currentInt < -32768:
            currentInt = -32768
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

def reverse(inputWave):
    processedWave = []
    for x in range(len(inputWave)):
        newSample = inputWave[-(x+1)]
        processedWave.append(newSample)
    return processedWave

def simpleFilter(inputWave, filterType):

    processedWave = []

    if filterType == 'notch':

        filterSample = 0
        for x in range(len(inputWave)):
            if x < len(inputWave) - 2:
                filterSample = int((inputWave[x] + inputWave[x+2]) / 2)

            processedWave.append(filterSample)
        #WHAT TO DO FOR LAST SAMPLE?
    elif filterType == 'lowpass':

        filterSample = 0
        for x in range(len(inputWave)):
            if x < len(inputWave) - 1:
                filterSample = int((inputWave[x] + inputWave[x+1]) / 2)

            processedWave.append(filterSample)

    elif filterType == 'highpass':

        filterSamplee = 0
        for x in range(len(inputWave)):
            if x < len(inputWave) - 1:
                filterSample = int((inputWave[x] - inputWave[x+1]) / 2)

            processedWave.append(filterSample)

    elif filterType == 'bandpass':

        filterSample = 0
        for x in range(len(inputWave)):
            if x < len(inputWave) - 2:
                filterSample = int((inputWave[x] - integerWave[x+2]) / 2)

            processedWave.append(filterSample)

    return processedWave

#simpleFilter('JustAnotherDay10.wav', 'bandpass', 'simpleFilterBandpass01.wav')

def butterworthFilter(inputWave, filterOrder, filterType, cutoffFreq):
    filterOrder = int(filterOrder)
    b, a = signal.butter(filterOrder, cutoffFreq, filterType)

    processedWave = signal.filtfilt(b,a, inputWave).tolist()
    for x in range(len(processedWave)):
        processedWave[x] = int(round(processedWave[x]))

    return processedWave

    #butterworthFilter('JustAnotherDay10.wav', 6, 'bandpass', [1/20, 1/10], 'butterworthBandpass01.wav')

def audioSum (sumInput1, sumLevel1, sumInput2, sumLevel2):
	sumWave = []
	currentSample = 0
	for x in range(len(sumInput1)):
		if x < len(sumInput2):
			currentSample = int(round((sumInput1[x] * sumLevel1) + (sumInput2[x] * sumLevel2)))
		elif x >= len(sumInput2):
			currentSample = int(round(sumInput1[x] * sumLevel1))
		sumWave.append(currentSample)
	return sumWave

def audioMix(inputA, levelA, inputB, levelB):

	if len(inputA) >= len(inputB):
		processedWave = audioSum(inputA, levelA, inputB, levelB)
	else:
		processedWave = audioSum(inputB, levelB, inputA, levelA)

	return processedWave


#audioMix('inputA.wav', .5, 'inputB.wav', .5, 'audioMix01.wav')

if __name__ == "__main__":
    print('\n***********************************\n* Welcome to the Audio Processor *\n***********************************\n')
    integerWave, parameters = openWaveFile()
    prompt = ''
    while prompt != '0':
        prompt = input("\n\t1: Varispeed\n\t2: Vibrato\n\t3: VariVibrato\n\t4: SimpleFilter\n\t5: ButterworthFilter\n\t6: Mix\n\t7: Reverse\n\t8: Export to file\n\t0: EXIT\n\nSelect a process: ")
        if prompt == '8':
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
        if prompt == '4':
            filterPrompt = ''
            filterPrompt = input("\n\t1: Lowpass\n\t2: Highpass\n\t3: Bandpass\n\t4: Notch\n\nEnter a filter type: ")
            if filterPrompt == '1':
                integerWave = simpleFilter(integerWave, 'lowpass')
            elif filterPrompt == '2':
                integerWave = simpleFilter(integerWave, 'highpass')
            elif filterPrompt == '3':
                integerWave = simpleFilter(integerWave, 'bandpass')
            elif filterPrompt == '4':
                integerWave = simpleFilter(integerWave, 'notch')
        if prompt == '5':
            filterTypePrompt = ''
            filterTypePrompt = input("\n\t1: Lowpass\n\t2: Highpass\n\t3: Bandpass\n\t4: Notch\n\nEnter a filter type: ")
            if filterTypePrompt == '1':
                filterType = 'lowpass'
                filterOrderPrompt = ''
                filterOrderPrompt = input("\nEnter a filter order 1-6: ")
                filterFreqAPrompt = ''
                filterFreqAPrompt = input("\nEnter a cutoff frequency in Hz: ")
                filterFreq = [float(filterFreqAPrompt) / (parameters[2] / 2)]
                integerWave = butterworthFilter(integerWave, filterOrderPrompt, filterType, filterFreq)
            elif filterTypePrompt == '2':
                filterType = 'highpass'
                filterOrderPrompt = ''
                filterOrderPrompt = input("\nEnter a filter order 1-6: ")
                filterFreqAPrompt = ''
                filterFreqAPrompt = input("\nEnter a cutoff frequency in Hz: ")
                filterFreq = [float(filterFreqAPrompt) / (parameters[2] / 2)]
                integerWave = butterworthFilter(integerWave, filterOrderPrompt, filterType, filterFreq)
            elif filterTypePrompt == '3':
                filterType = 'bandpass'
                filterOrderPrompt = ''
                filterOrderPrompt = input("\nEnter a filter order 1-4: ")
                filterFreqAPrompt = ''
                filterFreqAPrompt = input("\nEnter a lower cutoff frequency in Hz: ")
                filterFreqBPrompt = ''
                filterFreqBPrompt = input("\nEnter a high cutoff frequency in Hz: ")
                filterFreq = [float(filterFreqAPrompt) / (parameters[2] / 2), float(filterFreqBPrompt) / (parameters[2] / 2)]
                integerWave = butterworthFilter(integerWave, filterOrderPrompt, filterType, filterFreq)
            elif filterTypePrompt == '4':
                filterType = 'bandstop'
                filterOrderPrompt = ''
                filterOrderPrompt = input("\nEnter a filter order 1-4: ")
                filterFreqAPrompt = ''
                filterFreqAPrompt = input("\nEnter a lower cutoff frequency in Hz: ")
                filterFreqBPrompt = ''
                filterFreqBPrompt = input("\nEnter a high cutoff frequency in Hz: ")
                filterFreq = [float(filterFreqAPrompt) / (parameters[2] / 2), float(filterFreqBPrompt) / (parameters[2] / 2)]
                integerWave = butterworthFilter(integerWave, filterOrderPrompt, filterType, filterFreq)
        if prompt == '6':
            mixLevelAPrompt = ''
            mixLevelAPrompt = input('\nEnter a mix level for loaded wave (0-100): ')
            mixLevelAPrompt = float(mixLevelAPrompt) / 100
            print("\nSelect a Wave File to Mix\n")
            integerWaveB, parametersB = openWaveFile()
            mixLevelBPrompt = ''
            mixLevelBPrompt = input('\nEnter a mix level for loaded wave (0-100): ')
            mixLevelBPrompt = float(mixLevelBPrompt) / 100

            integerWave = audioMix(integerWaveB, mixLevelBPrompt, integerWave, mixLevelAPrompt)



        if prompt == '7':
            integerWave = reverse(integerWave)
