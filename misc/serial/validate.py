import sys, socket

f = open('bytestream','w')

def validate(data):
    print repr(data), " | ",
    data = str(data)[1:len(data)-2]# trim data
    tot = 0
    for char in data:
        tot += int(char)
    data = data[1:]
    print repr(data), " | ",
    if tot % 2 == 0:
        sum = 0
        for i in range(8):
            sum += 2**i * int(data[i])
        print(chr(sum))
        f.write(chr(sum))
    else:
        print 
    return tot % 2 == 0

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
    

netcat('misc.chal.csaw.io', 4239)
print '\n'
