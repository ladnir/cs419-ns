import socket
from sys import stdin
from random import randint
import time
import argparse


class Badguy:
    share1 = ""
    share2 = ""
    
    def check(self):
        if self.share1 == "" or self.share2 == "":
            print "bad guy knows one share"
            return
        
        print "bad guy thinks the password is "+str(self.share1 ^ self.share2) 
			
    

def setup(server1,server2):
    print "=============== setup ================"
    print " password?: ",
    password =  int(stdin.readline()[0:-1])
	
    r = randint(0,9999999999)
    print "random mask = "+str(r)
    
    server1.sendall("setup:" + str(r))
    server2.sendall("setup:" + str(r ^ password))
    return

def login(server1, server2):
    print "=============== login ==============="
    r = randint(0,9999999999)

    print " client picks a random number: "+str(r)
    print " password?: ",
    password =  int(stdin.readline()[0:-1])

    print "client sends server1 "+str(password ^ r)+". (password XOR random)"
    print "client sends server2 "+str(r)+". (just the random)"

    server1.sendall("login:" + str(password ^ r))
    server2.sendall("login:" + str(r))

    print
    msg1 = str(server1.recv(1024))
    if msg1 == "success":
        print "The password is correct"
    else:
        print "The password in not correct"
    return

def breach(s1,s2,badguy):
    bt  = ""
    
    print "which server? [1, 2] ",
    server = stdin.readline()[0:-1]
    print "server detection? [yes, no]",
    detection = stdin.readline()[0:-1]
    if detection == '1' or detection == 'yes':
        bt = "breach_notify"
    else:
        bt = "breach"
    
    if server == "1":
        s1.sendall(bt)
        badguy.share1 = int(s1.recv(1024))
    else:
        s2.sendall(bt)
        badguy.share2 =  int(s2.recv(1024))
    
    badguy.check()
	
def quit(s1,s2):
    s1.sendall("quit")
    s2.sendall("quit")
    
def main():
    HOST = 'localhost'
	
    badguy = Badguy()
	
    PORT1 = 95552 # primary server
    PORT2 = 95551 # secondary server

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((HOST, PORT1))
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((HOST, PORT2))
    command = ''
    while 1:
        print '?',
        command = stdin.readline()[0:-1]
        if command == 'setup':
	        setup(s1,s2)
        elif command == 'login':
		    login(s1,s2)
    	elif command == 'breach':
    	    breach(s1,s2,badguy)
        elif command == 'quit':
            quit(s1,s2)
            break
        else:
            print "invalid input, try:\n    > setup\n    > login\n    > breach\n    > quit"
    s1.close()
main()
