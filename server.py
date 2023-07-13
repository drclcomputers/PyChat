import threading
import socket

print("PyChat ver 0.3.7 --server")
host=input("Adresa IP a dispozitivului")
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
            trimitere((nume + " a parasit chatul!").encode('ascii'))
            numes.remove(nume)
            print(str(pc)+" deconectat")
            break

def primire():
    while True:
        pc, adresa=server.accept()
        print("Conectat cu adresa "+str(adresa))

        pc.send('nume'.encode('ascii'))
        nume=pc.recv(1024).decode('ascii')
        numes.append(nume)
        pcs.append(pc)

        trimitere((nume + ' a intrat in chat! \n').encode('ascii'))
        pc.send('Conectat la server!'.encode('ascii'))

        thread=threading.Thread(target=handle, args=(pc,))
        thread.start()

print("Server starting...")
primire()