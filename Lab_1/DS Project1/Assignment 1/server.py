import socket
import os

server = socket.socket()
print("Socket is created")

server.bind(("localhost", 9999))

server.listen(5000)
print("Waiting for connections")    

os.makedirs("Server", exist_ok=True)
os.chdir("Server")


def upload_rec():

    Currentserverlist = client.recv(1024).decode()
    print(
        "\nThe files present in the current directory of client are displayed below\n"
    )
    print(Currentserverlist)
    recfilename = str(
        input("\nEnter the file name which needs to be downloaded from client: \n")
    )
    client.send(recfilename.encode())

    print("\nFile has been downloaded from client.\n")
    print(client.recv(1024).decode())  # Prints the filename and filesize
    with open("received.txt", "a+") as f:
        # read 1024 bytes from the socket (receive)
        bytes_read = client.recv(1024)
        str_read = str(bytes_read)
        f.write(str_read)


def download_send():

    for currentlist in os.listdir("."):
        listoffiles = str(currentlist)
    print(listoffiles)
    client.send(f"{listoffiles}".encode())
    print(
        "\nAll files present in the current directory has been sent to Client and waiting for its response... "
    )
    toupload = client.recv(1024).decode("utf-8")
    # get the file size
    print("\nResponse has been received from Client. \nOperation is being performmed. \nPlease be patient.")
    filesize = os.path.getsize(toupload)
    dataToSend = (
        "Recieved filename is: "
        + toupload
        + " & its filesize is: "
        + str(filesize)
        + "\n"
    )
    client.sendall(dataToSend.encode())
    print("\n")
    with open(toupload, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read()
            if not bytes_read:
                # file transmitting is done
                break
            client.sendall(bytes_read)
    print("Download Operation has been performed from Server to Client.\n")


def rename():
    for currentlist in os.listdir("."):
        list = str(currentlist)
    client.send(f"{list}".encode())
    oldname = client.recv(1024).decode("utf-8")
    newname = client.recv(1024).decode("utf-8")
    os.rename(oldname, newname)
    print(f"\nRename operation has been performed. {oldname} is renamed to {newname}\n")


def delete():
    for currentlist in os.listdir("."):
        list = str(currentlist)
    client.send(f"{list}".encode())
    file = client.recv(1024).decode("utf-8")
    os.remove(file)
    print(f"\n Delete operation has been performed. {file} has been deleted.\n")


while True:
    client, addr = server.accept()
    print("Connected with ", addr)
    client.send(bytes("Welcome to Hardik's server".encode("utf-8")))
    option = client.recv(1024).decode("utf-8")
    print(f"The selected options is: {option}")
    if option == "1":
        upload_rec()
    elif option == "2":
        download_send()
    elif option == "3":
        rename()
    elif option == "4":
        delete()
    else:
        print(
            "Incorrect Option Selected. \nPlease run the code again with the correct option"
        )

    client.close()
