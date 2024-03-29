
import frequencyAnalysis
import FindKeyLength
import itertools

upperCaseLetter = []
lowerCaseLetter = []
NUM_MOST_FREQ_LETTER = 4

# get nth letter and make string
def getNthSubkeysLetter(nth, keyLength, message):
    i = nth - 1
    letters = []

    while i < len(message):
        letters.append(message[i])
        i += keyLength
    
    return ''.join(letters)

def code(x):
    if x.islower():
        return ord(x) - 97
    else:
        return ord(x) - 65

def getItemAtIndexOne(item):
    return item[1]


def decryptionForProblem2(key, cipherText):
    keyTextLength = len(key)
    cipherTextLength = len(cipherText)
    key = key * int(cipherTextLength / keyTextLength) + key[0: cipherTextLength % keyTextLength]
	
    originalText = ""

    for i in range(0,26):
        upperCaseLetter.append(chr(i + 65))
        lowerCaseLetter.append(chr(i + 97)) 

    for i in range(cipherTextLength):
        if cipherText[i].isupper():
            x = (ord(cipherText[i]) - 65 - code(key[i])) % 26
            originalText += upperCaseLetter[x]
        else:
            x = (ord(cipherText[i]) - 97 - code(key[i])) % 26
            originalText += lowerCaseLetter[x]

    return originalText


def attemptHack(cipherText, mostPossibleKeyLength):
    cipherTextUp = cipherText.upper()
    
    allFreqScores = []
    for i in range(1, mostPossibleKeyLength + 1):
        nthLetters = getNthSubkeysLetter(i, mostPossibleKeyLength, cipherTextUp)
        freqScores = []
        #decrypt nth letter and store the letter with most frequency
        for possibleKey in frequencyAnalysis.LETTERS:
            decryptedText = decryptionForProblem2(possibleKey, nthLetters)

            keyAndFreqMatchTuple = (possibleKey, frequencyAnalysis.frequencyMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        
        freqScores.sort(key = getItemAtIndexOne, reverse = True)
        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTER])

    for i in range(len(allFreqScores)):
        print('Possible letters for letter %s of the key: ' %(i+1), end = '')

        for j in allFreqScores[i]:
            print('%s ' %(j[0]), end = '')
        print()

    for index in itertools.product(range(NUM_MOST_FREQ_LETTER), repeat = mostPossibleKeyLength):
        possibleKey = ''
        for i in range(mostPossibleKeyLength):
            possibleKey += allFreqScores[i][index[i]][0]
            print('Attempting with the key: %s ' %(possibleKey))
            decryptedText = decryptionForProblem2(possibleKey,cipherTextUp)

            origText = []
            for i in range(len(cipherText)):
                if cipherText[i].isupper():
                    origText.append(decryptedText[i].upper())
                else:
                    origText.append(decryptedText[i].lower())

            decryptedText = ''.join(origText)
            print('Possible text using key : %s ' %(possibleKey))
            print(decryptedText[:100])
            print()
            print('Write exit if done, anything else to continue hacking..')
            response = input('> ')

            if response.strip() == 'exit':
                return decryptedText
    
    return None


def decryptVigenere(cipherText):
    possibleKeyLength = FindKeyLength.findKeyLength(cipherText)
      
    keyLength = ''
    for i in possibleKeyLength:
        keyLength += '%s ' %(i)
    print('Possible key lengths are : ' + keyLength + '\n')

    originalMessage = None
    for i in possibleKeyLength:
        print('Attempting hack with key length %s (%s possible keys)...'% (i, NUM_MOST_FREQ_LETTER ** i))
        originalMessage = attemptHack(cipherText, i)
            
        if originalMessage != None:
            break
    return originalMessage

