#Server database
import socket
import argparse
import time
from random import randint

secondaryServerPort = 95551
primaryServerPort = 95552

rotatePort = 95553    # port for rotating
internalPort = 95554  # port for sending values

def read(socket):
    d = ""
    while d == "":
        d = tryRead(socket)
        
    return d

def tryRead(socket):
    try:
        return socket.recv(1024)
    except :
        time.sleep(0.05)
        pass
        return ""
        
def clientConnect(HOST,port,blocking):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    s.listen(1)
    conn, addr = s.accept()
    conn.setblocking(blocking)
    
    return conn

def internalConnect(HOST,port,blocking,tt):
    s1 = 0
    if tt ==  1:
        s1 = clientConnect(HOST,port,blocking)
    else:
        time.sleep(.5)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((HOST, port))
        s1.setblocking(blocking)
        
    print "internal connect done"
    return s1
    
def getServerType():
    parser = argparse.ArgumentParser(description='Get type.')
    parser.add_argument('type', metavar='N', type=int, nargs = 1, help = ' The type of the server (1=primart ,0=secondary).')
    return parser.parse_args().type[0]

class Server:
    host = 'localhost'
    type = 0
    share = 0
    internalConn = 0
    rotateConn = 0
    clientConn = 0
    
    def __init__(self):
    
         # are we the primary server or secondary server?
        self.type =  getServerType()
            
        # set up server to server connections
        self.internalConn  = internalConnect(self.host, internalPort, 1,self.type)
        self.rotateConn    = internalConnect(self.host, rotatePort  , 0,self.type)
        
        # set up server client connection
        if self.type == 1 :
            self.clientConn = clientConnect(self.host, primaryServerPort, 0)
        else:
            self.clientConn = clientConnect(self.host, secondaryServerPort, 0)     

    def setup(self,s):
        print "=============== setup ================"
        self.share = int(s)
        print 'Share = ' + str(self.share)

    def login(self,clientMessage):
        print "=============== login ==============="
        
        calc1 = self.share ^ int(clientMessage)
        print 'calculated ' + str(calc1)
        
        if self.type ==  1: # get the other server's value and compare   
            calc2 = int(self.internalConn.recv(1024))
            
            if calc1 == calc2:
                self.clientConn.sendall("success")
            else:
                self.clientConn.sendall("failure")
                
        else:# send the other server our value
            self.internalConn.sendall(str(calc1))


    def rotate(self,rkey):
        print "============= Rotation ==============="
        self.share = self.share ^ rkey
        print "New share = " + str(self.share ^ rkey)

    def breach(self):
        self.clientConn.sendall(str(self.share))

    def breach_notify(self):
        self.breach()
        
        time.sleep(1)
        print "============= Breach ==============="
        
        r = randint(0,9999999999)
        print " rotating shares with random "+str(r)
        	
        self.rotate(r)
        self.rotateConn.sendall(str(r))
       
    def shutdown(self):
        self.clientConn.close()
        self.internalConn.close()
        self.rotateConn.close()
    
def main():
    
    s = Server()
    i = 0;
    while 1:
        
        rotateData = tryRead(s.rotateConn)
        if rotateData != "":
            s.rotate(int(rotateData))
            continue
            
        clientData = tryRead(s.clientConn)       
        if clientData == "":
            continue     
        data = clientData.split(":",1)
        
        if data[0] == 'setup':
    	    s.setup(data[1])
        elif data[0] == 'login':
            s.login(data[1])
        elif data[0] == 'breach_notify':
    	    s.breach_notify()
        elif data[0] == 'breach':
    	    s.breach()
        elif data[0] == 'quit':
    	    break
    	else:
    	    print "invalid command:\n    ",
    	    print data[0]
    	    
    s.shutdown()
    
main()















