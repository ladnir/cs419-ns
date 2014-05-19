#Server database
import socket
import argparse

def setup(conn):
    print "=============== setup ================"
    share = int(conn.recv(1024))
    print 'Share = ' + str(share)
    return share

def login(conn,share):
    print "=============== login ==============="
    message = int(conn.recv(1024))
    lmessage = share ^ message
    print 'calculated ' + str(lmessage)
    conn.sendall(str(lmessage))
    return

def rotate(conn,share):
    print "============= Rotation ==============="
    rkey = int(conn.recv(1024))
    print "New share = " + str(share ^ rkey)
    return share ^ rkey

def main():
    HOST = 'flip.engr.oregonstate.edu'
    parser = argparse.ArgumentParser(description='Get port number.')
    parser.add_argument('port', metavar='N', type=int, nargs = 1, help = ' The port that the server is hosted on.')
    PORT = parser.parse_args().port[0]
    #PORT = 95552
    share = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if data == 'setup':
    		share = setup(conn)
        if data == 'login':
            login(conn,share)
        if data == 'rotate':
    		share = rotate(conn,share)
        if data == 'quit':
    		break
    conn.close()
main()