import threading
import socket
import os
import time
from colorama import Fore, Style

os.system("cls")
print("PyChat ver 0.7.3 --client \n")
ipadresa=input("Enter the adress of the server: ")
portadr=input("Enter the port of the server: ")

pc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pc.connect((ipadresa, int(portadr)))

nume=input("Enter name: ")
os.system('cls')

running=True
def primire():
    global running, password
    while True:
        if running==False:
            break
        try:
            mesaj=pc.recv(1024).decode("utf-8")
            if mesaj=='nume':
                pc.send(nume.encode("utf-8"))
            elif mesaj=='.KICKYOU':
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
    global running, password
    while True:
        if running==False:
            pc.close()
            break
        mesaj=nume+": "+input("")
        if mesaj[len(nume)+2].startswith("/"):
            if mesaj[len(nume)+2:].startswith("/exit"):
                pc.send(".EXIT".encode("utf-8"))
                running=False
                print("You are no longer connected to the server!")
                time.sleep(1)
                print("Closing the client...")
                exit()
            if mesaj[len(nume)+2:].startswith("/list"):
                pc.send(".LIST".encode("utf-8"))
            if mesaj[len(nume)+2:].startswith("/time"):
                pc.send(".TIME".encode("utf-8"))
            if mesaj[len(nume)+2:].startswith("/clear"):
                os.system('cls')
            if mesaj[len(nume)+2:].startswith("/help"):
                pc.send(".HELP".encode("utf-8"))
            if mesaj[len(nume)+2:].startswith("/password "):
                password=mesaj[len(nume)+12:]
                print(password)
                pc.send((".PASSADMIN "+password).encode("utf-8"))
            if mesaj[len(nume)+2:].startswith("/kick"):
                perskick=mesaj[len(nume)+8:]
                pc.send((".KICK "+perskick).encode("utf-8"))
            if mesaj[len(nume)+2:].startswith("/admin"):
                pc.send(".ADMINLIST".encode("utf-8"))
        else:
            pc.send(mesaj.encode("utf-8"))

primire_thread=threading.Thread(target=primire)
primire_thread.start()

trimitere_thread=threading.Thread(target=trimitere)
trimitere_thread.start()