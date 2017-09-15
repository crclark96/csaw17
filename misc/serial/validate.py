import sys, socket

def netcat(host, port, content):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    i = 0
    while True:
        i += 1
        data = s.recv(4096).split('\n')
        try:
            data = data[1]
        except:
            data = data[0]
        if not data: 
            break
        tot = 0
        for char in data[1:len(data)-1]: # validate parity
            tot += int(char) # sum data byte
        if tot%2 == 0:
            print data[1:len(data)-3] # print data w/o parity, stop, start
            s.sendall("1".encode())
        else:
            print "invalid"
            s.sendall("0".encode())
        print data

    s.shutdown(socket.SHUT_WR)
    s.close()
    

netcat('misc.chal.csaw.io', 4239, '')

i = 0

for line in sys.stdin:
    i+=1
    if i==1:
        continue

