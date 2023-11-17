import socket
import threading
from _thread import *
import time

host = "localhost"
port = 9999
process_Count = 0

server = socket.socket()
clients = set()
response = []
response_CountArr = []
#socket.setdefaulttimeout(50)
global_lock = threading.Lock()
time.sleep(2)
print("Coordinator started. Waiting for processes to connect.")

try:
    server.bind((host,port))
except socket.error as e:
    print(str(e))

server.listen(5000)
try:
    def Coordinator(connection):
        userinfo = connection.recv(1024).decode()
        time.sleep(2)
        print("\nNew process " + userinfo + " has joined.\n")  
        message = "Voting has been initiated. Please vote to either commit or abort"
        connection.send(message.encode()) #Voting prompt sent to other connected clients
        def commit():
            commit_alert = "---------Global Commit---------\n"
            print(commit_alert)
            #global_lock.acquire()
            #for client in clients:
            connection.sendall(commit_alert.encode()) 
            #global_lock.release()

        def abort():
            abort_alert = "---------Global Abort---------\n"
            print(abort_alert)
            #for client in clients:
            connection.sendall(abort_alert.encode())  
            
        
        vote = connection.recv(1024).decode("utf-8") # Recieves vote from other processes
        vote_prompt = (f"{userinfo} has voted: {vote}")
        print(vote_prompt)
        response_CountArr.append(1)
        response_Count = response_CountArr.__len__()
        if vote == "abort":
            abort() #Checks all votes received from the processes. If any of the process fails it directly releases a global alert.
            exit()
        
        response.append(vote)
            
        wait_condition = True
        while wait_condition == True: #If none of the processes voted abort then an additional check has been implemented which checks for all votes sent by the processes.
            if process_Count == response_Count:
                #print(process_Count)
                #print(response_Count)

            #for element in response:
                if "abort" in response:
                #if element != "commit":
                    abort()
                else:
                    commit()
                #if all(response == "commit"):
                #    commit()
                #else:
                #    abort()
            wait_condition = False
        
    while True:
        client, addr = server.accept()
        for client in clients:
            if addr not in clients:
                clients.add(addr)
        
        process_Count += 1
        print("\nProcess Count: " + str(process_Count))
        start_new_thread(Coordinator,(client,)) #This creates a new thread for every new client connected.
        
    server.close()
except error as e:
    print(e)