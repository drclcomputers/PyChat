import threading
import socket
import os
import time
from datetime import datetime

os.system("cls")
print("PyChat ver 0.6.8 --server \n")
host='127.0.0.1'
port=55555

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

pcs=[]
numes=[]
admins=[]

comenzi={
    "/clear":"Clear the chat",
    "/time":"Sends the time and date",
    "/list":"Shows all the members of the chat",
    "/exit":"Disconnects from the servers and closes the client",
    "/help":"Shows help"
}

passwordreal="pychatetare"
password=None

def trimitere(mesaj):
    for pc in pcs:
        pc.send(mesaj)

def handle(pc):
    while True:
        try:
            mesaj=pc.recv(1024)
            if mesaj.decode('ascii')=='LIST':
                trimitere(str(numes).encode('ascii'))
            elif mesaj.decode('ascii')=='TIME':
                timp=datetime.now()
                trimitere(str(timp).encode('ascii'))
            elif mesaj.decode('ascii')=='EXIT':
                pc.close()
                trimitere(str("--"+nume + " left the chat!--").encode('ascii'))
            elif mesaj.decode('ascii')=='HELP':
                pc.send(str(comenzi).encode('ascii'))
            elif mesaj.decode('ascii')=='PASS':
                pc.send("ADMIN")
                password=pc.recv(1024)
                if password.decode('ascii')==passwordreal:
                    pc.send("You are now an admin!".encode('ascii'))
                    admins.append(pc)
            elif mesaj.decode('ascii')=='KICK' and password==passwordreal:
                if pc in admins:
                    pc.send(str(numes).encode('ascii'))
                    pc.send('NKICK'.encode('ascii'))
                    nkick=pc.recv(1024).decode('ascii')
                    if nkick in numes:
                        index=numes.index(nkick)
                        numes.remove(nkick)
                        pcrt=pcs.index(index)
                        pcrt.close()
                        pcs.remove(pcrt)
                        pcrt.send("KICKYOU".encode('ascii'))
                    else:
                        pc.send("Member isn't in the chat!".encode("ascii"))
                else:
                    pc.send("You are not the admin!".encode('ascii'))
            else:
                trimitere(mesaj)
        except:
            index=pcs.index(pc)
            print(str(pc)+" disconnected!")
            pcs.remove(pc)
            pc.close()
            nume=numes[index]
            trimitere(str("--"+nume + " left the chat!--").encode('ascii'))
            numes.remove(nume)
            break

def primire():
    while True:
        pc, adresa=server.accept()
        print("Connected "+str(adresa))

        pc.send('nume'.encode('ascii'))
        nume=pc.recv(1024).decode('ascii')
        numes.append(nume)
        pcs.append(pc)

        pc.send('--Succesfully connected to the server!-- \n'.encode('ascii'))
        trimitere(('--'+nume + ' joined the chat!--').encode('ascii'))

        thread=threading.Thread(target=handle, args=(pc,))
        thread.start()

print("Server starting...")
time.sleep(1)
print("Server configuring...")
time.sleep(1)
print("Server is online!")
primire()