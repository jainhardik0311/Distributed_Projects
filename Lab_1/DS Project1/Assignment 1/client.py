import socket
import os

try:

    def recurrence():
        client = socket.socket()

        client.connect(("localhost", 9999))

        print(client.recv(1024).decode())  # Shows the welcome server message

        os.makedirs("Client", exist_ok=True)
        os.chdir("Client")


        def upload_send():
            for currentlist in os.listdir("."):
                listoffiles = str(currentlist)
            print(listoffiles)
            client.send(f"{listoffiles}".encode())
            print(
                "\nAll files present in the current directory has been sent to Server and waiting for its response... "
            )
            toupload = client.recv(1024).decode("utf-8")
            # get the file size
            print("\nResponse has been received from Server. \nOperation is being performmed. \nPlease be patient.")
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
            print("Upload Operation has been performed from Client to Server.\n")


        def download_recv():
            
            Currentserverlist = client.recv(1024).decode()
            print(
                "\nThe files present in the current directory of server are displayed below\n"
            )
            print(Currentserverlist)
            recfilename = str(
                input("\nEnter the file name which needs to be downloaded from server: \n")
            )
            client.send(recfilename.encode())

            print("\nFile has been downloaded from server.\n")
            print(client.recv(1024).decode())  # Prints the filename and filesize
            with open("received.txt", "a+") as f:
                # read 1024 bytes from the socket (receive)
                bytes_read = client.recv(1024)
                str_read = str(bytes_read)
                f.write(str_read)



        def rename():
            Currentserverlist = client.recv(1024).decode()
            print("\nThe files present in the current directory are displayed below\n")
            print(Currentserverlist)
            oldname = str(input("\nEnter the file name which needs to be renamed: \n"))
            client.send(oldname.encode())
            newname = str(input("\nEnter new file name: \n"))
            client.send(newname.encode())


        def delete():
            Currentserverlist = client.recv(1024).decode()
            print("\nThe files present in the current directory are displayed below\n")
            print(Currentserverlist)
            filename = str(input("\nEnter the file name which needs to be renamed: \n"))
            client.sendall(filename.encode())
            print("\nThe operation has been performed.\n")


        print("\nSelect operations to be performed: ")
        print(
            "\n 1. Insert 1 for Upload \n 2. Insert 2 for Download \n 3. Insert 3 for Rename \n 4. Insert 4 for Delete \n"
        )
        option = str(input("Insert number of operation to be performed: "))
        client.sendall(f"{option}".encode("utf-8"))

        if option == "1":
            upload_send()
        elif option == "2":
            download_recv()
        elif option == "3":
            rename()
        elif option == "4":
            delete()
        else:
            print(
                "Incorrect Option Selected. \nPlease run the code again with the correct option"
            )

        client.close()
    recurrence()

    while True:
        num = input("Please enter 1 to continue or 2 to exit: ")
        if num == "1":
            recurrence()
        else:
            quit()

except Exception as x:
    print(f"An exception occurred: \n {x}")
