import socket

def send(stuff):
    UDP_IP="127.0.0.1"
    UDP_PORT=5005
    MESSAGE=stuff

    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    print "message:", MESSAGE

    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.sendto( MESSAGE, (UDP_IP, UDP_PORT) )


def receive():
    UDP_IP=""
    UDP_PORT=5005

    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.settimeout(3.0)
    sock.bind( (UDP_IP,UDP_PORT) )
    
    try:
        data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
        print "received message:", data
    except:
        pass
receive()
