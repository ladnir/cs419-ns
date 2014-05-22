from sys import stdin
from random import randint
import time

class Server:
	share = "NULL"
	
class Client:
	password = "NULL"

class BadGuy:
	share1 = "NULL"
	share2 = "NULL"

def setup(server1, server2, client):
	print "=============== setup ================"

	print " password?: ",
	client.password =  int(stdin.readline())

	
	r = randint(0,9999999999)
	print "random mask = "+str(r),;stdin.readline()

	server1.share = r
	server2.share = r ^ client.password
	print " server1's share = "+str(server1.share) + ". (random)",;stdin.readline()
	print "server2's share = "+str(server2.share) + ".  (password XOR random)",;stdin.readline()


def login(server1, server2, client):
	print "=============== login ==============="
	r = randint(0,9999999999)

	print " client picks a random number: "+str(r),;stdin.readline()
	message1 = client.password ^ r
	message2 = r

	print "client sends server1 "+str(message1)+". (password XOR random)",;stdin.readline()
	print "client sends server2 "+str(message2)+". (just the random)",;stdin.readline()
	print

	print "server1 calculated "+str(server1.share ^ message1)+ " (message XOR share)",;stdin.readline()
	print "server2 calculated "+str(server2.share ^ message2)+ " (message XOR share)",;stdin.readline()
	print
	if (server1.share ^ message1) == (server2.share ^ message2):
		print "values match. login successful!",;stdin.readline()
	else:
		print "values dont match. login failed",;stdin.readline()
	print

def rotate( server1, server2):
	print "============= Rotation ==============="

	r = randint(0,9999999999)
	print " rotating shares with random "+str(r),;stdin.readline()


	server1.share = server1.share ^ r
	server2.share = server2.share ^ r

	print "server1's new share = "+str(server1.share),;stdin.readline()
	print "server2's new share = "+str(server2.share),;stdin.readline()

	print

def leak(server,badGuy,i,client):

	print "============ leak server"+str(i)+"'s share ==============="
	if i == 1:
		badGuy.share1 = server.share
		if badGuy.share2 != "NULL":
			print "bad guy thinks password is "+ str(badGuy.share1 ^ badGuy.share2),;stdin.readline()
			if (badGuy.share1 ^ badGuy.share2) == client.password:
				print "Oh nooo, the password is leaked!!!",;stdin.readline()
			else:
				print "but he's wrong!",;stdin.readline()
		else:
			print "bad guy knows only 1 share",;stdin.readline()
	if i == 2:
		badGuy.share2 = server.share
		if badGuy.share1 != "NULL":
			print "bad guy thinks password is "+ str(badGuy.share1 ^ badGuy.share2),;stdin.readline()
			if (badGuy.share1 ^ badGuy.share2) == client.password:
				print "Oh nooo, the password is leaked!!!",;stdin.readline()
			else:
				print "but he's wrong!",;stdin.readline()
		else:
			print "bad guy knows only 1 share",;stdin.readline()
	

def main():
	server1 = Server()
	server2 = Server() 
	client  = Client()
	badGuy = BadGuy()

	input = "start"

	while(input != "quit\n"):
		print "\ncommand?: ",
		input = stdin.readline()
		if input == "setup\n":
			setup(server1, server2, client)
		if input == "login\n":
			login(server1, server2, client)
		if input == "rotate\n":
			rotate(server1, server2)
		if input == "leak share1\n":
			leak(server1,badGuy,1,client)
		if input == "leak share2\n":
			leak(server2,badGuy,2,client)

main()
