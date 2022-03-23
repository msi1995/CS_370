# Referenced for guidance: https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
#output of murmur is 2^32 (32 bit hash): 4294967296

from bitarray import bitarray
import mmh3
import sys

dictfile = sys.argv[2]
inputfile = sys.argv[4]
bitarr_3_output = sys.argv[6]
bitarr_5_output = sys.argv[8]

def create_bitarray_3hash():
    # size of bitarray selected using this site. The false positive probability is about 2.9% here w/ 3 hashes.
    # https://hur.st/bloomfilter/?n=615000&p=0.05&m=&k=3
    bitarr_size = 5000000
    bit_array = bitarray(bitarr_size)
    bit_array.setall(0)
    hash_results = []

    # iterate through the dictionary and strip as needed
    with open(dictfile) as dictionary:
        for word in dictionary:
            word = word.rstrip()
            # integer i is fed into the Murmur hash as a seed. This means each loop is a different seed,
            # so each loop results in a different hash value, satisfying the 3 different hashes for this function.
            for i in range(3):
                hash_result = mmh3.hash(word, i) % bitarr_size
                hash_results.append(hash_result)
                bit_array[hash_result] = True

    return bit_array, bitarr_size

def check_presence_3hash(bit_array, bitarr_size):
    bitarr3_file = open(bitarr_3_output, "a")
    counter = 0
    isPresent = True

    # open the file
    with open(inputfile) as inputs:
        # get how many lines to read from the first line
        linesToRead = int(inputs.readline()[0:2]) + 1
        for word in inputs:
            word = word.rstrip()
            # stop reading if the number of lines to read has been reached
            if counter == linesToRead:
                break

            # if both of these pass, the hashed indices were all matched in the bitarray
            if isPresent is True and counter > 0:
                # print(store_word.rstrip() + " maybe")
                bitarr3_file.write(store_word + " maybe\n")

            isPresent = True
            counter = counter+1

            store_word = word
            for i in range(3):
                hash_result = mmh3.hash(word, i) % bitarr_size
                if bit_array[hash_result] == False:
                    isPresent = False
                    # print(word.rstrip() + " no")
                    bitarr3_file.write(word + " no\n")
                    break

    bitarr3_file.close()

def create_bitarray_5hash():
    # size of bitarray selected using this site. The false positive probability is about 2.0% here w/ 5 hashes.
    # https://hur.st/bloomfilter/?n=615000&p=0.05&m=&k=3
    bitarr_size = 5000000
    bit_array = bitarray(bitarr_size)
    bit_array.setall(0)
    hash_results = []

    # iterate through the dictionary and strip as needed
    with open(dictfile) as dictionary:
        for word in dictionary:
            word = word.rstrip()
            # integer i is fed into the Murmur hash as a seed. This means each loop is a different seed,
            # so each loop results in a different hash value, satisfying the 5 different hashes for this function.
            for i in range(5):
                hash_result = mmh3.hash(word, i) % bitarr_size
                hash_results.append(hash_result)
                bit_array[hash_result] = True

    return bit_array, bitarr_size


def check_presence_5hash(bit_array, bitarr_size):
    bitarr5_file = open(bitarr_5_output, "a")
    counter = 0
    isPresent = True

    # open the file
    with open(inputfile) as inputs:
        # get how many lines to read from the first line
        linesToRead = int(inputs.readline()[0:2]) + 1
        for word in inputs:
            word= word.rstrip()
            # stop reading if the number of lines to read has been reached
            if counter == linesToRead:
                break

            # if both of these pass, the hashed indices were all matched in the bitarray
            if isPresent is True and counter > 0:
                #print(store_word.rstrip() + " maybe")
                bitarr5_file.write(store_word.rstrip() + " maybe\n")

            isPresent = True
            counter = counter+1

            store_word = word
            for i in range(5):
                hash_result = mmh3.hash(word, i) % bitarr_size
                if bit_array[hash_result] == False:
                    isPresent = False
                    #print(word.rstrip() + " no")
                    bitarr5_file.write(word.rstrip() + " no\n")
                    break
    bitarr5_file.close()


if __name__ == '__main__':

    #create bit array for 3 hash and check presence
    bit_array_3, bitarr_3_size = create_bitarray_3hash()
    check_presence_3hash(bit_array_3, bitarr_3_size)

    # create bit array for 5 hash and check presence
    bit_array_5, bitarr_5_size = create_bitarray_5hash()
    check_presence_5hash(bit_array_5, bitarr_5_size)
