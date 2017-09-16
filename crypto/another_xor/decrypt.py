cipher = "274c10121a0100495b502d551c557f0b0833585d1b27030b5228040d3753490a1c025415051525455118001911534a0052560a14594f0b1e490a010c4514411e070014615a181b02521b580305170002074b0a1a4c414d1f1d171d00151b1d0f480e491e0249010c150050115c505850434203421354424c1150430b5e094d144957080d4444254643"


def find_duplicates(length):
    dups = []
    for i in range(len(cipher)-length):
        subset = cipher[i:i+length]
        if subset in cipher[i+length:]:
            dups.append(subset)
    return dups

def indices(dup):
    index_arr = []
    for i in range(len(cipher)-len(dup)):
        if cipher[i:i+len(dup)] == dup:
            index_arr.append(i)
    return index_arr

def freq_analysis(keylen):
    ciphers = []
    for i in range(keylen):
        ciphers.append('')
    for i in range(len(cipher)):
        ciphers[i%keylen] += cipher[i]
    for sub_cipher in ciphers:
        freq_table = dict()
        for char in sub_cipher:
            if char in freq_table:
                freq_table[char] += 1
            else:
                freq_table[char] = 1
        print(freq_table)

if __name__ == '__main__':
    dups = find_duplicates(4)
    print(dups)
    for dup in dups:
        index_arr = indices(dup)
        print((dup, index_arr, index_arr[1] - index_arr[0]))
    print(freq_analysis(2))
    
