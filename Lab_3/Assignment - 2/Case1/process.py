import socket
import time

client = socket.socket()
host = "localhost"
port = 9999

try:
    client.connect((host,port))
except socket.error as e:
    print(str(e))

#while True:

# client = socket.socket()
# client.connect(("localhost", 9999))

username = input("Please enter your name: ")
#user = ("New user " + username + "has joined. ")
client.send(username.encode())

print(f"\nWelcome {username}!\n")
vote_prompt = client.recv(1024).decode() #Vote prompt received from server end.
print(vote_prompt)

#print(client.recv(1024).decode())  # Prints the voting message
option = str.lower(input()) # Stores user input
#while option:
client.sendall(f"{option}".encode("utf-8")) #Sends user input
final_alert = client.recv(1024).decode() #Receives global abort
print(final_alert)

client.close()
