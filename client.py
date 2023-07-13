import threading
import socket
import os

print("PyChat ver 0.3.7 --client")
ipadresa=input("Introduceti adresa IP a serverului: ")
nume=input("Introduceti numele: ")

pc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pc.connect(('127.0.0.1', 55555))

def primire():
    while True:
        try:
            mesaj=pc.recv(1024).decode('ascii')
            if mesaj=='nume':
                pc.send(nume.encode('ascii'))
            else:
                print(mesaj)
        except:
            print("Error!")
            pc.close()
            break

def trimitere():
    while True:
        mesaj=nume+": "+input("")
        if mesaj==nume+": exit":
            os.system('exit')
            exit()
        else:
            pc.send(mesaj.encode('ascii'))

primire_thread=threading.Thread(target=primire)
primire_thread.start()

trimitere_thread=threading.Thread(target=trimitere)
trimitere_thread.start()