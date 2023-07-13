import threading
import socket
import os
import time

os.system("cls")
print("PyChat ver 0.5.8 --server \n")
hostname=socket.gethostname()
host=socket.gethostbyname(hostname)
print("Your IP adress is "+host)
port=input("Enter your desire server port (recommended 55555): ")
print("In order for other computers to connect, you'll need to open the respective port!")

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, int(port)))
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