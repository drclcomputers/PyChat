import threading
import socket
import os
import time

os.system("cls")
print("PyChat ver 0.5.9 --client \n")
ipadresa=input("Enter the adress of the server: ")
portadr=input("Enter the port of the server: ")

pc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pc.connect((ipadresa, int(portadr)))

nume=input("Enter name: ")
os.system('cls')

def primire():
    global aux, nume
    while True:
        try:
            mesaj=pc.recv(1024).decode('ascii')
            if mesaj=='nume':
                pc.send(nume.encode('ascii'))
            else:
                if aux==mesaj:
                    pass
                else:
                    print(mesaj)
        except:
            print("You are no longer connected to the server!")
            pc.close()
            break

def trimitere():
    global aux
    while True:
        mesaj=nume+": "+input("")
        aux=mesaj
        if mesaj==nume+": /exit":
            print("Leaving the chat...")
            time.sleep(1)
            print("Closing the client...")
            pc.close()
            exit()
        else:
            pc.send(str(mesaj).encode('ascii'))

primire_thread=threading.Thread(target=primire)
primire_thread.start()

trimitere_thread=threading.Thread(target=trimitere)
trimitere_thread.start()