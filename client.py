import socket
from sys import stdin
from random import randint
import time
import argparse

def setup(server1,server2):
    print "=============== setup ================"
    print " password?: ",
    password =  int(stdin.readline()[0:-1])

	
    r = randint(0,9999999999)
    print "random mask = "+str(r)

    server1.sendall(str(r))
    server2.sendall(str(r ^ password))
    return

def login(server1, server2):
    print "=============== login ==============="
    r = randint(0,9999999999)

    print " client picks a random number: "+str(r)
    print " password?: ",
    password =  int(stdin.readline()[0:-1])
    print "client sends server1 "+str(password ^ r)+". (password XOR random)"
    server1.sendall(str(password ^ r))
    print "client sends server2 "+str(r)+". (just the random)"
    server2.sendall(str(r))
    print
    msg1 = str(server1.recv(1024))
    print "Got " + msg1 + " from server1"
    msg2 = str(server2.recv(1024))
    print "Got " + msg2 + " from server2"
    if msg1 == msg2:
        print "The password is correct"
    else:
        print "The password in not correct"
    return

def rotate( server1, server2):
	print "============= Rotation ==============="

	r = 3384485068
	print " rotating shares with random "+str(r)


	server1.sendall(str(r))
	server2.sendall(str(r))
	print
	
def main():
    HOST = 'flip.engr.oregonstate.edu'
    parser = argparse.ArgumentParser(description='Get port number.')
    parser.add_argument('port', metavar='N', type=int, nargs = 2, help = ' The ports that the servers is hosted on.')
    PORT1 = parser.parse_args().port[0]	
    PORT2 = parser.parse_args().port[1]	
    #PORT1 = 95552
    #PORT2 = 95551
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((HOST, PORT1))
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((HOST, PORT2))
    command = ''
    while 1:
        print '?',
        command = stdin.readline()[0:-1]
        s1.sendall(command)
        s2.sendall(command)
        if command == 'setup':
	        setup(s1,s2)
        if command == 'login':
		    login(s1,s2)
        if command == 'rotate':
	    	rotate(s1,s2)
        if command == 'quit':
		    break
    s1.close()
main()