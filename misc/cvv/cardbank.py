import socket, random
from random import Random
import copy

prefixdict = {'Visa': [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']],
              'MasterCard': [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']],
              'Discover': [['6', '0', '1', '1']],
              'American Express': [['3', '4'], ['3', '7']]}

generator = Random()
generator.seed()        # Seed from current time

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0

def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = int(((sum / 10 + 1) * 10 - sum) % 10)

    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)


def credit_card_number(rnd, prefixList, length, howMany):

    result = []

    while len(result) < howMany:

        ccnumber = copy.copy(rnd.choice(prefixList))
        result.append(completed_number(ccnumber, length))

    return result

def completed_number_suffix(prefix, length, suffix):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1 - len(suffix)):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    for c in suffix:
        ccnumber.append(c)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = int(((sum / 10 + 1) * 10 - sum) % 10)

    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)


def credit_card_number_suffix(rnd, prefixList, length, howMany, suffix):

    result = []

    while len(result) < howMany:

        ccnumber = copy.copy(rnd.choice(prefixList))
        result.append(completed_number_suffix(ccnumber, length, suffix))

    return result


def output(title, numbers):

    result = []
    result.append(title)
    result.append('-' * len(title))
    result.append('\n'.join(numbers))
    result.append('')

    return '\n'.join(result)

def netcat(host, port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host, int(port)))
    types = ['MasterCard','Discover','American Express','Visa']
    lengthdict = {'MasterCard':16,'Discover':16,'American Express':15,'Visa':16}
    for i in range(25):
        data = s.recv(256)
        print(repr(data))
        for card in types:
            if card in data:
                ccnum = credit_card_number(generator, prefixdict[card], lengthdict[card], 1)
                print(ccnum[0])
                s.send(str(ccnum[0])+"\n")
        if not data:
            break
    for i in range(25):
        data = s.recv(256)
        print(repr(data))
        new_list = [[]]
        for c in data[-6:-2]:
            new_list[0].append(c)
        ccnum = credit_card_number(generator, new_list, 16, 1)
        print ccnum[0]
        s.send(str(ccnum[0]+"\n"))
    for i in range(25):
        data = s.recv(256)
        print(repr(data))
        endbit = data[-3]
        ccnum = credit_card_number(generator, new_list, 16, 20)
        while ccnum[0][-1] != endbit:
            ccnum = credit_card_number(generator, new_list, 16, 20)
        print ccnum[0]
        s.send(str(ccnum[0]+"\n"))
    for i in range(25):
        data = s.recv(256)
        print(repr(data))
        endbit = data[-3]
        ccnum = credit_card_number_suffix(generator, new_list, 16, 20, data[42:45])
        while ccnum[0][-1] != endbit:
            ccnum = credit_card_number_suffix(generator, new_list, 16, 20, data[42:45])
        print ccnum[0]
        s.send(str(ccnum[0]+"\n"))
        if not data:
            break
        prev = 0
    for i in range(26):
        data = s.recv(256)
        print(repr(data))
        len_ccnum = len(data) - 55 - prev
        number = data[26+prev:26+prev+len_ccnum]
        print number
        print is_luhn_valid(number)
        if is_luhn_valid(number):
            s.send("1\n")
            prev = 5
        else:
            s.send("0\n")
            prev = 6
        if not data:
            break

    s.shutdown(socket.SHUT_WR)
    s.close()

#
# Main
#

if __name__ == '__main__':

    netcat('misc.chal.csaw.io', 8308)

#voyager = credit_card_number(generator, voyagerPrefixList, 15, 3)
#print(output("Voyager", voyager))


