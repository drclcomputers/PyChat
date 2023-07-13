import threading
import socket
import os
import time

os.system("cls")
print("PyChat ver 0.5.6 --server \n")
host=input("Enter the IP of this device: ")
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
            trimitere(mesaj)
        except:
            index=pcs.index(pc)
            pcs.remove(pc)
            pc.close()
            nume=numes[index]
            trimitere(("--"+nume + " left the chat!--").encode('ascii'))
            numes.remove(nume)
            print(str(pc)+" deconnected!")
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
        trimitere(("--"+nume + ' entered the chat! --').encode('ascii'))

        thread=threading.Thread(target=handle, args=(pc,))
        thread.start()

print("Server starting...")
time.sleep(1)
print("Server configuring...")
time.sleep(1)
print("Server is online!")
primire()