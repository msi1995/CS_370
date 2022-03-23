# References:
# https://datatracker.ietf.org/doc/html/rfc6238  -- documentation for TOTP. Some code copied verbatim from here.

import qrcode
import sys
import datetime
import time
import base64
import hmac
import hashlib

codeDigits = 6
padChar = b'\x00'


def generate_qr():
    # Described in GAuth documentation
    uri = "otpauth://totp/Example:lloyddo_HW4@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"
    qr_code = qrcode.make(uri)
    qr_code.save("myqrcode.jpg")


def get_otp():
    step_array = bytearray()

    #getting unix time
    currTime = datetime.datetime.now()
    timeTuple = currTime.timetuple()
    secSinceEpoch = time.mktime(timeTuple)

    # need to use // to get floor. number of 30 second steps since epoch
    stepNumber = int(secSinceEpoch // 30)

    while stepNumber != 0:
        # ensure the byte is in range 0-255 by getting the lowest 8 bits using AND operation (& 0xff)
        # The number has to be 0-255 to be put in the byte array. eight_bit contains the decimal value
        # represented by the last 8 or less binary bits of the decimal held in stepNumber. Since 8 bits is
        # 0-255, this will be in range.
        eight_bit = (stepNumber & 0xff)
        step_array.append(eight_bit)

        # shift 8 bits right(movingFactor) for next number
        stepNumber >>= 8

    # change endian, pad it
    result = bytearray(reversed(step_array))

    fullByte = 0
    while fullByte == 0:
        if len(result) == 8:
            fullByte = 1
            break
        result = padChar + result


    # in the RFC documentation they change key to bytes: byte[] k = hexStr2Bytes(key);
    key = base64.b32decode('JBSWY3DPEHPK3PXP')
    hasher = hmac.new(key, result, hashlib.sha1)
    hasher_output = bytearray(hasher.digest())

    # directly from documentation
    offset = hasher_output[len(hasher_output)-1] & 0xf

    # I honestly have no idea what this is doing... it shifts some bytes but I don't know.
    # I pulled it directly from the documentation
    binary = ((hasher_output[offset] & 0x7f) << 24 |
              (hasher_output[offset + 1] & 0xff) << 16 |
              (hasher_output[offset + 2] & 0xff) << 8 |
              (hasher_output[offset + 3] & 0xff))

    output = binary % 10 ** codeDigits

    # from documentation also
    while len(str(output)) < codeDigits:
        output = '0' + output
    print("--------------------")
    print("Auth Code: " + str(output))
    print("--------------------")


if __name__ == '__main__':
    if sys.argv[1] == "--generate-qr":
        generate_qr()
    if sys.argv[1] == "--get-otp":
        get_otp()
