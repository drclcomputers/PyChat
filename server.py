import threading
import socket
import os
import time
from datetime import datetime

os.system("cls")
print("PyChat ver 0.7.7 --server \n")
ip=input("Input server (this pc's) IP address: ")
host=str(ip)
port=55555
passwordreal=input("Set admin password: ")

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
    "/admin":"Shows the list of the admins",
    "/password":"Enter the password to become an admin (exp: /password password)",
    "/kick":"(Admin privileges required) Kicks a member (exp: /kick member1)",
    "/exit":"Disconnects from the servers and closes the client",
    "/help":"Shows help"
}

password=None

def trimitere(mesaj):
    for pc in pcs:
        pc.send(mesaj)

def handle(pc):
    while True:
        try:
            mesaj=pc.recv(1024).decode("utf-8")
            if mesaj.startswith('.'):
                if mesaj=='.LIST':
                    pc.send(str(numes).encode("utf-8"))
                if mesaj=='.ADMINLIST':
                    pc.send(str(admins).encode("utf-8"))
                if mesaj=='.TIME':
                    timp=datetime.now()
                    pc.send(str(timp).encode("utf-8"))
                if mesaj=='.EXIT':
                    pc.close()
                    trimitere(str("--"+nume + " left the chat!--").encode("utf-8"))
                    pcs.remove(pc)
                    numes.remove(nume) 
                if mesaj=='.HELP':
                    pc.send(str(comenzi).encode("utf-8"))
                if mesaj.startswith('.PASSADMIN'):
                    password=mesaj[11:]
                    print("Tried password is: ."+password+".")
                    if password==passwordreal:
                        pc.send("You are now an admin!".encode("utf-8"))
                        index=pcs.index(pc)
                        nume=numes[index]
                        admins.append(nume)
                    else:
                        pc.send("Wrong password!!!".encode("utf-8"))
                    print(str(admins))
                if mesaj.startswith('.KICK '):
                    index=pcs.index(pc)
                    nume=numes[index]
                    if nume in admins:
                        perskick=mesaj[6:]
                        print("kicking "+perskick)
                        if perskick in numes and perskick!=nume:
                            index2=numes.index(perskick)
                            pcrt=pcs[index2]
                            numes.remove(perskick)
                            pcs.remove(pcrt)
                            pcrt.send(".KICKYOU".encode("utf-8"))
                            pcrt.close()
                        else:
                            pc.send("Person isn't in the chat or is you!".encode("utf-8"))
                    else:
                        pc.send("You are not the admin!".encode("utf-8"))
            else:
                trimitere(mesaj.encode("utf-8"))
        except:
            index=pcs.index(pc)
            print(str(pc)+" disconnected!")
            pcs.remove(pc)
            pc.close()
            nume=numes[index]
            trimitere(str("--"+nume + " left the chat!--").encode("utf-8"))
            numes.remove(nume)
            break

def primire():
    while True:
        pc, adresa=server.accept()
        print("Connected "+str(adresa))

        pc.send('nume'.encode("utf-8"))
        nume=pc.recv(1024).decode("utf-8")
        numes.append(nume)
        pcs.append(pc)

        pc.send('--Succesfully connected to the server!-- \n'.encode("utf-8"))
        trimitere(('--'+nume + ' joined the chat!--').encode("utf-8"))

        thread=threading.Thread(target=handle, args=(pc,))
        thread.start()

print("Server starting...")
time.sleep(1)
print("Server configuring...")
time.sleep(1)
print("Server is online!")
primire()