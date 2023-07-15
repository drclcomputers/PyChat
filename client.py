import threading
import socket
import os
import time
from colorama import Fore, Style

os.system("cls")
print("PyChat ver 0.6.8 --client \n")
ipadresa=input("Enter the adress of the server: ")
portadr=input("Enter the port of the server: ")

pc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pc.connect((ipadresa, int(portadr)))

nume=input("Enter name: ")
os.system('cls')

running=True
def primire():
    global running
    while True:
        if running==False:
            break
        try:
            mesaj=pc.recv(1024).decode('ascii')
            if mesaj=='nume':
                pc.send(nume.encode('ascii'))
            elif mesaj=="ADMIN":
                password=input("Enter admin password: ")
                pc.send(password.encode('ascii'))
            elif mesaj=='KICKYOU':
                pc.close()
                print("You've been kicked from the group chat! \n")
                print("You are no longer connected to the server!")
                time.sleep(1)
                print("Closing the client...")
                running=False
                break
            else:
                if mesaj.startswith(nume+": "):
                    pass
                else:
                    print(Fore.GREEN + mesaj + Style.RESET_ALL)
        except:
            pc.close()
            print("You are no longer connected to the server!")
            time.sleep(1)
            print("Closing the client...")
            running=False
            break

def trimitere():
    global running
    while True:
        if running==False:
            pc.close()
            break
        mesaj=nume+": "+input("")
        if mesaj[len(nume)+2].startswith("/"):
            if mesaj[len(nume)+2:].startswith("/exit"):
                pc.send("EXIT".encode('ascii'))
                running=False
                print("You are no longer connected to the server!")
                time.sleep(1)
                print("Closing the client...")
                exit()
            if mesaj[len(nume)+2:].startswith("/list"):
                pc.send("LIST".encode('ascii'))
            if mesaj[len(nume)+2:].startswith("/time"):
                pc.send("TIME".encode('ascii'))
            if mesaj[len(nume)+2:].startswith("/clear"):
                os.system('cls')
            if mesaj[len(nume)+2:].startswith("/help"):
                pc.send("HELP".encode('ascii'))
            if mesaj[len(nume)+2:].startswith("/pass"):
                password=mesaj[len(nume)+8:]
                pc.send(password.encode('ascii'))
            if mesaj[len(nume)+2:].startswith("/kick"):
                perskick=mesaj[len(nume)+8:]
                pc.send(("KICK "+perskick).encode('ascii'))
        else:
            pc.send(mesaj.encode('ascii'))

primire_thread=threading.Thread(target=primire)
primire_thread.start()

trimitere_thread=threading.Thread(target=trimitere)
trimitere_thread.start()