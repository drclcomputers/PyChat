import threading
import socket
import os
import time
from datetime import datetime

os.system("cls")
print("PyChat ver 0.5.9 --server \n")
host='127.0.0.1'
port=55555

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

pcs=[]
numes=[]

def trimitere(mesaj):
    for pc in pcs:
        pc.send(mesaj)

def handle(pc):
    while True:
        try:
            mesaj=pc.recv(1024)
            if mesaj.decode('ascii')=='LIST':
                trimitere(str(numes).encode('ascii'))
            else:
                trimitere(mesaj)
        except:
            index=pcs.index(pc)
            nume=numes[index]
            trimitere(str("--"+nume + " left the chat!--").encode('ascii'))
            numes.remove(nume)
            print(str(pc)+" disconnected!")
            pc.close()
            pcs.remove(pc)
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