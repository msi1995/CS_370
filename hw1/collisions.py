#Reference: https://stackoverflow.com/questions/47073453/how-to-generate-a-random-string-with-symbols

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends.openssl.backend import backend
import random
import string
import binascii

def weakCollision():
    trialCount, successCount, totalTrials = 0, 0, 0
    plaintext = "rand!"
    plaintext_length = len(plaintext)
    plaintext = b"rand!"
    digest = hashes.Hash(hashes.SHA256(), backend)
    digest.update(plaintext)

    # set target to the first 24 bytes (3 values, or 6 ascii characters) of resulting hash
    target = binascii.hexlify(digest.finalize())
    target = target[0:6]

    digest = hashes.Hash(hashes.SHA256(), backend)
    print("\nMatching can take nearly 10 minutes to complete. Program is not frozen.")
    # runs 5 trials
    while successCount < 5:
        temp_digest = digest.copy()
        trialCount = trialCount + 1
        random_string = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(plaintext_length)])
        temp_digest.update(random_string.encode("utf-8"))
        actual = binascii.hexlify(temp_digest.finalize())[0:6]
        # print("Checking, run # ", trialCount)
        if actual == target:
            print("Weak Collision Run " + str(successCount+1) + ": Matched first 3 characters after " + str(trialCount) + " trials")
            successCount = successCount + 1
            totalTrials = totalTrials + trialCount
            trialCount = 0

    print("\nAfter 5 trials, the total number of trials ran: " + str(totalTrials))
    print("The average number of attacks to find a match for the first 3 characters was " + str(totalTrials/5))
    print("\n")


def strongCollision():
    hash_list = []
    trialCount, successCount, totalTrials = 0, 0, 0

    while successCount < 50:
        trialCount = trialCount + 1
        random_string = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(16)])
        digest = hashes.Hash(hashes.SHA256(), backend)
        digest.update(random_string.encode("utf-8"))
        hash_full = binascii.hexlify(digest.finalize()).decode("utf-8")
        hash_list.append(hash_full)
        for hash_value in hash_list[:-1]:
            if hash_full[0:6] == hash_value[0:6]:
                # print("Matched first 3 of " + hash_full + " with first 3 of " + hash_value + "after " + str(trialCount) + " trials")
                print("Strong Collision Run " + str(successCount+1) + ": Matched first 3 characters after " + str(trialCount) + " trials")
                successCount = successCount + 1
                totalTrials = totalTrials + trialCount
                trialCount = 0
                hash_list[:] = []
                break

    print("\nAfter 50 trials, the total number of trials ran: " + str(totalTrials))
    print("The average number of attacks to find a match for the first 3 characters was " + str(totalTrials / 50))
    print("\n")



if __name__ == '__main__':
    weakCollision()
    strongCollision()