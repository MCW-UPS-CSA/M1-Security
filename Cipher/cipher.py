#!/usr/bin/python3
class Text:
    def __init__(self):
        self.fileIN = ""
        self.fileOUT = ""
        self.encrypted = ""
        self.decrypted = ""
class Key:
    def __init__(self):
        self.minLen = 2
        self.maxLen = 18
        self.length = 0
        self.value = ""
class Cipher:
    def __init__(self):
        self.AlphaUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.AlphaLower = 'abcdefghijklmnopqrstuvwxyz'
        self.Alpha = self.AlphaLower + self.AlphaUpper
        self.AlphaUDict = { self.AlphaUpper[i:i+1] :i for i in range(0,len(self.AlphaUpper),1) }
        self.AlphaLDict = { self.AlphaLower[i:i+1] :i for i in range(0,len(self.AlphaLower),1) }
        self.AlphaLUDict = {**self.AlphaLDict, **self.AlphaUDict}
        self.AlphaDict = {self.Alpha[i:i+1] : i for i in range(0,len(self.Alpha),1)}
        self.Frequencies = { 'en' : {
            'A': 8.12, 'B': 1.49, 'C': 2.71, 'D': 4.32, 'E': 12.02, 'F': 2.30, 'G': 2.03, 
            'H': 5.92, 'I': 7.31, 'J': 0.10, 'K': 0.69, 'L': 3.98, 'M': 2.61, 'N': 6.95,
            'O': 7.68, 'P': 1.82, 'Q': 0.11, 'R': 6.02, 'S': 6.28, 'T': 9.10, 'U': 2.88,
            'V': 1.11, 'W': 2.09, 'X': 0.17, 'Y': 2.11, 'Z': 0.07},
            'fr' : {},
            'de' : {}
        }
        self.avgIC = {'rand':0.0385, 'en' : 0.0667, 'ru' : 0.0529, 'german' : 0.0762, 'fr':0.0778}
    def Caesar_TextStrip(self,text):
        strippedText = ""
        for letter in text:
            if letter.isalnum(): strippedText += letter
            elif letter == ' ': strippedText += letter
        return strippedText
    def Caesar_Cipher(self,text,key,mode):
        text = self.Caesar_TextStrip(text)
        if mode == "decrypt" and key >= 0: key = -key
        translated = ""
        for symbol in text:
            if symbol.isalpha():
                if symbol.isupper(): translated += self.AlphaUpper[(self.AlphaUDict[symbol] +key) % len(self.AlphaUpper)]
                elif symbol.islower(): translated += self.AlphaLower[(self.AlphaLDict[symbol] +key) % len(self.AlphaLower)]
            elif symbol.isalnum(): translated += symbol
            else: translated += symbol
        return translated
    def Caesar_Encrypt(self,text,key):
        return self.Caesar_Cipher(text,key,"encrypt")
    def Caesar_Decrypt(self,text,key):
        return self.Caesar_Cipher(text,key,"decrypt")
    def Vigenere_TextStrip(self,text):
        strippedText = ""
        for letter in text:
            if letter.isalpha():
                strippedText += self.AlphaUpper[self.AlphaLUDict[letter]]
        return strippedText
    def Vigenere_TextStripLight(self,text):
        strippedText = ""
        for letter in text:
            if letter.isalpha():
                if letter.isupper():
                    strippedText += self.AlphaUpper[self.AlphaLUDict[letter]]
                elif letter.islower():
                    strippedText += self.AlphaLower[self.AlphaLUDict[letter]]
            elif letter.isalnum():
                strippedText += letter
            elif letter == ' ':
                strippedText += letter
        return strippedText
    def Vigenere_Alpha2Num(self,text):
        numarr = []
        for symbol in text:
            if symbol.isalpha(): numarr.extend([self.AlphaLUDict[symbol]])
        return numarr
    def Vigenere_Cipher(self,text,key,mode):
        text = self.Vigenere_TextStripLight(text)
        #text = self.Vigenere_TextStrip(text)
        key = self.Vigenere_Alpha2Num(key)
        keyLength = len(key)
        translated = ""
        keyIndex = 0
        for letter in text:
            if letter.isalpha():
                translated += self.Caesar_Cipher(letter,key[keyIndex % keyLength],mode)
                keyIndex += 1
            else: translated += letter
        #for letterIndex in range(0,len(text),1):
        #    translated += self.Caesar_Cipher(text[letterIndex],key[letterIndex % keyLength],mode)
        return translated
    def Vigenere_Encrypt(self,text,key):
        return self.Vigenere_Cipher(text,key,"encrypt")
    def Vigenere_Decrypt(self,text,key):
        return self.Vigenere_Cipher(text,key,"decrypt")
    def Vigenere_getOccurencesByNGramAgressive(self,text,N):
        #text = string, N = int
        text = self.Vigenere_TextStrip(text)
        subText = []
        for pos in range(0,len(text)-N,1):
            subText.append([pos,text[pos:pos+N]])
        occurences = []
        for sub in subText:
            times = 0
            occurencesLocal = []
            for k in range(sub[0]+1,len(text)-N):
                if sub[1] == text[k:k+N]:
                    occurencesLocal.extend([k])
                    times += 1
            if times > 0:
                occurences.append([sub[1],sub[0]]+occurencesLocal)
        #occurences = [['ABC',0,4,80...],['HWS',5,20,position...]...]
        return occurences
    def Vigenere_getKeySpacing(self,occurences):
        #occurences = [['ABC',0,4,80,position...],['HWS',5,20...]...]
        spacings = []
        for couple in occurences:
            localDist = []
            localDist.append(couple[0])
            for i in range(1,len(couple)-1):
                localDist.extend([couple[i+1]-couple[i]])
            spacings.append(localDist)
        #spacingts = [['ABC',4,76...],['HWS',5,15,distance...]]
        return spacings
    def Vigenere_getSpacingFactors(self,spacings):
        #spacingts = [['ABC',4,76,distance...],['HWS',5,15...]]
        factors = []
        for distances in spacings:
            for pos in range(1,len(distances),1):
                for i in range(1, distances[pos]//2+1):
                    if distances[pos] % i == 0:
                        factors.append(i)
        #factors = [(factor),2,2,2,3,3,3,4,4,6,6,6,6...]
        return factors
    def Vigenere_getCountFactors(self,factors):
        #factors = [(factor),2,2,2,3,3,3,4,4,6,6,6,6...]
        factorFreq = []
        alreadyParsed = []
        for item in factors:
            if item not in alreadyParsed:
                alreadyParsed.append(item)
                localFreq = 0
                for compare in factors:
                    if item == compare:
                        localFreq += 1
                factorFreq.append([item,localFreq])
        #factorFreq = [[(factor),(occurence)],[3,3],[4,2],[6,4]...]
        return factorFreq
    def Vigenere_getTopFactors(self,factorFreq,minKey,maxKey):
        #factorFreq = [[2,4],[3,3],[(factor),(occurence)],[6,4]...]
        viableFactors = []
        for item in factorFreq:
            if item[0] >= minKey and item[0] <= maxKey:
                viableFactors.append(item)
        viableFactors = sorted(viableFactors, key = lambda item: item[1],reverse=True)
        topViableFactors = []
        base = viableFactors[0][1] / 3
        for factor in viableFactors:
            if factor[1] > base:
                topViableFactors.append(factor)
        #viableFactors = [[(factor),(occurence)],[3,3],[4,2],[6,4]...]
        return topViableFactors
    def Vigenere_getEveryNthLetter2List(self,text,keyLength):
        text = self.Vigenere_TextStrip(text)
        lines = []
        for i in range(0,keyLength,1):
            builtLine = ""
            for k in range(i,len(text),keyLength):
                builtLine += text[k]
            lines.extend([builtLine])
        return lines
    def stringLetterCounter(self,text):
        counterMap = []
        alreadyCounted = []
        for letter in range(0,len(text),1):
            if text[letter] not in alreadyCounted:
                occurences = 0
                alreadyCounted.extend([text[letter]])
                for pos in range(letter,len(text)):
                    if text[letter] == text[pos]:
                        occurences += 1
                counterMap.append([text[letter],occurences])
        return counterMap
    def Vigenere_IoCscoreLine(self,line):
        lineScoreMap = self.stringLetterCounter(line)
        IC = 0
        for score in lineScoreMap:
            IC += score[1] * (score[1] - 1)
        return IC
    def Vigenere_IndexOfCoincidence(self,text,keyLength):
        text = self.Vigenere_TextStrip(text)
        lines = self.Vigenere_getEveryNthLetter2List(text,keyLength)
        coefs = []
        for line in lines:
            lineScoreMap = self.stringLetterCounter(line)
            freqsum = 0.0
            for score in lineScoreMap:
                freqsum += score[1] * (score[1] -1)
            IC = freqsum / (len(line)*(len(line)-1)) #* len(self.AlphaUpper)
            #print(IC)
            coefs.extend([IC])
        IoC = 0
        for c in coefs: IoC += c
        IoC = IoC / len(coefs)
        return round(IoC,4)
    def Vigenere_getKeyPeriod(self,text,minKey,maxKey,N):
        #text = string, minKey, maxKey, N = int
        text = self.Vigenere_TextStrip(text)
        occurences = self.Vigenere_getOccurencesByNGramAgressive(text,N)
        #occurences = [['ABC',0,4,80...],['HWS',5,20...]...]
        spacings = self.Vigenere_getKeySpacing(occurences)
        #spacingts = [['ABC',4,76...],['HWS',5,15...]]
        spacingFacotrs = self.Vigenere_getSpacingFactors(spacings)
        #spacingFacotrs = [2,2,2,2,3,3,3,4,4,6,6,6,6...]
        factorFreq = self.Vigenere_getCountFactors(spacingFacotrs)
        #factorFreq = [[2,4],[3,3],[4,2],[6,4]...]
        topViableFactors = self.Vigenere_getTopFactors(factorFreq,minKey,maxKey)
        #viableFactors = [[2,4],[3,3],[4,2],[6,4]...]
        print("Top viable periods by NGrams: ",topViableFactors)
        periods = []
        for period in topViableFactors:
            periods.append([period[0],self.Vigenere_IndexOfCoincidence(text,period[0])])
        periods = sorted(periods, key = lambda item: item[1],reverse=True)
        print("Top viable key lengths by IC: ", periods)
        return periods[0][0]
    def Vigenere_CHI2(self,text,keyLength):
        text = self.Vigenere_TextStrip(text)
        lines = self.Vigenere_getEveryNthLetter2List(text,keyLength)
        bestCHIscores = []
        for line in lines:
            CHIlineScores = []
            for decryptKey in range(0,len(self.AlphaUpper),1):
                decrypted = self.Caesar_Decrypt(line,decryptKey)
                lineMap = self.stringLetterCounter(decrypted)
                chi = 0
                for couple in lineMap:
                    chi += ((couple[1]- self.Frequencies["en"][couple[0]])**2)/self.Frequencies["en"][couple[0]]
                CHIlineScores.append([decryptKey,chi])
            CHIlineScores = sorted(CHIlineScores, key = lambda item: item[1],reverse=False)
            bestCHIscores.append(CHIlineScores)
        #print(bestCHIscores)
        topViableKeys = []
        for lineScore in bestCHIscores:
            line = []
            for score in range(0,3,1):
                line.extend([lineScore[score][0]])
            topViableKeys.append(line)
        return topViableKeys
        '''
            lowestCHIscore = CHIlineScores[0]
            for score in CHIlineScores:
                if lowestCHIscore[1] > score[1]:
                    lowestCHIscore = score
            bestCHIscores.append(lowestCHIscore)
        result = []
        for score in bestCHIscores:
            result.extend([score[0]])
        return result
        '''
    def Vigenere_getKeyValue(self,text,keyLength):
        caesarKeys = self.Vigenere_CHI2(text,keyLength)
        translatedKeys = []
        # in progress
        for line in range(0,len(caesarKeys),1):
            tmpLine = []
            print("\nCandidates for key ",line,": ", end='')
            for key in caesarKeys[line]:
                print(self.AlphaUpper[key],' ', end='')
                tmpLine.extend(self.AlphaUpper[key])
            translatedKeys.append(tmpLine)       
        print()
        #works fine
        bestKey = ""
        for line in range(0,len(caesarKeys),1):
            bestKey += self.AlphaUpper[caesarKeys[line][0]]
        return bestKey
def init(mode,keyMode,fileIN,fileOUT,keyValue,minKey,maxKey,keySize):
    text = Text()
    text.fileIN = fileIN
    text.fileOUT = fileOUT
    if mode == "encrypt":
        text.decrypted = open(fileIN,'r').read().replace('\n', '')
    elif mode == "decrypt":
        text.encrypted = open(fileIN,'r').read().replace('\n', '')
    key = Key()
    if keyMode == 'value':
        key.value =  keyValue
    elif keyMode == 'limits':
        key.minLen = minKey
        key.maxLen = maxKey
    elif keyMode == 'length':
        key.length = keySize
    return Cipher(),text, key
def encryptMode(cipher,key,text,method):
    if method == "caesar":
        text.encrypted = cipher.Caesar_Encrypt(text.decrypted,key.value)
        print("Your encrypted can be found in the file '"+text.fileOUT+"' :\n",text.encrypted)
        open(text.fileOUT,'w').write(text.encrypted)
    elif method == "vigenere":
        text.encrypted = cipher.Vigenere_Encrypt(text.decrypted,key.value)
        print("Your encrypted can be found in the file '"+text.fileOUT+"' :\n",text.encrypted)
        open(text.fileOUT,'w').write(text.encrypted)
def decryptMode(method,cipher,text,key,keymode):
    if method == "caesar":
        text.decrypted = cipher.Caesar_Decrypt(text.encrypted,key.value)
        print("Your decrypted can be found in the file '"+text.fileOUT+"' :\n",text.decrypted)
        open(text.fileOUT,'w').write(text.decrypted)
    elif method == "vigenere":
        if keymode == "value":
            text.decrypted = cipher.Vigenere_Decrypt(text.encrypted,key.value)
            print("Your decrypted can be found in the file '"+text.fileOUT+"' :\n",text.decrypted)
            open(text.fileOUT,'w').write(text.decrypted)
        if keymode == "limits":
            key.length = cipher.Vigenere_getKeyPeriod(text.encrypted,key.minLen,key.maxLen,3)
            print("Estipated key Length: ", key.length)
            key.value = cipher.Vigenere_getKeyValue(text.encrypted,key.length)
            print("The found key is:", key.value)
            text.decrypted = cipher.Vigenere_Decrypt(text.encrypted,key.value)
            print("\nThe decrypted text is found in the file '"+text.fileOUT+"' :\n")
            print(text.decrypted)
            open(text.fileOUT,'w').write(text.decrypted)
        if keymode == "length":
            key.value = cipher.Vigenere_getKeyValue(text.encrypted,key.length)
            print("The found key is:", key.value)
            text.decrypted = cipher.Vigenere_Decrypt(text.encrypted,key.value)
            print("The decrypted text is found in the file '"+text.fileOUT+"' :\n")
            print(text.decrypted)
            open(text.fileOUT,'w').write(text.decrypted)
def main():
    #Modes: 1 = encrypt, 2 = decrypt, Methods: 'vigenere', 'caesar'
    method,mode,fileIN,fileOUT = "vigenere","decrypt","encrypted","out"
    #KeyModes: value = known, limits = knownLimits, length = knownLength
    keyMode,keyValue,minKey,maxKey,keySize = "limits","ABC",2,8,3

    #cipher and resources initialization
    cipher,text,key = init(mode,keyMode,fileIN,fileOUT,keyValue,minKey,maxKey,keySize)
    if mode == "encrypt": encryptMode(cipher,key,text,method)
    elif mode == "decrypt": decryptMode(method,cipher,text,key,keyMode)
'''

    key.length = cipher.Vigenere_getKeyPeriod(text.encrypted,key.minLen,key.maxLen,3)
    print("Estipated key Length: ", key.length)

    key.value = cipher.Vigenere_getKeyValue(text.encrypted,key.length)
    print("The found key is:", key.value)

    text.decrypted = cipher.Vigenere_Decrypt(text.encrypted,key.value)
    print("The decrypted text is found in the file '"+text.fileOUT+"' :\n")
    print(text.decrypted)
    open(text.fileOUT,'w').write(text.decrypted)
'''
if __name__ == "__main__":
    main()
