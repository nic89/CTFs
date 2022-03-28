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

def injectCode(original, code):
    original = original[3:] #remove magic bytes

    magicBytes = b'\xFF\xD8\xFF\xE0'
    startJSComment = b'\x2F\x2A'
    header_length = original[:2] #get length in hex
    header = original[2:int.from_bytes(header_length, "big") - 2] #get original header

    headerPadding = int.from_bytes(startJSComment, "big") - int.from_bytes(header_length, "big")
    newHeader = startJSComment  
    if header_length > startJSComment:
        print("Try a smaller JPEG file")
        return False
    

