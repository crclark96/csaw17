import sys, socket, time

flag = ""
f = open('bytestream','w')

def validate(data):

    global flag
    
    assert data[0] == '0'
    assert data[-2] == '1'
    print repr(data), " | ",
    
    data = str(data)[1:-2]# trim data
    tot = 0
    parity = int(data[-1])
    c_bits = data[:-1]
    print repr(c_bits), " | ",
    valid = c_bits.count('1') % 2 == parity
    print valid, " | ", 
    print chr(int(c_bits,2))
    if (valid):
        flag += chr(int(c_bits,2))
    return valid
    

def netcat(host, port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host, int(port)))
    data = s.recv(256).split('\n')[1]
    if validate(data+'\n'):
        s.send("1")
    else:
        s.send("0")
    while True:
        data = s.recv(256)
        if not data:
            break
        if validate(data):
            s.send("1")
        else:
            s.send("0")
    
    s.shutdown(socket.SHUT_WR)
    s.close()

    print flag
    
    
netcat('18.218.208.4', 8000)
print '\n'
