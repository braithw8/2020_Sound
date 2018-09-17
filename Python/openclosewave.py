import wave
import struct

intWave = []
byteArrayWave = bytearray()

rFile = wave.open('wave.wav', mode='rb')

rParams = rFile.getparams()
#print(rParams)
#print(type(rFile.getsampwidth()))

rawDump = rFile.readframes(rFile.getnframes())

#print("rawDump")
#print(rawDump)


for x in range(rFile.getnframes()*2):
    if x % 2 == 0:
        intWave.append(int.from_bytes(rawDump[x:(x+2)], byteorder='big', signed=True))

for x in range(len(intWave)):
    currentInt = intWave[x]
    currentByte = struct.pack('>h', currentInt)
    #print(currentByte)
    #print(type(currentByte))
    byteArrayWave.append(currentByte[0])
    byteArrayWave.append(currentByte[1])




wFile = wave.open('newWave.wav', mode='wb')

wFile.setparams(rParams)


byteWave = bytes(byteArrayWave)


#wFile.writeframesraw(rawDump)
wFile.writeframesraw(byteWave)





wFile.close()
