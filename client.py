import threading
import socket
import os
from datetime import datetime
import time
from colorama import Fore, Style

os.system("cls")
print("PyChat ver 0.5.6 --client \n")
ipadresa=input("Enter the IP adress of the server: ")
portadr=input("Enter the port of the server: ")

pc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pc.connect((ipadresa, int(portadr)))

nume=input("Enter name: ")
os.system('cls')

def primire():
    while True:
        try:
            mesaj=pc.recv(1024).decode('ascii')
            if mesaj=='nume':
                pc.send(nume.encode('ascii'))
            else:
                print(Fore.GREEN + mesaj + Style.RESET_ALL)
        except:
            print("You are no longer connected to the server!")
            pc.close()
            break

def trimitere():
    while True:
        mesaj=nume+": "+input("")
        if mesaj==nume+": exit":
            print("Leaving the chat...")
            time.sleep(1)
            print("Exiting...")
            pc.close()
            exit()
        elif mesaj==nume+": /time":
            timp=datetime.now()
            pc.send((nume+": Time is "+str(timp)).encode('ascii'))
        else:
            pc.send(mesaj.encode('ascii'))

primire_thread=threading.Thread(target=primire)
primire_thread.start()

trimitere_thread=threading.Thread(target=trimitere)
trimitere_thread.start()