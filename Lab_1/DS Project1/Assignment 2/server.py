import socket
import os
import threading

ThreadCount = 0

server = socket.socket()
print("[Starting] Socket is created & Server is Created")

server.bind(("localhost", 9999))

server.listen(5000)
print("[Listenning] Waiting for connections")

os.makedirs("Server", exist_ok=True)
os.chdir("Server")


def threaded_client():
    client.sendall(bytes("Welcome to Hardik's server".encode("utf-8")))

    def upload():
        with open("mytext.txt", "w") as f:
            f.write("Debugging at its best")

        with open("mytext.txt") as f:
            message = f.read()

        filename = "mytext.txt"  # get the filename
        filesize = os.path.getsize(filename)  # get the filesize
        dataToSend = (
            "Recieved filename is: " + filename + " & its filesize is: " + str(filesize)
        )
        client.sendall(dataToSend.encode())

        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read()
                if not bytes_read:
                    # file transmitting is done
                    break
                client.sendall(bytes_read)
        print("\nUpload operation has been performed\n")

    def download():
        print("\nDownload operation has been performed\n")
        print(client.recv(1024).decode())  # Prints the filename and filesize
        with open("received.txt", "a+") as f:
            # read 1024 bytes from the socket (receive)
            bytes_read = client.recv(1024)
            str_read = str(bytes_read)
            f.write(str_read)

    def rename():
        for currentlist in os.listdir("."):
            list = str(currentlist)
        client.sendall(f"{list}".encode())
        oldname = client.recv(1024).decode("utf-8")
        newname = client.recv(1024).decode("utf-8")
        os.rename(oldname, newname)
        print(
            f"\nRename operation has been performed. {oldname} is renamed to {newname}\n"
        )

    def delete():
        for currentlist in os.listdir("."):
            list = str(currentlist)
        client.sendall(f"{list}".encode())
        file = client.recv(1024).decode("utf-8")
        os.remove(file)
        print(f"\n Delete operation has been performed. {file} has been deleted.\n")

    option = client.recv(1024).decode("utf-8")
    print(f"The selected options is: {option}")
    if option == "1":
        upload()
    elif option == "2":
        download()
    elif option == "3":
        rename()
    elif option == "4":
        delete()
    else:
        print(
            "Incorrect Option Selected. \nPlease run the code again with the correct option"
        )


while True:
    client, addr = server.accept()
    print("Connected with ", addr)
    t = threading.Thread(target=threaded_client)
    t.start()
    ThreadCount += 1
    print("Thread Number: " + str(ThreadCount))

server.close()
