MAX_KEY_SIZE = 26
MIN_KEY_SIZE = 0
nrVersions = 2
def getVersion():
    v = 0
    while True:
        print("\nProgram version to execute: ")
        v = int(raw_input())
        if (v > 0 and v <= nrVersions):
            return v

def getMessage():
    print("\nEnter your message: ")
    return raw_input()
def getKey():
    key = 0
    while True:
        print("\nEnter your key: ")
        key = int(raw_input())
        if (key >= MIN_KEY_SIZE and key < MAX_KEY_SIZE):
            return key
def getMode():
    while True:
        print("\nEncrypt(E) / Decrypt(D): ")
        mode = raw_input().lower()
        if mode == "e" or mode == "d":
            return mode  
def getMessageTranslation(mode,key,message):
    if mode == "d":
        key = -key
    translated = ""

    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key
            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            translated += chr(num)
        else:
            translated += symbol
    return translated
def CaesarBrute(mode,message):
    for k in range(0,MAX_KEY_SIZE+1,1):
        trans = getMessageTranslation(mode,k,message)
        print("key " + str(k) + ": " + trans)
def main():
    ver = getVersion()
    if ver == 1:
        md = getMode()
        msg = getMessage()
        k = getKey()
        trans = getMessageTranslation(md,k,msg)
        print("Translated message: " + trans)
    elif ver == 2:
        md = getMode()
        msg = getMessage()
        CaesarBrute(md,msg)
        
if __name__ == "__main__":
    main()